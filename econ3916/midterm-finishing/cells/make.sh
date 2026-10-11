#!/bin/sh
# Rebuild the deck from the snippets. Every number on a slide comes out of midterm.out.json.
set -e
cd "$(dirname "$0")"
PY=~/econ-recording/colabenv/bin/python          # Colab's library versions
TOOLS="$HOME/Resilio Sync/documents/econ-lecture-material/TA/teaching-improvement/tools"
$PY make_data.py                                  # data/*.csv, fixed seed
$PY ~/econ-recording/py101-b5/run_snippets.py midterm.py > /dev/null   # -> midterm.out.json
python3 build_deck.py                             # -> ../index.html
python3 "$TOOLS/notes_speaker_view.py" --check ../index.html   # every note already in speaker-view form
python3 build_deck.py --term                      # THIS TERM line, first in its note
cp ../index.html ../presentation.html
# third copy: the authoring folder (feedback_deck_three_copies)
AUTH="$HOME/Resilio Sync/documents/econ-lecture-material/econ3916-applied-data-analytics/midterm-econ3916-finishing"
mkdir -p "$AUTH/figures"
cp ../index.html "$AUTH/presentation.html"
cp ../styles.css "$AUTH/styles.css"
cp ../figures/*.png "$AUTH/figures/"
md5 -q ../index.html ../presentation.html "$AUTH/presentation.html" | sort -u | wc -l | awk '{ if ($1 != 1) { print "THREE COPIES DIFFER"; exit 1 } else print "three copies identical" }'
