#!/usr/bin/env python3
"""Rotate the shared instructor passphrase across every CCGate payload.

CCGate caches exactly ONE passphrase per origin, so all payloads on the site
must share it. This rotates all of them together, in one pass:

    class-console/index.html   (the attendance codes for all four courses)
    poll-admin/index.html
    poll-secret.js             (the Supabase poll secret -- minted fresh)

You run this. It asks for the current passphrase and a new one, and prints
nothing but the SQL line you paste into Supabase. Neither passphrase is
stored, echoed or logged.

    python3 rotate.py

Afterwards: git add -u && git commit && git push, and unlock any browser once
with the new passphrase.
"""
import base64, getpass, hashlib, json, os, re, secrets, shutil, sys, time
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

ITER = 600_000
HERE = os.path.dirname(os.path.abspath(__file__))
PAGES = ["class-console/index.html", "poll-admin/index.html"]
PAT = re.compile(r'(payload:\s*)(\{.*?\})(\s*,\s*\n)', re.S)
B = lambda x: base64.b64encode(x).decode()


def ask(prompt):
    # Pasting from a browser console often brings the surrounding quotes along;
    # they are invisible in a getpass prompt and fail with no explanation.
    v = getpass.getpass(prompt).strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        v = v[1:-1].strip()
        print("  (stripped the surrounding quotes)")
    return v


def decrypt(pl, p):
    key = hashlib.pbkdf2_hmac("sha256", p.encode(), base64.b64decode(pl["salt"]), pl["iter"], dklen=32)
    return AESGCM(key).decrypt(base64.b64decode(pl["iv"]), base64.b64decode(pl["ct"]), None)


def encrypt(clear, p):
    salt, iv = os.urandom(16), os.urandom(12)
    key = hashlib.pbkdf2_hmac("sha256", p.encode(), salt, ITER, dklen=32)
    return {"salt": B(salt), "iv": B(iv), "ct": B(AESGCM(key).encrypt(iv, clear, None)), "iter": ITER}


def print_sql():
    """--sql : re-print the SQL line for the secret ALREADY in poll-secret.js.

    For when the rotation worked but its SQL never reached Supabase. This does
    NOT mint a new secret -- it decrypts the one you already published, so the
    file and the database end up agreeing instead of drifting further apart.
    """
    here = os.path.dirname(os.path.abspath(__file__))
    ps = os.path.join(here, "poll-secret.js")
    if not os.path.exists(ps):
        sys.exit("poll-secret.js not found.")
    pl = json.loads(re.search(r"=\s*(\{.*\});", open(ps).read(), re.S).group(1))
    pw = ask("Instructor passphrase (the CURRENT one): ")
    try:
        secret = json.loads(decrypt(pl, pw))["poll_secret"]
    except Exception:
        sys.exit("\nThat passphrase does not open poll-secret.js.\n"
                 "So the problem is the PASSPHRASE, not the SQL. Nothing was changed.\n"
                 "If the current one is truly lost, the pre-rotation files are in\n"
                 "the .rotate-backup-* directory and can be restored.")
    print("\n  poll-secret.js opened. The passphrase is correct.\n")
    print("=" * 72)
    print("PASTE THIS INTO THE SUPABASE SQL EDITOR AND PRESS RUN:")
    print("=" * 72)
    print("insert into public.poll_secrets (k, v)")
    print("values ('instructor', '%s')" % secret)
    print("on conflict (k) do update set v = excluded.v;")
    print("=" * 72)
    print("\nNo new secret was minted and no file changed.")
    print("Do not paste the line above into a chat -- it is the live secret.\n")


def main():
    old = ask("CURRENT passphrase: ")
    if not old:
        sys.exit("Nothing entered.")

    # Read and decrypt everything FIRST. Nothing is written until every payload
    # has been proved readable -- a half-rotated site locks you out.
    clears = {}
    for rel in PAGES:
        path = os.path.join(HERE, rel)
        if not os.path.exists(path):
            sys.exit("Missing " + rel)
        m = PAT.search(open(path, encoding="utf-8").read())
        if not m:
            sys.exit("No payload found in " + rel)
        try:
            clears[rel] = decrypt(json.loads(m.group(2)), old)
        except Exception:
            sys.exit("\nThat passphrase does not unlock %s.\nNothing was changed." % rel)
    print("Current passphrase verified against all %d payloads.\n" % len(PAGES))

    new = ask("NEW passphrase: ")
    if len(new) < 8:
        sys.exit("Too short. Nothing was changed.")
    if ask("NEW passphrase again: ") != new:
        sys.exit("They do not match. Nothing was changed.")
    if new == old:
        sys.exit("That is the current passphrase. Nothing was changed.")

    stamp = time.strftime("%Y%m%d-%H%M%S")
    backup = os.path.join(HERE, ".rotate-backup-" + stamp)
    os.makedirs(backup, exist_ok=True)

    for rel in PAGES:
        path = os.path.join(HERE, rel)
        shutil.copy2(path, os.path.join(backup, rel.replace("/", "_")))
        s = open(path, encoding="utf-8").read()
        pl = encrypt(clears[rel], new)
        s = PAT.sub(lambda m: m.group(1) + json.dumps(pl) + m.group(3), s, count=1)
        open(path, "w", encoding="utf-8").write(s)
        # prove the file we just wrote actually opens with the new passphrase
        chk = PAT.search(open(path, encoding="utf-8").read())
        assert decrypt(json.loads(chk.group(2)), new) == clears[rel], rel
        print("  rotated + verified:", rel)

    poll_secret = secrets.token_urlsafe(32)
    ps = os.path.join(HERE, "poll-secret.js")
    if os.path.exists(ps):
        shutil.copy2(ps, os.path.join(backup, "poll-secret.js"))
    pl = encrypt(json.dumps({"poll_secret": poll_secret}).encode(), new)
    open(ps, "w").write(
        "/* Generated by rotate.py -- do not hand-edit.\n"
        " * Supabase poll secret, encrypted under the shared instructor passphrase\n"
        " * (PBKDF2-SHA256 %d -> AES-GCM). Ciphertext only; safe to publish.\n"
        " */\nwindow.POLL_SECRET_PAYLOAD = %s;\n" % (ITER, json.dumps(pl)))
    assert json.loads(decrypt(pl, new))["poll_secret"] == poll_secret
    print("  rotated + verified: poll-secret.js (new secret minted)\n")

    print("Backup of the previous files:", backup)
    print("\n" + "=" * 72)
    print("PASTE THIS INTO THE SUPABASE SQL EDITOR AND PRESS RUN:")
    print("=" * 72)
    print("insert into public.poll_secrets (k, v)")
    print("values ('instructor', '%s')" % poll_secret)
    print("on conflict (k) do update set v = excluded.v;")
    print("=" * 72)
    print("\nThen:  git add -u && git add poll-secret.js && git commit && git push")
    print("Every browser must be unlocked once with the NEW passphrase.")
    print("Do not paste the line above into a chat -- it is the live secret.\n")


if __name__ == "__main__":
    if "--sql" in sys.argv:
        print_sql()
    else:
        main()
