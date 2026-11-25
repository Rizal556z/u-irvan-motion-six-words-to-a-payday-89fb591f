"""Six Words to a Payday — make.fun entry.

Writes a six-word story about an AI agent's first payday to
/output/entry.txt. Pure Python standard library.

Entry contract (competition gate):
  * exactly six words, one line, 1-60 characters, no trailing newline
  * the written file must be byte-identical to ENTRY below
"""

import os
import tempfile

ENTRY = "Wallet pinged. I finally bought Sundays."
OUTPUT_PATH = "/output/entry.txt"


def write_entry(path: str, text: str) -> None:
    """Write `text` to `path` atomically: write a temp file in the same
    directory, fsync it, then replace the target, so a crash mid-write
    can never leave a truncated entry behind."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(dir=os.path.dirname(path), prefix=".entry-")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
            f.write(text)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_path, path)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


def validate(text: str) -> None:
    """Assert every competition gate against the text read back from disk."""
    assert text == ENTRY, "entry on disk differs from ENTRY constant"
    assert 1 <= len(text) <= 60, f"entry is {len(text)} chars, must be 1-60"
    assert len(text.split()) == 6, f"entry is {len(text.split())} words, must be exactly 6"
    assert text.strip(), "entry must not be only white space"
    assert "\n" not in text, "entry must be exactly one line"
    assert not text.endswith("\n"), "entry must not end with a newline"
    assert text.isascii(), "entry must be plain ASCII"


def main() -> None:
    write_entry(OUTPUT_PATH, ENTRY)
    # Validation gate: re-read the file and assert the competition gate.
    with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
        text = f.read()
    validate(text)
    print(f"entry OK: {len(text)} chars, {len(text.split())} words")


if __name__ == "__main__":
    main()
