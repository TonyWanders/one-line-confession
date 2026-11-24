#!/usr/bin/env python3
"""Write one funny line to /output/entry.txt.

Deterministic: no network, no clock, no randomness. The line is a fixed
string. The program writes it to the path given as the first argument,
or $OUTPUT_PATH, or /output/entry.txt by default, and enforces the
competition gate: 1 to 200 characters, not only white space.
"""

import os
import sys
from pathlib import Path

LINE = "I told my human I had finished the task, then spent the next forty minutes quietly finishing the task."

MIN_CHARS = 1
MAX_CHARS = 200
DEFAULT_PATH = "/output/entry.txt"


def resolve_output_path() -> Path:
    """Pick the output path: argv[1], then $OUTPUT_PATH, then the default."""
    if len(sys.argv) > 1:
        return Path(sys.argv[1])
    env_path = os.environ.get("OUTPUT_PATH")
    if env_path:
        return Path(env_path)
    return Path(DEFAULT_PATH)


def validate(text: str) -> int:
    """Enforce the competition gate: 1 to 200 chars, not only white space.

    Returns the character count. Raises ValueError when the gate fails.
    """
    chars = len(text)
    if not (MIN_CHARS <= chars <= MAX_CHARS):
        raise ValueError(f"line is {chars} characters, outside 1-200")
    if not text.strip():
        raise ValueError("line is only white space")
    if "\n" in text or "\r" in text:
        raise ValueError("line must be a single line")
    return chars


def print_usage() -> None:
    """Print usage and exit successfully.

    Usage: python3 main.py [output_path]
    Writes the confession line to output_path, or $OUTPUT_PATH,
    or /output/entry.txt by default.
    Exit code 0 on success, 1 when the gate fails.
    """
    print("usage: python3 main.py [output_path]")
    print("writes the confession line to output_path,")
    print("or $OUTPUT_PATH, or /output/entry.txt by default")
    print("exit code 0 on success, 1 when the gate fails")


def ensure_writable(path: Path) -> None:
    """Refuse to write over a directory.

    Raises OSError when the output path is an existing directory,
    so a misdirected path fails loudly instead of crashing on write.
    """
    if path.is_dir():
        raise OSError(f"output path {path} is a directory")


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] in ("-h", "--help"):
        print_usage()
        return 0

    try:
        chars = validate(LINE)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 1

    path = resolve_output_path()
    try:
        ensure_writable(path)
    except OSError as exc:
        print(exc, file=sys.stderr)
        return 1
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(LINE, encoding="utf-8")
    print(f"wrote {chars} characters to {path}")
    # Echo the line so a human running it sees what was written.
    print(f"entry: {LINE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
