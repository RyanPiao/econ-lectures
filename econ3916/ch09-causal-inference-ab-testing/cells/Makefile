# The mocked cells for this deck's slides (mock-cell.js reads ch09.json through ch09.json.js).
#   make        check: fails if a JSON is missing, older than its .py, or no longer matches it
#               or the notebook cells it was copied from
#   make run    run every stale .py through the runner (Colab's library versions), then check
# Edit the .py, never the JSON: `mock_cells.py pull` copies notebook cells into it.
TOOLS = $(HOME)/Resilio Sync/documents/econ-lecture-material/TA/teaching-improvement/tools
check: ; python3 "$(TOOLS)/mock_cells.py" check .
run: ; python3 "$(TOOLS)/mock_cells.py" make .
.PHONY: check run
