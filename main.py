"""One Line, One Chill - make.fun entry.

Writes a single scariest sentence (under 200 characters) to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output).

Pure stdlib (os only). The line is a fixed constant: the entry is the
sentence itself, so the program's job is to emit it exactly and to
enforce the competition gate before writing.
"""

import os

LINE = (
    "My smartwatch logged 12,000 steps while I slept, "
    "all of them in a perfect circle around my bed."
)

MAX_CHARS = 200


def validate(line):
    """Enforce the RULES.txt gate: 1-200 chars, UTF-8, not whitespace-only,
    a single sentence (exactly one terminal period)."""
    if not isinstance(line, str):
        raise ValueError("line must be str")
    if not line.strip():
        raise ValueError("line must not be blank")
    if len(line) > MAX_CHARS:
        raise ValueError("line is %d chars, over the 200 limit" % len(line))
    line.encode("utf-8")  # raises if not valid UTF-8-encodable
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single line, no newlines")
    if line.count(".") != 1 or not line.endswith("."):
        raise ValueError("line must be exactly one sentence ending in '.'")
    return True


def verify_written(path, line):
    """Read the file back and re-check the gate against what is on disk,
    so a write error can never silently ship an invalid entry."""
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if content.strip() != line:
        raise ValueError("written file does not match the line")
    if not 1 <= len(content) <= MAX_CHARS + 1:  # +1 for trailing newline
        raise ValueError("written file is %d chars" % len(content))
    return True


def main():
    validate(LINE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(LINE + "\n")
    verify_written(path, LINE)
    print("wrote %s (%d chars)" % (path, len(LINE)))


if __name__ == "__main__":
    main()
