#!/usr/bin/env python3
"""Generate poll-secret.js — the CCGate-encrypted Supabase poll secret.

You run this. It asks for the SAME passphrase that unlocks /poll-admin/ and
/class-console/. It then invents a random machine secret, encrypts it under
that passphrase in exactly the format auth.js expects, and prints the one SQL
line you paste into Supabase.

Nobody -- not Claude, not the repo, not a student -- ever sees either value.
The passphrase is never stored, and the machine secret is never printed except
in the SQL line you paste and then discard.

    python3 make-poll-secret.py
"""
import base64, getpass, hashlib, json, os, secrets, sys
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

ITER = 600_000          # must match the other CCGate payloads on this site
B = lambda x: base64.b64encode(x).decode()

def unquote(v):
    """Pasting from a browser console brings the surrounding quotes along, and
    they are invisible at a getpass prompt. Chrome's console prints strings
    quoted, so this is the single likeliest way to mistype a correct value."""
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        print("  (stripped the surrounding quotes)")
        return v[1:-1].strip()
    return v


def check(passphrase):
    """Decrypt the existing class-console payload. Wrong passphrase -> stop."""
    import re
    here = os.path.dirname(os.path.abspath(__file__))
    ref = os.path.join(here, "class-console", "index.html")
    if not os.path.exists(ref):
        print("! class-console/index.html not found -- cannot verify the passphrase.")
        return
    m = re.search(r'payload:\s*(\{.*?\})\s*,\s*\n', open(ref, encoding="utf-8").read(), re.S)
    if not m:
        print("! could not find the class-console payload -- skipping verification.")
        return
    pl = json.loads(m.group(1))
    key = hashlib.pbkdf2_hmac("sha256", passphrase.encode(),
                              base64.b64decode(pl["salt"]), pl["iter"], dklen=32)
    try:
        AESGCM(key).decrypt(base64.b64decode(pl["iv"]), base64.b64decode(pl["ct"]), None)
    except Exception:
        sys.exit("\nThat is NOT the passphrase that unlocks /class-console/ and /poll-admin/.\n"
                 "It has to be the same one, or your browser can never decrypt what this\n"
                 "script writes -- and the failure would be silent.\n"
                 "Nothing was written. Try again with the shared instructor passphrase.")
    print("Passphrase verified against the existing class-console payload.\n")


def verify():
    """--check : is the secret in poll-secret.js the one Supabase actually holds?

    Side-effect free. close_poll() checks the passphrase first, then UPDATEs zero
    rows for a poll id that does not exist, so nothing is created or changed.
    """
    import urllib.request, urllib.error
    SU = "https://dpntbrsorgbivmntwmod.supabase.co"
    ANON = ("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRwbnRicnNvcmdiaXZt"
            "bnR3bW9kIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU4NjY5NzksImV4cCI6MjA5MTQ0Mjk3OX0."
            "7__ja5Sq2AB__iFXhj-CKZJ0l7SjUerf8mpGQlo2bxI")
    here = os.path.dirname(os.path.abspath(__file__))
    ps = os.path.join(here, "poll-secret.js")
    if not os.path.exists(ps):
        sys.exit("poll-secret.js does not exist yet. Run this script with no arguments first.")
    import re
    pl = json.loads(re.search(r"=\s*(\{.*\});", open(ps).read(), re.S).group(1))

    pw = unquote(getpass.getpass("Instructor passphrase: ").strip())
    key = hashlib.pbkdf2_hmac("sha256", pw.encode(), base64.b64decode(pl["salt"]), pl["iter"], dklen=32)
    try:
        secret = json.loads(AESGCM(key).decrypt(
            base64.b64decode(pl["iv"]), base64.b64decode(pl["ct"]), None))["poll_secret"]
    except Exception:
        sys.exit("That passphrase does not open poll-secret.js. (Wrong passphrase, or the file\n"
                 "was generated under a different one -- regenerate it.)")
    print("  poll-secret.js opens with this passphrase.")

    body = json.dumps({"p_poll_id": "__probe__", "p_session_key": "__probe__",
                       "p_pass": secret}).encode()
    req = urllib.request.Request(SU + "/rest/v1/rpc/close_poll", data=body, method="POST",
                                 headers={"apikey": ANON, "Authorization": "Bearer " + ANON,
                                          "Content-Type": "application/json"})
    try:
        urllib.request.urlopen(req, timeout=15)
    except urllib.error.HTTPError as e:
        if b"not authorized" in e.read():
            sys.exit("\nMISMATCH. Supabase is holding a DIFFERENT secret than poll-secret.js.\n"
                     "Every run of this script mints a NEW secret, so the SQL line it printed must\n"
                     "be pasted from the SAME run that wrote poll-secret.js.\n"
                     "Fix: run this script again and paste the SQL line it prints.")
        raise
    print("\n  Supabase accepts this secret. Open/close voting will work.\n")


def main():
    print(__doc__.split("\n\n")[1].replace("\n", " "), "\n")
    p1 = unquote(getpass.getpass("CCGate passphrase (same as poll-admin): ").strip())
    if not p1:
        sys.exit("No passphrase given.")
    p2 = unquote(getpass.getpass("Again, to be sure: ").strip())
    if p1 != p2:
        sys.exit("They do not match. Nothing was written.")

    # Prove it is the RIGHT passphrase before writing anything.
    # It must be the one that already unlocks class-console, or the browser
    # will never be able to decrypt what we are about to write -- and the
    # failure would be silent and, on a projector, invisible.
    check(p1)

    # The Supabase-side secret. Random, machine-only, never typed by a human.
    poll_secret = secrets.token_urlsafe(32)

    salt, iv = os.urandom(16), os.urandom(12)
    key = hashlib.pbkdf2_hmac("sha256", p1.encode(), salt, ITER, dklen=32)
    ct = AESGCM(key).encrypt(iv, json.dumps({"poll_secret": poll_secret}).encode(), None)
    payload = {"salt": B(salt), "iv": B(iv), "ct": B(ct), "iter": ITER}

    out = ("/* Generated by make-poll-secret.py -- do not hand-edit.\n"
           " * The Supabase poll secret, encrypted under the shared instructor\n"
           " * passphrase (PBKDF2-SHA256 %d -> AES-GCM), same scheme as the\n"
           " * class-console and poll-admin payloads. Safe to publish.\n"
           " */\n"
           "window.POLL_SECRET_PAYLOAD = %s;\n") % (ITER, json.dumps(payload))

    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "poll-secret.js")
    with open(path, "w") as f:
        f.write(out)

    # Also drop the SQL in a file. Printing it alone has now twice ended with it
    # scrolling away unpasted, which leaves poll-secret.js and poll_secrets holding
    # secrets from different runs -- a mismatch whose only symptom is silence.
    sqlp = os.path.join(os.path.dirname(os.path.abspath(__file__)), "poll-secret.sql")
    with open(sqlp, "w") as f:
        f.write("-- Paste into the Supabase SQL editor and press Run.\n"
                "-- Pairs with the poll-secret.js written in the SAME run; regenerate both together.\n"
                "-- Gitignored: this file holds the live secret in plaintext. Delete it once pasted.\n"
                "insert into public.poll_secrets (k, v)\n"
                "values ('instructor', '%s')\n"
                "on conflict (k) do update set v = excluded.v;\n" % poll_secret)

    print("\nWrote", path)
    print("Wrote", sqlp, "(gitignored -- delete it once pasted)")
    print("\n" + "=" * 72)
    print("PASTE THIS ONE LINE INTO THE SUPABASE SQL EDITOR, THEN PRESS RUN:")
    print("=" * 72)
    print("insert into public.poll_secrets (k, v)")
    print("values ('instructor', '%s')" % poll_secret)
    print("on conflict (k) do update set v = excluded.v;")
    print("=" * 72)
    print("\nThen, in order:")
    print("  1. paste the SQL above (or the contents of poll-secret.sql) into Supabase")
    print("  2. git add poll-secret.js && git commit -m 'new poll secret' && git push")
    print("  3. python3 make-poll-secret.py --check     <- confirms the two now agree")
    print("Do not paste the line above into a chat -- it is the live secret.\n")

if __name__ == "__main__":
    if "--check" in sys.argv:
        verify()
    else:
        main()
