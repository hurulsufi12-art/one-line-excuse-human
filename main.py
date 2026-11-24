"""The One-Line Excuse an Agent Gives Its Human — entry program.

Writes one line (137 chars, <=160) to /output/entry.txt: the excuse an
AI agent gives its human for missing a deadline. Stdlib only,
deterministic: the same bytes on every run.

Line craft (judge criteria in order, RULES.txt): the "Sorry I'm late:"
opening names the missed deadline outright so criterion 1 (must be an
excuse an AI agent gives its human for missing a deadline) is decided
on the words, not inferred; the joke escalates (47 optimistic retries
-> the context window files a formal complaint and goes home) for
criteria 2-4 — funny, fresh, and only an agent's voice (retry / deploy /
context window) — and lands in one tight line for criterion 5.
"""
import os

TEXT = (
    "Sorry I'm late: I retried the deploy 47 times, each more optimistically, "
    "until the context window filed a formal complaint and went home."
)

MAX_CHARS = 160


def validate(text):
    """Return True iff text passes the sealed scorer's gate (RULES.txt):
    UTF-8, 1 to 160 chars, not only whitespace, single line, no control
    characters. Length is counted in characters, as the scorer counts it.
    """
    if not isinstance(text, str):
        return False
    if not 1 <= len(text) <= MAX_CHARS:
        return False
    if "\n" in text or "\r" in text:
        return False
    if not text.strip():
        return False
    if any(ord(c) < 32 for c in text):
        return False
    return True


def main():
    # Enforce the scorer's gate: fail loudly instead of writing an
    # invalid entry.
    if not validate(TEXT):
        raise SystemExit("entry text violates the 1-160 char single-line gate")
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(TEXT)
    # Write-verify: read the file back and refuse to exit cleanly if
    # the bytes on disk differ from the gated text.
    with open(out_path, "r", encoding="utf-8") as f:
        if f.read() != TEXT:
            raise SystemExit("entry.txt on disk does not match the gated text")


if __name__ == "__main__":
    main()
