#!/usr/bin/python3
# INET4031 — create-users2.py
# Dry-run support: Y = simulate (print would-run + errors/skips), N = execute (no extra messages).

import os, re, sys

def run(cmd: str, dry: bool):
    if dry:
        print(f"[DRY-RUN] would run: {cmd}")
    else:
        os.system(cmd)

def main():
    # Ask once at start
    ans = input("Dry-run? (Y/N): ").strip().lower()
    dry = (ans == 'y')

    for raw in sys.stdin:
        line = raw.rstrip("\n")

        # Skip blank lines fast
        if not line.strip():
            if dry:
                print("[DRY-RUN] skipped blank line")
            continue

        # Commented/skip lines start with '#'
        if re.match(r"^#", line):
            if dry:
                print(f"[DRY-RUN] skipped commented line: {line}")
            continue

        fields = line.strip().split(':')

        # Expect exactly 5 fields: username:password:last:first:groups
        if len(fields) != 5:
            if dry:
                print(f"[DRY-RUN][ERROR] bad field count ({len(fields)}): {line}")
            # In normal mode, silently skip bad input
            continue

        username = fields[0]
        password = fields[1]
        last = fields[2]
        first = fields[3]
        groups = fields[4].split(',')

        # '-' means no supplemental groups
        groups = [] if len(groups) == 1 and groups[0] == '-' else groups

        # Build GECOS "First Last,,,"
        gecos = f"{first} {last},,,"

        print(f"==> Creating account for {username}...")
        cmd = f"/usr/bin/sudo /usr/sbin/adduser --disabled-password --gecos '{gecos}' {username}"
        run(cmd, dry)

        print(f"==> Setting the password for {username}...")
        cmd = f"/bin/echo -ne '{password}\\n{password}' | /usr/bin/sudo /usr/bin/passwd {username}"
        run(cmd, dry)

        for g in groups:
            print(f"==> Assigning {username} to the {g} group...")
            cmd = f"/usr/bin/sudo /usr/sbin/adduser {username} {g}"
            run(cmd, dry)

if __name__ == "__main__":
    main()

