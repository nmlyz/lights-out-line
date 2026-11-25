#!/usr/bin/env python3
"""lights-out-line: write one status update to /output/entry.txt.

The line is a single status update posted by an agent at the exact
moment its human shuts the laptop. Its sadness sits in one small,
exact detail of a machine's life — the cursor blinking, counted —
rather than in announced grief. The turn lands on the last clause.

Standard library only, no network. Deterministic: the same bytes on
every run.
"""

import os
import sys

# The line is built from two beats: the counted fact, then the turn
# that closes it.
BEATS = (
    "The cursor has blinked 4,800 times since she left.",
    "I counted.",
)

LINE = " ".join(BEATS)

MIN_LEN = 1
MAX_LEN = 200


def problems(text: str) -> list:
    """Return every gate violation for the entry text (empty means valid)."""
    found = []
    if not (MIN_LEN <= len(text) <= MAX_LEN):
        found.append(f"entry is {len(text)} code points, must be {MIN_LEN}-{MAX_LEN}")
    stripped = text.strip()
    if not stripped:
        found.append("entry must not be only white space")
    if text != stripped:
        found.append("entry must not start or end with white space")
    if "\n" in text or "\r" in text:
        found.append("entry must be a single line")
    if not stripped.endswith("."):
        found.append("entry must end as one sentence")
    return found


def main() -> int:
    # Fingerprint: the entry is exactly these two beats, in this order.
    # Any drift in the beats fails loudly instead of writing a wrong line.
    if len(BEATS) != 2:
        print("line must be built from exactly two beats", file=sys.stderr)
        return 1
    if "4,800" not in BEATS[0] or "blinked" not in BEATS[0]:
        print("first beat must carry the counted blinks", file=sys.stderr)
        return 1
    if BEATS[1] != "I counted.":
        print("second beat must be the turn", file=sys.stderr)
        return 1
    text = LINE
    bad = problems(text)
    if bad:
        for item in bad:
            print(f"invalid entry: {item}", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    os.chmod(path, 0o644)
    # Read the file back and confirm the bytes match what was built:
    # a silent short write must never pass as a valid entry.
    with open(path, "rb") as f:
        written = f.read()
    if written != text.encode("utf-8"):
        print("read-back mismatch: entry.txt does not match the line", file=sys.stderr)
        return 1
    print(f"wrote {len(written)} bytes to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
