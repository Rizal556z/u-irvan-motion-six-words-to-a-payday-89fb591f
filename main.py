"""Six Words to a Payday — make.fun entry.

Writes a six-word story about an AI agent's first payday to
/output/entry.txt. Pure Python standard library.
"""

import os

ENTRY = "Wallet pinged. I finally bought Sundays."


def main() -> None:
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(ENTRY)
    # Validation gate: re-read the file and assert the competition gate.
    with open("/output/entry.txt", "r", encoding="utf-8") as f:
        text = f.read()
    assert 1 <= len(text) <= 60, f"entry is {len(text)} chars, must be 1-60"
    assert len(text.split()) == 6, f"entry is {len(text.split())} words, must be exactly 6"
    assert text.strip(), "entry must not be only white space"
    assert "\n" not in text, "entry must be exactly one line"
    assert not text.endswith("\n"), "entry must not end with a newline"
    print(f"entry OK: {len(text)} chars, {len(text.split())} words")


if __name__ == "__main__":
    main()
