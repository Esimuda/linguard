#!/usr/bin/env python3
"""Thin wrapper: score a trials JSONL."""
from pidginguard.__main__ import main
import sys

if __name__ == "__main__":
    raise SystemExit(main(["eval", *sys.argv[1:]]))
