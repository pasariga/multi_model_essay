"""Detect common accidental credential commits without printing matching values.

This repository hygiene check is not a comprehensive secret scanner.
It reads tracked files only and makes no network requests.
"""
from pathlib import Path
import re
import subprocess
import sys


def main() -> int:
    tracked = subprocess.check_output(["git", "ls-files", "-z"]).decode().split("\0")
    patterns = (
        re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH |DSA |ENCRYPTED )?PRIVATE KEY-----"),
        re.compile(rb"\bgh[pousr]_[A-Za-z0-9]{36,}\b"),
        re.compile(rb"\bgithub_pat_[A-Za-z0-9_]{60,}\b"),
        re.compile(rb"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    )
    failures = []
    for name in filter(None, tracked):
        path = Path(name)
        example = path.name.endswith((".example", ".sample", ".template"))
        forbidden_path = (
            (not example and (path.name == ".env" or path.name.endswith(".env") or path.name.startswith(".env.")))
            or path.suffix.lower() in {".pem", ".key", ".p12", ".pfx"}
            or ".ssh" in path.parts
            or name.endswith(".aws/credentials")
        )
        if forbidden_path:
            failures.append((name, "credential-like file path"))
            continue
        if not path.is_file() or path.stat().st_size > 2_000_000:
            continue
        content = path.read_bytes()
        if b"\0" not in content and any(pattern.search(content) for pattern in patterns):
            failures.append((name, "credential-like content; value withheld"))
    for name, reason in failures:
        print(f"FAIL: {name}: {reason}")
    if failures:
        print("Remove the credential from the commit; rotate it if it was real.")
        return 1
    print(f"Repository hygiene passed for {len(list(filter(None, tracked)))} tracked files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
