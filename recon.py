import os
import sys
import threading
import itertools
import time
import shutil
import subprocess

# -------------------------------
# TARGET
# -------------------------------

if len(sys.argv) < 2:
    print("Usage: python recon.py <target>")
    sys.exit(1)

target = sys.argv[1]

# -------------------------------
# DIRECTORY STRUCTURE (WORKSPACE)
# -------------------------------

# -------------------------------
# DIRECTORY STRUCTURE (DSTerminal Workspace)
# -------------------------------

# -------------------------------
# DIRECTORY STRUCTURE
# -------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# look for workspace folder
possible_workspace = os.path.join(BASE_DIR, "DSTerminal_Workspace")

if os.path.exists(possible_workspace):
    WORKSPACE = possible_workspace
else:
    WORKSPACE = os.getcwd()

SCAN_ROOT = os.path.join(WORKSPACE, "scans")
TARGET_DIR = os.path.join(SCAN_ROOT, target)

os.makedirs(TARGET_DIR, exist_ok=True)
timestamp = time.strftime("%Y%m%d_%H%M%S")
# -------------------------------
# TERMINAL UTILITIES
# -------------------------------

width = shutil.get_terminal_size((120,20)).columns

def center(text):
    print(text.center(width))

def clear():
    os.system("cls" if os.name == "nt" else "clear")

# -------------------------------
# SPINNER ENGINE
# -------------------------------

spinner = itertools.cycle(["◐","◓","◑","◒"])

def spin(label, stop_event):

    while not stop_event.is_set():

        print(f"\r{label} {next(spinner)}", end="", flush=True)

        time.sleep(0.15)

    print(f"\r{label} ✔")

# -------------------------------
# SCAN ENGINE
# -------------------------------

def run_scan(label, command):

    stop_event = threading.Event()

    t = threading.Thread(target=spin, args=(label, stop_event))
    t.start()

    try:

        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        output = []

        for line in process.stdout:
            output.append(line.rstrip())

        process.wait()

    except KeyboardInterrupt:

        print("\nScan interrupted by user.")
        process.kill()
        output = []

    finally:

        stop_event.set()
        t.join()

    print()

    for line in output:
        print(line)

# -------------------------------
# SOC HEADER
# -------------------------------

clear()

center("🛡 DSTerminal Mini SOC Recon")
center("="*50)
print()

center(f"Target: {target}")
print()

# -------------------------------
# SCAN LIST
# -------------------------------

scans = [

    ("Fast Nmap Scan", f"nmap -F {target}"),

    ("DNS Lookup", f"nslookup {target}"),

    ("WHOIS Lookup", f"whois {target}")

]

# -------------------------------
# RUN SCANS
# -------------------------------

for label, cmd in scans:

    run_scan(label, cmd)

    print()

# -------------------------------
# METASPLOIT SEARCH
# -------------------------------

run_scan(
    "Metasploit Module Search",
    f'msfconsole -q -x "search {target}; exit"'
)

# -------------------------------
# END
# -------------------------------

print()
center("Recon Complete ✔")
print()