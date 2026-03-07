import os
from turtle import color
# ===============================
# Cross-platform terminal support
# ===============================
IS_WINDOWS = os.name == "nt"

if IS_WINDOWS:
    import msvcrt
else:
    import tty
    import termios

import sys
import math
import shlex
import shutil
import socket
import netifaces
from getpass import getpass
import requests
import base64
import hashlib
import logging
import psutil
from tqdm import tqdm
import threading
import textwrap
import platform
import json
import time
import random
import ssl
import OpenSSL
import subprocess
import argparse
from cryptography.x509 import load_pem_x509_certificate
from cryptography.x509.ocsp import OCSPRequestBuilder
from threading import Thread, Event
from datetime import datetime, timedelta
from cryptography.fernet import Fernet

from prompt_toolkit import PromptSession, HTML
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.formatted_text import HTML
from colorama import Fore, Style, init
# from pyfiglet import figlet_format
from pyfiglet import figlet_format
import itertools
from rich.console import Console, Group
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.live import Live
from collections import Counter

from rich.console import Console
from rich.layout import Layout
from rich.table import Table as Table
from random import choice
from rich.prompt import Prompt
# from rich.group import Group
from shutil import which
from rich.columns import Columns
from edu_typing_engine import EducationTypingEngine
from cryptography.hazmat.primitives import serialization
import cryptography

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle,
    PageBreak
)
from reportlab.lib.colors import black, lightgrey, HexColor

init(autoreset=True)

engine = EducationTypingEngine(speed=0.03)

def init_workspace():
    workspace_path = os.path.expanduser("~/dsterminal_workspace")
    subdirs = ["sandbox", "scans", "exploits", "reports"]
    
    try:
        os.makedirs(workspace_path, exist_ok=True)
        for subdir in subdirs:
            os.makedirs(os.path.join(workspace_path, subdir), exist_ok=True)
        # print(f"{Fore.GREEN}[+] Workspace initialized at: {workspace_path}{Style.RESET_ALL}")
        # return workspace_path
    except Exception as e:
        print(f"{Fore.RED}[!] Failed to initialize workspace: {e}{Style.RESET_ALL}")
        sys.exit(1) 
# Initialize workspace safely
WORKSPACE = init_workspace()
console = Console()

# Configuration
CONFIG = {
    'VT_API_KEY': '957166d424812a397e328022b84594a8c02757814f6c04518dce7e81179b4b79',
    'UPDATE_URL': 'https://github.com/Stark-Expo-Tech-Exchange/DSTerminal_releases_latest.git',
    'LOG_FILE': 'secure_audit.log',
    'ENCRYPT_KEY': Fernet.generate_key().decode(),
    'CURRENT_VERSION': '2.0.59'
}
# Add this near CONFIG or __init__
EDUCATION_TIPS = {
    "system scan -all": """
    [bold]💡 Did You Know?[/bold]\n
    Regular system scans help detect malware persistence mechanisms like:\n
    - [red]Rootkits[/red] hiding in kernel modules\n
    - [yellow]Malicious scheduled tasks[/yellow] (check `crontab -l` or Task Scheduler)\n
    - [blue]Unusual network listeners[/blue] (`netstat -tulnp`)\n
    """,
    "net -n mon": """
    [bold]🔍 Network Monitoring Tip[/bold]\n
    Monitor for:\n
    1. [red]Unexpected outbound connections[/red] (could indicate data exfiltration)\n
    2. Ports in `LISTEN` state that shouldn't be open\n
    3. Use tools like [green]Wireshark[/green] for deep packet inspection.\n
    """,
    "harden -t sys": """
    [bold]🛡️ Hardening Pro Tip[/bold]\n
    Always follow the [yellow]Principle of Least Privilege[/yellow]:\n
    - Disable unnecessary services\n
    - Apply OS-specific benchmarks (e.g., [blue]CIS Benchmarks[/blue])\n
    - Use [green]SELinux/AppArmor[/green] for mandatory access control.\n
    """,
    "exploitcheck": """
    [bold]🔍 Exploit Check Tip[/bold]\n
    Checks for common vulnerabilities like:\n
    - [red]Unpatched CVEs[/red] (check with `cve-search`)\n
    - [yellow]Misconfigured services[/yellow] (SSH, FTP, SMB)\n
    - [blue]Kernel exploits[/blue] (DirtyPipe, DirtyCow)\n
    [green]Pro Tip:[/green] Cross-reference with exploit-db.com\n
    [bold]🧠 Exploit Check Insight[/bold]\n
    - Regularly scan for known vulnerabilities (CVEs).\n
    - Tools like [cyan]searchsploit[/cyan], [magenta]exploitdb[/magenta], and vulnerability scanners (Nessus, OpenVAS) are critical.
    """,
    
    "macspoof": """
    [bold]📡 MAC Spoofing Tip[/bold]\n
    Remember:\n
    1. Spoofing only works until [red]next reboot[/red]\n
    2. For persistence, modify [yellow]/etc/network/interfaces[/yellow]\n
    3. Some networks use [blue]MAC filtering[/blue] (check ARP tables)\n
    [green]Example:[/green] macspoof wlan0\n
    [bold]🎭 MAC Spoofing Caution[/bold]\n
    - Changing MAC addresses can evade network tracking but might disrupt connections.\n
    - Always reset your original MAC for stability.
    """,
    
    "clearlogs": """
    [bold]🧹 Log Cleaning Tip[/bold]\n
    Targets common log locations:\n
    - [red]/var/log/[/red] (syslog, auth.log)\n
    - [yellow]~/.bash_history[/yellow]\n
    - [blue]Journald[/blue] (`journalctl --vacuum-time=1s`)\n
    [green]Warning:[/green] Some systems use remote logging!\n
    Clearing logs should be used ethically. Logs are vital for:\n
    - Forensics
    - Intrusion Detection
    - Compliance Audits
    
    """,
    
    "portsweep": """
    [bold]🔎 Port Scanning Tip[/bold]\n
    Advanced techniques:\n
    - [red]SYN stealth scan[/red] (-sS)\n
    - [yellow]Service version detection[/yellow] (-sV)\n
    - [blue]OS fingerprinting[/blue] (-O)\n
    [green]Pro Tip:[/green] Use `-T4` for faster scans (noisy)\n
    : Port sweeps reveal exposed services.\n
    - Scan with `-sS`, `-sV`, `-sT`, `-sS`, `-sV`, `-Pn`, `-p`, `-T4` flags in [green]nmap[/green] for stealth and version detection.
    
    """,
    
    "hashfile": """
    [bold]🔐 Hashing Tip[/bold]\n
    Why multiple hashes matter:\n
    - [red]MD5[/red] - Fast but broken\n
    - [yellow]SHA1[/yellow] - Deprecated but common\n
    - [blue]SHA256[/blue] - Current standard\n
    [green]Pro Tip:[/green] Verify against VirusTotal hashes\n
    : Use SHA-256 for strong integrity checks.\n
    Example: `sha256sum file.txt`
    """,
    
    "sysinfo": """
    [bold]🖥️ System Recon Tip[/bold]\n
    Critical info to check:\n
    - [red]Kernel version[/red] (uname -a)\n
    - [yellow]CPU flags[/yellow] (/proc/cpuinfo)\n
    - [blue]Sudo version[/blue] (CVE-2021-3156)\n
    [green]Pro Tip:[/green] Check `lshw` for full hardware details\n
    """,
    
    "killproc": """
    [bold]💀 Process Killing Tip[/bold]\n
    Advanced methods:\n
    - [red]SIGKILL[/red] (-9) for stubborn processes\n
    - [yellow]pkill[/yellow] for name-based termination\n
    - [blue]killall[/blue] for all instances\n
    [green]Warning:[/green] Can cause data loss!\n
    """,
    
    "check integrity": """
    [bold]🛡️ Integrity Check Tip[/bold]\n
    Checks for:\n
    - [red]Modified system binaries[/red] (ls, ps, netstat)\n
    - [yellow]Unexpected setuid files[/yellow] (find / -perm -4000)\n
    - [blue]Hidden kernel modules[/blue] (lsmod)\n
    [green]Pro Tip:[/green] Compare against package manager (`rpm -V`)\n
    """,
    
    "encrypt": """
    [bold]🔒 Encryption Tip[/bold]\n
    Best practices:\n
    - Use [red]strong passwords[/red] (12+ chars, special symbols)\n
    - Consider [yellow]GPG[/yellow] for asymmetric encryption\n
    - [blue]Shred[/blue] original files after encryption\n
    [green]Example:[/green] encrypt secret.docx\n
    """,
    
    "decrypt": """
    [bold]🔓 Decryption Tip[/bold]\n
    Key management:\n
    - Store keys in [red]separate secure location[/red]\n
    - Use [yellow]key derivation functions[/yellow] (PBKDF2)\n
    - Consider [blue]hardware tokens[/blue] for critical keys\n
    [green]Syntax:[/green] decrypt file.enc myStrongPassword123!\n
    """,
    
    "watchfolder": """
    [bold]👀 Folder Monitoring Tip[/bold]\n
    Detects:\n
    - [red]New files[/red] (ransomware indicators)\n
    - [yellow]Permission changes[/yellow] (chmod/chown)\n
    - [blue]Hidden files[/blue] (dotfiles, double extensions)\n
    [green]Pro Tip:[/green] Monitor /tmp and /dev/shm\n
    """,
    
    "traceroute": """
    [bold]🌐 Network Tracing Tip[/bold]\n
    Advanced options:\n
    - [red]TCP SYN[/red] probes (-T)\n
    - [yellow]ICMP[/yellow] echo (-I)\n
    - [blue]DNS lookups[/blue] (-n to disable)\n
    [green]Pro Tip:[/green] Use mtr for continuous monitoring\n
    """,
    
    "ransomwatch": """
    [bold]💰 Ransomware Tip[/bold]\n
    Detection signs:\n
    - [red]Mass file renames[/red] (.enc, .locked)\n
    - [yellow]Unusual process[/yellow] (encryption patterns)\n
    - [blue]Bitcoin wallet[/blue] creation attempts\n
    [green]Pro Tip:[/green] Monitor /home and network shares\n
    """,
    
    "wificrack": """
    [bold]📶 WiFi Auditing Tip[/bold]\n
    Common attacks:\n
    - [red]WPA2 handshake[/red] capture\n
    - [yellow]Evil Twin[/yellow] access points\n
    - [blue]KRACK[/blue] vulnerability tests\n
    [green]Requires:[/green] Monitor mode capable adapter\n
    """,
    
    "stegcheck": """
    [bold]🖼️ Steganography Awareness & Forensics Tip[/bold]\n
    Steganography is the practice of hiding information inside seemingly normal files
    such as images, audio, or video. It is often used to bypass security controls.\n

    [bold]Common Indicators of Hidden Data:[/bold]\n
    - Unusually large file size for the image resolution
    - High entropy (random-looking data)
    - Inconsistent or missing EXIF metadata
    - Suspicious color-channel patterns\n

    [bold]Detection & Analysis Methods:[/bold]\n
    - [red]Binwalk[/red]: Identify embedded files or appended data
    - [yellow]Stegdetect[/yellow]: Detect signatures of known steganography tools
    - [blue]LSB Analysis[/blue]: Examine least-significant-bit manipulation
    - [cyan]Entropy Analysis[/cyan]: Identify abnormal randomness levels\n

    [bold]Real-World Use Cases:[/bold]\n
    - Malware command-and-control via images
    - Hidden financial instructions in invoices or screenshots
    - Covert data exfiltration over messaging platforms
    - Digital evidence analysis in cybercrime investigations.\n

    [bold][green]Pro Tip:[/green][/bold]\n
    Always inspect EXIF metadata and file structure before deep analysis.
    Detection should remain non-invasive unless authorized forensic procedures apply.\n

    [bold]Ethical Reminder:[/bold]\n
    Steganalysis should only be performed for defensive, investigative,
    or educational purposes with proper authorization.\n
    """,

    "certcheck": """
    [bold]🔖 SSL Cert Tip[/bold]\n
    Critical checks:\n
    - [red]Expiration date[/red]\n
    - [yellow]Weak algorithms[/yellow] (SHA1, RC4)\n
    - [blue]SAN mismatches[/blue]\n
    [green]Pro Tip:[/green] Test with testssl.sh\n
    """,
    
    "memdump": """
    [bold]🧠 Memory Forensics Tip[/bold]\n
    What to look for:\n
    - [red]Process memory[/red] (passwords, keys)\n
    - [yellow]Network connections[/yellow] (raw sockets)\n
    - [blue]Malicious implants[/blue] (shellcode)\n
    [green]Tool:[/green] Analyze with Volatility\n
    """,
    
    "torify": """
    [bold]🧅 Tor Networking Tip[/bold]\n
    Important notes:\n
    - [red]Not 100% anonymous[/red] (exit node risks)\n
    - [yellow]DNS leaks[/yellow] still possible\n
    - [blue]Bridge nodes[/blue] for censored networks\n
    [green]Pro Tip:[/green] Combine with VPN (Tor-over-VPN)\n
    """,
    
    "update": """
    [bold cyan]🔄 DSTERMINAL SECURITY UPDATE PROTOCOL[/bold cyan]

    [bold underline]WHY SYSTEMATIC UPDATES ARE NON-NEGOTIABLE FOR SECURITY TOOLS[/bold underline]

    As a defensive security platform, DSTerminal occupies a privileged position within your infrastructure. 
    Its capabilities—from network reconnaissance to forensic analysis—require constant evolution to counter 
    the rapidly advancing threat landscape. Each update represents not just new features, but essential 
    adaptations to emerging attack methodologies.

    [underline]CRITICAL SECURITY IMPERATIVES ADDRESSED THROUGH UPDATES[/underline]

    [bold red]ZERO-DAY & N-DAY VULNERABILITY MITIGATION[/bold red]
    • [white]▸ Preemptive Patch Deployment[/white] – Closing security gaps before widespread exploitation
    • [yellow]▸ CVE-Responsive Updates[/yellow] – Direct responses to published advisories affecting scanning engines
    • [red]▸ Memory Corruption Protections[/red] – Enhanced buffer overflow and code injection defenses
    • [magenta]▸ Sandbox Escape Prevention[/magenta] – Hardening against container/VM breakout techniques

    [bold yellow]PRIVILEGE & ACCESS CONTROL REINFORCEMENT[/bold yellow]
    • [white]▸ Least Privilege Enforcement[/white] – Tighter restrictions on DSTerminal's own system access
    • [cyan]▸ Credential Handling Security[/cyan] – Improved encryption for stored API keys and credentials  
    • [green]▸ SUID/SGID Vulnerability Remediation[/green] – Fixes for potential local privilege escalation vectors
    • [red]▸ Race Condition Elimination[/red] – Preventing TOCTOU (Time-of-Check-Time-of-Use) vulnerabilities

    [bold blue]THREAT INTELLIGENCE & DETECTION ENHANCEMENT[/bold blue]
    • [white]▸ Real-Time Signature Updates[/white] – Integration of latest malware hashes and IOCs (Indicators of Compromise)
    • [yellow]▸ Behavioral Analysis Improvements[/yellow] – Enhanced heuristic detection for polymorphic malware
    • [cyan]▸ Attack Pattern Recognition[/cyan] – Updated MITRE ATT&CK framework mapping for detected activities
    • [green]▸ Threat Actor TTP Updates[/green] – Detection rules for emerging adversary tactics and procedures

    [bold magenta]CRYPTOGRAPHIC & COMMUNICATIONS SECURITY[/bold magenta]
    • [white]▸ TLS/SSL Implementation Updates[/white] – Protection against protocol-level vulnerabilities
    • [yellow]▸ Certificate Validation Enhancements[/yellow] – Improved PKI verification for API communications
    • [red]▸ Cryptographic Algorithm Rotation[/red] – Migration from deprecated to current standards
    • [cyan]▸ Secure Channel Reinforcement[/cyan] – Hardened connections to VirusTotal, threat feeds, and update servers

    [bold green]COMPLIANCE & GOVERNANCE REQUIREMENTS[/bold green]
    • [white]▸ Regulatory Framework Alignment[/white] – Updates for GDPR, HIPAA, PCI-DSS, NIST, ISO 27001 compliance
    • [yellow]▸ Audit Trail Enhancements[/yellow] – Improved logging for forensic reconstruction and compliance audits
    • [cyan]▸ Reporting Template Updates[/cyan] – Formats meeting current regulatory and executive briefing standards
    • [red]▸ Data Handling Improvements[/red] – Enhanced privacy protections for scanned data retention

    [bold underline]OPERATIONAL & FUNCTIONAL ENHANCEMENTS[/bold underline]

    [white]NETWORK DEFENSE CAPABILITIES[/white]
    • [cyan]▸ Protocol Analysis Updates[/cyan] – Detection for newer network protocols and encapsulated traffic
    • [yellow]▸ Evasion Technique Countermeasures[/yellow] – Detection of port knocking, tunneling, and protocol smuggling
    • [green]▸ IoT/OT Device Recognition[/green] – Expanded fingerprinting for industrial and embedded systems
    • [red]▸ Cloud Environment Adaptations[/red] – Scanning optimizations for AWS, Azure, GCP infrastructures

    [white]FORENSIC & INCIDENT RESPONSE IMPROVEMENTS[/white]
    • [yellow]▸ Memory Forensics Enhancements[/yellow] – Updated Volatility profiles and memory analysis techniques
    • [cyan]▸ Disk Imaging Compatibility[/cyan] – Support for newer filesystems and storage technologies
    • [green]▸ Timeline Analysis Upgrades[/green] – Improved event correlation and attack chain reconstruction
    • [red]▸ Anti-Forensics Detection[/red] – Identification of evidence tampering and artifact wiping

    [white]PERFORMANCE & SCALABILITY OPTIMIZATIONS[/white]
    • [cyan]▸ Parallel Processing Improvements[/cyan] – Faster large-scale network sweeps and distributed scanning
    • [yellow]▸ Resource Utilization Optimization[/yellow] – Reduced memory and CPU overhead during operations
    • [green]▸ Database Schema Updates[/green] – Enhanced storage efficiency for scan results and historical data
    • [red]▸ Cache Mechanism Refinements[/red] – Intelligent caching for frequently accessed threat intelligence

    [bold underline]RISK ASSESSMENT: CONSEQUENCES OF UPDATE NEGLECT[/bold underline]

    [red]IMMEDIATE THREATS[/red]
    • [white]Known Exploit Vulnerability[/white] – Attackers targeting published DSTerminal CVEs
    • [yellow]Detection Blind Spots[/yellow] – Failure to identify current malware variants
    • [cyan]False Negative Inflation[/cyan] – Missed compromise indicators due to outdated signatures
    • [magenta]Toolchain Exploitation[/magenta] – Using DSTerminal as an initial attack vector

    [red]STRATEGIC VULNERABILITIES[/red]
    • [white]Security Posture Degradation[/white] – Weakened defensive capabilities across monitored infrastructure
    • [yellow]Compliance Failures[/yellow] – Violations of mandatory security tool maintenance requirements
    • [cyan]Incident Response Impairment[/cyan] – Compromised forensic accuracy during security incidents
    • [magenta]Resource Inefficiency[/magenta] – Wasted time with false positives from outdated detection logic

    [bold underline]BEST PRACTICES FOR DSTERMINAL UPDATE MANAGEMENT[/bold underline]

    [green]FREQUENCY & SCHEDULING[/green]
    • [white]Weekly Update Checks[/white] – Minimum frequency for security tools in active environments
    • [yellow]Critical Update Immediate Application[/yellow] – Zero-day patches within 24 hours of release
    • [cyan]Change Window Coordination[/cyan] – Integration with organizational maintenance schedules
    • [red]Pre-Update Validation[/red] – Testing in isolated environments before production deployment

    [green]VERIFICATION & INTEGRITY CHECKS[/green]
    • [white]Digital Signature Validation[/white] – Confirming authenticity of all downloaded updates
    • [yellow]Hash Verification[/yellow] – SHA-256 checksum confirmation for update packages
    • [cyan]Source Authenticity[/cyan] – Ensuring updates originate from official GitHub repository
    • [red]Rollback Preparedness[/red] – Maintaining ability to revert problematic updates

    [green]EDUCATION & AWARENESS[/green]
    • [white]CVE Monitoring Subscriptions[/white] – Automatic alerts for DSTerminal-related vulnerabilities
    • [yellow]Change Log Review[/yellow] – Understanding security implications of each update
    • [cyan]Training Updates[/cyan] – Incorporating new features into security team workflows
    • [red]Vendor Communication[/red] – Reporting potential vulnerabilities discovered during use

    [bold underline]DSTERMINAL'S UPDATE ARCHITECTURE[/bold underline]

    [dim]Our update system employs a multi-layered verification approach:
    1. [white]GitHub API Integration[/white] – Secure communication with official release repository
    2. [yellow]Version Validation[/yellow] – Semantic version comparison with integrity checking
    3. [cyan]Fallback Mechanisms[/cyan] – Redundant update sources for resilience
    4. [green]Privilege Escalation Controls[/green] – Admin rights required only for installation phase
    5. [red]Rollback Capabilities[/red] – Automated restoration points before major updates[/dim]

    [bold cyan]FINAL ADVISORY:[/bold cyan]
    In cybersecurity, your defensive tools are only as strong as their most recent update.
    DSTerminal's capabilities evolve continuously—ensure your installation does too.

    [dim italic]"The only truly secure system is one that is powered off, cast in a block of concrete,
    and sealed in a lead-lined room with armed guards—and even then I have my doubts."[/dim italic]
    [dim]— Updated for the modern threat landscape[/dim]
    CER""",
    
    "vt-scan": """
    [bold]🦠 VirusTotal Tip[/bold]\n
    Advanced features:\n
    - [red]Behavioral analysis[/red] (sandbox)\n
    - [yellow]Community insights[/yellow]\n
    - [blue]YARA rule scanning[/blue]\n
    [green]Warning:[/green] Files become public!\n
    """,
    
    "registry -n mon": """
    [bold]💾 Registry Monitoring Tip[/bold]\n
    Critical keys to watch:\n
    - [red]Run/RunOnce[/red] (persistence)\n
    - [yellow]AppInit_DLLs[/yellow] (code injection)\n
    - [blue]LSA secrets[/blue] (credential storage)\n
    [green]Tool:[/green] Use RegShot for comparisons\n
    """,

    }

SUSPICIOUS_PORTS = {23, 3389, 4444, 5555, 6667, 1337}
HIGH_RISK_COUNTRIES = {"RU", "KP", "IR", "SY"}

def calculate_threat_score(conn, geo=None):
    score = 0

    if not conn.raddr:
        return "LOW", "✓", 0

    ip = conn.raddr.ip
    port = conn.raddr.port

    if not ip.startswith(("192.168", "10.", "172.")):
        score += 2

    if port in SUSPICIOUS_PORTS:
        score += 3

    if not conn.pid:
        score += 2

    if geo and geo.get("countryCode") in HIGH_RISK_COUNTRIES:
        score += 3

    if score >= 7:
        return "HIGH", "✖", score
    elif score >= 4:
        return "MEDIUM", "⚠", score
    else:
        return "LOW", "✓", score


def get_geo_ip(ip):
    try:
        r = requests.get(
            f"http://ip-api.com/json/{ip}?fields=status,country,countryCode,isp",
            timeout=2
        )
        data = r.json()
        if data["status"] == "success":
            return data
    except:
        pass
    return None
    
class SecurityTerminal:
    def __init__(self):
        # Set up workspace root and current directory
        self.workspace_root = os.path.abspath("DSTerminal_Workspace")
        self.current_dir = self.workspace_root
        
        # Create workspace if it doesn't exist
        if not os.path.exists(self.workspace_root):
            os.makedirs(self.workspace_root)
            # print(f"{Fore.GREEN}[+] Created workspace: {self.workspace_root}{Style.RESET_ALL}")
        
        # Create default directories
        default_dirs = ["exploits", "reports", "sandbox", "scans"]
        for dir_name in default_dirs:
            dir_path = os.path.join(self.workspace_root, dir_name)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
        
        self.terminal_width = self._get_terminal_width()

        # Initialize encryption
        self.cipher = None
        self.init_cipher()
 
        # Virtual filesystem directory
        self.vfs_root = os.path.expanduser("~/.dsterminal_vfs")
        self.ensure_vfs()

    def get_key(self):
        if IS_WINDOWS:
            return msvcrt.getch().decode(errors="ignore")
        else:
            return sys.stdin.read(1)

    def enable_raw(self):
        if IS_WINDOWS:
            return None  # Windows does not need raw mode

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        tty.setraw(fd)
        return old_settings


    def disable_raw(self, old):
        if IS_WINDOWS or old is None:
            return

        fd = sys.stdin.fileno()
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

    def show_education_tip(self, command):

        tip = EDUCATION_TIPS.get(command)

        if not tip:
            console.print("[red]No education tip available[/red]")
            return

        console.clear()
        console.print("\n[cyan]📘 Loading Training Module...[/cyan]\n")
        time.sleep(1)

        engine.type_text(tip)

        # =================

    def ensure_vfs(self):
        """Create virtual filesystem directory"""
        os.makedirs(self.vfs_root, exist_ok=True)
    
    def resolve_path(self, filename):
        """Resolve filename to either VFS or real path"""
        # First check VFS
        vfs_path = os.path.join(self.vfs_root, filename)
        if os.path.exists(vfs_path):
            return vfs_path

     # Then check current directory
        if os.path.exists(filename):
            return os.path.abspath(filename)
        
        # Check in VFS subdirectories
        for root, dirs, files in os.walk(self.vfs_root):
            if filename in files:
                return os.path.join(root, filename)
        
        return None

# --------------------VERSION OF THE DSTERMINAL STARTS HERE--------------

    def get_current_version():
        version_file = os.path.join(os.path.dirname(__file__), "VERSION")
        try:
            with open(version_file, "r") as f:
                return f.read().strip()
        except FileNotFoundError:
            return "0.0.0"

# --------------------VERSION OF THE DSTERMINAL END HERE--------------
    def init_cipher(self):
        """Initialize encryption cipher with key from config or user"""
        try:
            key = CONFIG.get('ENCRYPT_KEY')
            if not key:
                # Generate or load key
                key_file = os.path.expanduser("~/.dsterminal_key")
                if os.path.exists(key_file):
                    with open(key_file, 'r') as f:
                        key = f.read().strip()
                else:
                    # Generate new key
                    key = Fernet.generate_key().decode()
                    with open(key_file, 'w') as f:
                        f.write(key)
                    os.chmod(key_file, 0o600)  # Secure permissions
            
            self.cipher = Fernet(key.encode())
        except Exception as e:
            print(f"[!] Encryption initialization failed: {e}")
            self.cipher = None

        """Initialize terminal settings"""
        self.log_file = "security_harden.log"
        self.setup_logging()
 
        self.session = PromptSession(
            history=FileHistory('.dst_history'),
            auto_suggest=AutoSuggestFromHistory(),
            completer=WordCompleter([
                'system scan -All', 'clear', 'clear terminal', 'transfertrace', 'metasploit', 'nmap', 'transfer', 
                'legitify', 'nikto', 'nikto --url [TARGET URL HERE] -p (port number here) -o [output file e.g report.txt]', 'net -n mon', 'harden -t sys', 'vt-scan',
                'registry -n mon', 'crypto-list', 'encrypted-files', 'cls', 'crypto-info', 'nmap',
                'memdump', 'update', 'help', 'exit', 'clearlogs', 'crypto-verify', 'crypto-backup', 'encrypt-test',
                'portsweep', 'hashfile', 'sysinfo', 'killproc',
                'check integrity', 'encrypt', 'decrypt', 'watchfolder',
                'traceroute', 'exploitcheck', 'macspoof', 'dnssec',
                'sqlmap', 'ransomwatch', 'wificrack', 'stegcheck',
                'certcheck', 'torify', 'msf', 'encrypt-setup', 'crypto-init', 'crypto-status', 'mkdir', 'cd', 'touch', 'cat'
            ]),
            bottom_toolbar=HTML('<b>DSTerminal</b> v{} | Mode: <style bg="{}">{}</style>').format(
                CONFIG['CURRENT_VERSION'],
                "ansired" if self.is_admin() else "ansigreen",
                "ADMIN" if self.is_admin() else "USER"
            )
        )
        self.cipher = Fernet(CONFIG['ENCRYPT_KEY'].encode())
        self.scan_complete = Event()
        self.scan_progress = 0

    def is_admin(self):
        """
        Check if running with administrative/root privileges
        """
        try:
            return os.geteuid() == 0
        except AttributeError:
        # Windows fallback
            import ctypes
            try:
                return ctypes.windll.shell32.IsUserAnAdmin()
            except Exception:
                return False

    def setup_logging(self):
        """Configure logging system"""
        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format='%(asctime)s - %(message)s',
            filemode='a'
        )
    def is_windows(self):
        return os.name == "nt"

    def print_banner(self):
        colors = [Fore.RED, Fore.GREEN, Fore.CYAN, Fore.MAGENTA, Fore.YELLOW, Fore.BLUE]
        color = random.choice(colors)
        terminal_width = shutil.get_terminal_size((80, 20)).columns

        banner_lines = [
        "╔═══════════════════════════════════════════════════════════════════============═══╗",
        "    ██████╗ ███████╗███████╗███████╗███╗   ██╗███████╗██╗  ██╗",
        "    ██╔══██╗██╔════╝██╔════╝██╔════╝████╗  ██║██╔════╝╚██╗██╔╝",
        "    ██║  ██║█████╗  █████╗  █████╗  ██╔██╗ ██║█████╗   ╚███╔╝ ",
        "    ██║  ██║██╔══╝  ██╔══╝  ██╔══╝  ██║╚██╗██║██╔══╝   ██╔██╗ ",
        "    ██████╔╝██║     ██║     ███████╗██║ ╚████║███████╗██╔╝ ██╗",
        "    ╚═════╝ ╚═╝     ╚═╝     ╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝",
        "",
        "╠════════════════════════════════════════════════════════════════============══════╣",
        f"║    Defensive Security Terminal v2.0.59 | {platform.system()} {platform.release()}   ║",
        "║    Developed by: Spark Wilson Spink | © 2024| Powered by Stark Expo Tech Exchange║",
        "║    Type 'help' for available commands                                            ║",
        f"║ (🔍, ⚡, 🛡️) 🌐 ⚡ CLI Mode: {'ADMIN' if self.is_admin() else 'USER'}               ",
        "╚════════════════════════════════════════════════════════════════════============══╝"
        ]

        def glitch_char(c):
            if c.isspace():
                return c
            return random.choice(["#", "@", "%", "&", "*", c])

        def type_line(line, delay=0.002, glitch=False):
            centered = line.center(terminal_width)
            output = ""
            for char in centered:
                if glitch and random.random() < 0.04:
                    sys.stdout.write(color + glitch_char(char))
                    sys.stdout.flush()
                    time.sleep(delay * 2)
                    sys.stdout.write('\b' + color + char)
                    sys.stdout.flush()
                else:
                    sys.stdout.write(color + char)
                    sys.stdout.flush()
                time.sleep(delay)
            sys.stdout.write("\n")
            time.sleep(0.01)

        for line in banner_lines:
            type_line(line, glitch=True)

        print(Style.RESET_ALL)

        if not self.is_admin():
            print("\n[!] Warning: Running without administrator privileges. Some features may be limited.")

    def system_info(self):
        """Enhanced system information display with security context"""
        print("\n" + "="*60)
        print("🔍 SYSTEM INFORMATION & SECURITY ASSESSMENT")
        print("="*60)
    
    # Basic system info
        print(f"\n📁 [BASIC SYSTEM]")
        print(f"  OS: {platform.system()} {platform.release()}")
        print(f"  Kernel: {platform.version().split('#')[0] if '#' in platform.version() else platform.version()}")
        print(f"  Architecture: {platform.machine()}")
        print(f"  Hostname: {socket.gethostname()}")
    
    # Enhanced processor info
        print(f"\n⚡ [PROCESSOR]")
        try:
            with open('/proc/cpuinfo', 'r') as f:
                cpuinfo = f.read()
            # Get processor model
                for line in cpuinfo.split('\n'):
                    if 'model name' in line:
                        processor = line.split(':')[1].strip()
                        print(f"  Model: {processor}")
                        break
            # Count cores
                cores = cpuinfo.count('processor\t:')
                print(f"  Cores: {cores} logical processors")
        except:
            print("  Info: Unable to read CPU info")
    
    # Memory info with psutil
        print(f"\n💾 [MEMORY]")
        if psutil:
            mem = psutil.virtual_memory()
            swap = psutil.swap_memory()
            print(f"  RAM: {mem.used/1024**3:.1f}/{mem.total/1024**3:.1f} GB ({mem.percent}% used)")
            print(f"  Swap: {swap.used/1024**3:.1f}/{swap.total/1024**3:.1f} GB ({swap.percent if swap.total > 0 else 0}% used)")
        else:
            print("  Info: psutil not available")
    
    # Disk info
        print(f"\n💿 [STORAGE]")
        if psutil:
            try:
                disk = psutil.disk_usage('/')
                print(f"  Root FS: {disk.used/1024**3:.1f}/{disk.total/1024**3:.1f} GB ({disk.percent}% used)")
                print(f"  Free: {disk.free/1024**3:.1f} GB")
            except:
                print("  Info: Disk info unavailable")
    
    # Security context
        print(f"\n🛡️ [SECURITY CONTEXT]")
        print(f"  Privileges: {'🔴 ADMIN/ROOT' if self.is_admin() else '🟢 USER'}")
        print(f"  Workspace: {self.current_dir}")
    
    # Network info
        print(f"\n🌐 [NETWORK]")
        try:
            interfaces = netifaces.interfaces()
            print(f"  Interfaces: {len(interfaces)} found")
            for iface in interfaces[:3]:  # Show first 3
                print(f"    • {iface}")
        except ImportError:
            print("  Info: Install 'netifaces' for network details")
    
    # Python environment
        print(f"\n🐍 [PYTHON ENVIRONMENT]")
        print(f"  Version: {platform.python_version()}")
        print(f"  Implementation: {platform.python_implementation()}")
        print(f"  Virtual Env: {'Yes' if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) else 'No'}")
    
    # Security recommendations
        print(f"\n📋 [RECOMMENDATIONS]")
        if not self.is_admin():
            print("  ⚠️  Run with sudo for full security features")
            print("  🔍 Run 'exploitcheck' for vulnerability assessment")
            print("  🛡️  Run 'check integrity' for system file verification")
            print("  📊 Run 'system scan -All' for comprehensive scan")
    
            print("\n" + "="*60)


    def show_tip(self, cmd):
        """Display educational tip for the executed command."""
        if cmd in EDUCATION_TIPS:
            tip = EDUCATION_TIPS[cmd]
            console = Console()
            console.print(
                Align.center(
                    Panel.fit(
                        tip,
                        title="[bold cyan]RECOMMENDED EDUCATIONAL TIP[/bold cyan]",
                        border_style="blue",
                        width=60,
                    ),
                    vertical="middle",
                )
            )
        # displaying education tips code ends here


# ---------------------folder or dir creation for safe environment running
    def safe_path(self, path):
        full_path = os.path.abspath(os.path.join(self.current_dir, path))
        if not full_path.startswith(self.workspace_root):
            raise PermissionError("Access outside workspace is not allowed")
        return full_path
# --------------------------------------------creating dir/folder
 
# ---viewing a file

# Initialize colorama for Windows compatibility

    def _get_terminal_width(self):
        """Get terminal width for centering"""
        try:
            import shutil
            return shutil.get_terminal_size().columns
        except:
            return 80  # Default width
    
    def _center_text(self, text):
        """Center text based on terminal width"""
        return text.center(self.terminal_width)
    
    # ---------------------folder or dir creation for safe environment running
    def safe_path(self, path):
        """Ensure path is within workspace"""
        full_path = os.path.abspath(os.path.join(self.current_dir, path))
        if not full_path.startswith(self.workspace_root):
            raise PermissionError("Access outside workspace is not allowed")
        return full_path
    
    # --------------------------------------------creating dir/folder
    def mkdir(self, dirname):
        """Create a directory"""
        try:
            path = self.safe_path(dirname)
            os.makedirs(path, exist_ok=True)
            print(f"{Fore.GREEN}[+]📁 Safe directory created successfully: {os.path.basename(path)}{Style.RESET_ALL}")
        except PermissionError as e:
            print(f"{Fore.RED}[!] {e}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[!] Error creating directory: {e}{Style.RESET_ALL}")
    
    # -------------------------------creating a file------------------
    def touch(self, filename):
        """Create an empty file"""
        try:
            path = self.safe_path(filename)
            with open(path, "w") as f:
                f.write("DSTerminal test file\n")
            print(f"{Fore.GREEN}[+] File created: {filename}{Style.RESET_ALL}")
        except PermissionError as e:
            print(f"{Fore.RED}[!] {e}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[!] Error creating file: {e}{Style.RESET_ALL}")
    
    # -----------------------echo function
 
    # ------------------------folder/file navigation-------------
    def handle_echo(self, user_input):
        """
        Handle the echo command:
        - echo text
        - echo text > file
        - echo text >> file
        """
        try:
            # Remove leading/trailing whitespace
            user_input = user_input.strip()

            # Must start with 'echo'
            if not user_input.lower().startswith("echo"):
                print("[!] Invalid echo command")
                return

        # Remove 'echo' from start
            command_body = user_input[4:].strip()  # safely remove first 4 chars

        # Check for file redirection
            if '>>' in command_body:
                parts = command_body.split('>>', 1)
                text_part = parts[0].strip()
                filename = parts[1].strip()
                mode = 'a'  # append
            elif '>' in command_body:
                parts = command_body.split('>', 1)
                text_part = parts[0].strip()
                filename = parts[1].strip()
                mode = 'w'  # overwrite
            else:
            # Simple echo (no file)
                print(command_body)
                return

        # Remove quotes if present
            text_part = text_part.strip('"').strip("'")

        # Resolve safe path
            path = self.safe_path(filename)

        # Make sure directory exists
            dir_name = os.path.dirname(path)
            if dir_name:
                os.makedirs(dir_name, exist_ok=True)

        # Write to file
            with open(path, mode, encoding='utf-8') as f:
                f.write(text_part + '\n')

            print(f"[+] Written to {filename}")
            print(f"   Content: '{text_part}'")
            print(f"[DEBUG] Full path: {path}")

        except Exception as e:
            print(f"[!] Echo failed: {e}")
    
    def pwd(self):
        """Print working directory"""
        # Replace workspace root with ~ for display
        display_path = self.current_dir.replace(self.workspace_root, "~")
        print(display_path) 
    
    # ---------------------------------
    def ls(self, path="."):
        """List directory contents"""
        try:
            target_path = self.safe_path(path) if path != "." else self.current_dir
            items = os.listdir(target_path)
            
            # Color-code directories and files
            for item in sorted(items):
                item_path = os.path.join(target_path, item)
                if os.path.isdir(item_path):
                    print(f"{Fore.BLUE}{item}{Style.RESET_ALL}")  # Directories in blue
                else:
                    print(f"{Fore.WHITE}{item}{Style.RESET_ALL}")  # Files in white
                    
        except PermissionError as e:
            print(f"{Fore.RED}[!] {e}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[!] Error listing directory: {e}{Style.RESET_ALL}")
    
    # =---------------------------------------------
    def cd(self, dirname):
        """Change directory"""
        try:
            if dirname == "~" or dirname == "":
                path = self.workspace_root
            else:
                path = self.safe_path(dirname)
                
            if os.path.isdir(path):
                self.current_dir = path
                # Show new path
                display_path = path.replace(self.workspace_root, "~")
                print(f"{Fore.GREEN}[+] Changed to: {display_path}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}[!] Not a directory: {dirname}{Style.RESET_ALL}")
                
        except PermissionError as e:
            print(f"{Fore.RED}[!] {e}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[!] Error changing directory: {e}{Style.RESET_ALL}")
    
    # -----------------------------------
    # ---viewing a file
    def cat(self, filename):
        """Display file contents"""
        try:
            path = self.safe_path(filename)
            with open(path, "r") as f:
                content = f.read()
                print(content)
        except FileNotFoundError:
            print(f"{Fore.RED}[!] File not found: {filename}{Style.RESET_ALL}")
        except PermissionError as e:
            print(f"{Fore.RED}[!] {e}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[!] Error reading file: {e}{Style.RESET_ALL}")
    
    # -----------------------------------
    # Command dispatcher - THIS IS THE KEY MISSING PART!
    def process_command(self, user_input):
        """Process and dispatch commands"""
        if not user_input.strip():
            return True  # Nothing to do, continue

    # Handle echo first to preserve the raw string
        if user_input.strip().lower().startswith("echo"):
            self.handle_echo(user_input)
            return True

    # Otherwise, parse normally
        import shlex
        parts = shlex.split(user_input)
        command = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []

    # Command dispatch
        if command == "help":
            self.show_help()
        elif command in ("exit", "quit"):
            print(f"{Fore.YELLOW}[+] Exiting DSTerminal...{Style.RESET_ALL}")
            return False
        elif command in ("clear", "cls"):
            os.system('cls' if os.name == 'nt' else 'clear')
        elif command == "pwd":
            self.pwd()
        elif command == "ls":
            self.ls(args[0] if args else ".")
        elif command == "cd":
            if args:
                self.cd(args[0])
            else:
                self.cd("~")
        elif command == "mkdir":
            if args:
                self.mkdir(args[0])
            else:
                print(f"{Fore.RED}[!] Usage: mkdir <directory_name>{Style.RESET_ALL}")
        elif command == "touch":
            if args:
                self.touch(args[0])
            else:
                print(f"{Fore.RED}[!] Usage: touch <filename>{Style.RESET_ALL}")
        elif command == "cat":
            if args:
                self.cat(args[0])
            else:
                print(f"{Fore.RED}[!] Usage: cat <filename>{Style.RESET_ALL}")
        elif command == "harden":
            dry_run = "-t" in args or "--test" in args
            self.harden_system(dry_run=dry_run)
        else:
            print(f"{Fore.RED}[!] Unknown command: '{command}'. Type 'help' for available commands.{Style.RESET_ALL}")

        return True

    def show_help(self):
        """Display help information"""
        help_text = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗
║                    DSTERMINAL HELP MENU                        ║
╠════════════════════════════════════════════════════════════════╣
║  {Fore.YELLOW}FILE OPERATIONS:{Fore.CYAN}                                            ║
║    ls                    - List directory contents             ║
║    cd <dir>              - Change directory                    ║
║    pwd                   - Print working directory             ║
║    mkdir <name>          - Create a new directory              ║
║    touch <file>          - Create a new file                   ║
║    cat <file>            - Display file contents               ║
║    echo <text>           - Display text                        ║
║    echo <text> > <file>  - Write text to file                  ║
║    echo <text> >> <file> - Append text to file                 ║
║                                                               ║
║  {Fore.YELLOW}SYSTEM OPERATIONS:{Fore.CYAN}                                          ║
║    harden                - Run system hardening                ║
║    harden -t             - Test mode (dry run)                 ║
║    clear / cls           - Clear the screen                    ║
║    exit / quit           - Exit DSTerminal                     ║
║    help                  - Show this help menu                 ║
║                                                               ║
║  {Fore.YELLOW}WORKSPACE:{Fore.CYAN}                                                ║
║    All operations are confined to: {Fore.GREEN}~/DSTerminal_Workspace{Fore.CYAN}     ║
║    Default directories: exploits, reports, sandbox, scans      ║
╚════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
        print(help_text)
    
    def run(self):
        """Main terminal loop"""
        print(f"{Fore.GREEN}DSTerminal v2.0.59 | Type 'help' for commands | Workspace: ~/DSTerminal_Workspace{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Mode: {'ADMIN' if self.is_admin() else 'USER'}{Style.RESET_ALL}\n")
        
        running = True
        while running:
            try:
                # Show prompt
                prompt_path = self.current_dir.replace(self.workspace_root, "~")
                user_input = input(f"{Fore.CYAN}[-- DFFENEX@DSTerminal {prompt_path} ]-{Style.RESET_ALL} ").strip()
                
                # Process command
                if user_input:
                    running = self.process_command(user_input)
                    
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}[!] Use 'exit' to quit{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}[!] Error: {e}{Style.RESET_ALL}")
  
#   metasploit--------------------



# ------added msf impleme
 
    def launch_metasploit(self):
        system = platform.system()

        try:
            if system == "Linux":
                subprocess.call(["msfconsole"])

            elif system == "Windows":

                try:
                    result =subprocess.run(
                        ["wsl", "bash", "-c", "command -v msfconsole"],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    )
                    if result.returncode == 0:
                        return True
                except Exception as e:
                    pass
                return shutil.which("msfconsole") is not None

            elif system == "Darwin":
                subprocess.call(["msfconsole"])

            else:
                print("Unsupported OS.")

        except FileNotFoundError:
            print(f"{Fore.RED}[!] msfconsole not found in PATH{Style.RESET_ALL}")

    def check_metasploit_installed(self):
        system = platform.system()

        if system == "Linux":
            return shutil.which("msfconsole") is not None

        elif system == "Windows":
        # Check WSL
            try:
                result = subprocess.run(
                    ["wsl", "which", "msfconsole"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                return result.returncode == 0
            except Exception:
                return False

        elif system == "Darwin":  # macOS
            return shutil.which("msfconsole") is not None

        return False
    
    def cinematic_spinner(self, stop_event, message, color=Fore.CYAN):
        """Enhanced spinner with cinematic effects"""
        spinner_chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        i = 0
        while not stop_event.is_set():
            sys.stdout.write(f"\r{color}{spinner_chars[i]} {message}{Style.RESET_ALL}")
            sys.stdout.flush()
            time.sleep(0.1)
            i = (i + 1) % len(spinner_chars)
        sys.stdout.write("\r" + " " * (len(message) + 20) + "\r")
    
    def typewriter_effect(self, text, delay=0.03, color=Fore.GREEN):
        """Typewriter effect for text output"""
        for char in text:
            sys.stdout.write(f"{color}{char}{Style.RESET_ALL}")
            sys.stdout.flush()
            time.sleep(delay)
        print()
    
    def scan_lines(self, text, line_count=3, delay=0.05):
        """Simulate scanning lines like a terminal"""
        for i in range(line_count):
            line = f"[SCANNING] {text}... [{i+1}/{line_count}]"
            print(Fore.YELLOW + line, end="\r")
            time.sleep(delay)
        print(" " * 50, end="\r")
    
    def play_beep(self):
        """Play a beep sound (ASCII bell)"""
        print("\a", end="", flush=True)
    
    def animated_progress_bar(self, title, duration=2):
        """Animated progress bar"""
        print(f"\n{title}")
        for i in range(101):
            bar = "█" * (i // 2) + "░" * (50 - (i // 2))
            print(f"\r[{bar}] {i}%", end="", flush=True)
            time.sleep(duration / 100)
        print()

    def metasploit_intro(self):
        """Cinematic Metasploit introduction sequence"""
        phases = [
            ("Initializing Metasploit Framework", 0.7, Fore.CYAN),
            ("Loading exploit modules", 0.5, Fore.RED),
            ("Loading auxiliary modules", 0.5, Fore.YELLOW),
            ("Initializing database interface", 0.6, Fore.GREEN),
            ("Preparing cyber operations shell", 0.8, Fore.MAGENTA),
            ("Establishing secure connection", 0.4, Fore.BLUE),
            ("Bypassing security protocols", 0.5, Fore.RED),
            ("Setting up payload handlers", 0.6, Fore.CYAN)
        ]
        
        print("\n" + "="*50)
        print(Fore.RED + "           METASPLOIT FRAMEWORK" + Style.RESET_ALL)
        print("="*50 + "\n")
        
        # Simulate system scan
        self.scan_lines("Checking system compatibility", 4, 0.1)
        
        for phase, delay, color in phases:
            sys.stdout.write(f"{color}[+] {phase}")
            sys.stdout.flush()
            
            # Add dynamic dots
            for _ in range(3):
                sys.stdout.write(".")
                sys.stdout.flush()
                time.sleep(delay/3)
            
            print(f" {Fore.GREEN}✓{Style.RESET_ALL}")
            
            # Random progress simulation
            if "exploit" in phase.lower():
                self.scan_lines("Verifying exploit integrity", 2, 0.1)
            elif "database" in phase.lower():
                time.sleep(0.3)
                print(f"  {Fore.BLUE}>> Database connection established{Style.RESET_ALL}")
        
        # Final loading animation
        print(f"\n{Fore.YELLOW}[*] Finalizing initialization...")
        for i in range(5):
            print(f"  {Fore.YELLOW}▶ Loading component {i+1}/5", end="\r")
            time.sleep(0.2)
        
        self.play_beep()

    def show_metasploit_install_guide(self):
        """Show installation instructions for Metasploit"""

        system = platform.system()

        print(f"{Fore.RED}[!] Metasploit Framework not detected on this system.{Style.RESET_ALL}\n")

        if system == "Linux":
            print(Fore.CYAN + "[Linux Installation]" + Style.RESET_ALL)
            print("Recommended installation:")
            print(Fore.YELLOW + "  sudo apt update && sudo apt install metasploit-framework\n" + Style.RESET_ALL)

            print("Alternative (official installer):")
            print("  curl https://raw.githubusercontent.com/rapid7/metasploit-framework/master/msfinstall | sudo bash\n")

        elif system == "Windows":
            print(Fore.CYAN + "[Windows Installation]" + Style.RESET_ALL)

            print("Option 1: Install via WSL (Recommended)")
            print(Fore.YELLOW + "  wsl --install\n" + Style.RESET_ALL)
            print("Then install metasploit inside WSL:")

            print(Fore.YELLOW + "  sudo apt install metasploit-framework\n" + Style.RESET_ALL)

            print("Option 2: Use the official Windows installer:")
            print("  https://www.metasploit.com/download\n")

        elif system == "Darwin":
            print(Fore.CYAN + "[macOS Installation]" + Style.RESET_ALL)

            print("Install via Homebrew:")
            print(Fore.YELLOW + "  brew install metasploit\n" + Style.RESET_ALL)

            print("Official installer:")
            print("  https://www.metasploit.com/download\n")

        else:
            print("Unsupported operating system.\n")

        print(Fore.GREEN + "[*] After installation, restart DSTerminal and run 'msf' again." + Style.RESET_ALL)

    def handle_msf(self, args):
        """Handle Metasploit launch with cinematic effects"""
        if not self.check_metasploit_installed():
            self.show_metasploit_install_guide()
            return
        
        # Clear screen for cinematic effect
        os.system('clear' if os.name == 'posix' else 'cls')
        
        # Start cinematic intro
        self.metasploit_intro()
        
        # Launch sequence with enhanced spinner
        print(f"\n{Fore.MAGENTA}[*] Starting Metasploit Framework...{Style.RESET_ALL}")
        
        stop_event = threading.Event()
        spinner_messages = [
            "LAUNCHING MSFCONSOLE",
            "ESTABLISHING CONNECTION",
            "PREPARING PAYLOAD HANDLERS",
            "LOADING EXPLOIT DATABASE",
            "INITIALIZING SESSION MANAGER"
        ]
        
        for msg in spinner_messages:
            spinner = threading.Thread(
                target=self.cinematic_spinner,
                args=(stop_event, msg, Fore.CYAN),
                daemon=True
            )
            spinner.start()
            time.sleep(1.5)
            stop_event.set()
            spinner.join()
            stop_event.clear()
        
        # Countdown effect
        print(f"\n{Fore.RED}[!] LAUNCHING IN:{Style.RESET_ALL}")
        for i in range(3, 0, -1):
            print(f"  {Fore.RED}{i}...{Style.RESET_ALL}")
            time.sleep(0.5)
        
        # Final handoff
        print(f"\n{Fore.GREEN}[+] Handing control to Metasploit Framework...{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[*] Use 'exit' to return to DSTerminal{Style.RESET_ALL}")
        self.play_beep()
        time.sleep(1)
        
        try:
            # Replace current process with msfconsole (REAL TTY)
            # os.execvp("msfconsole", ["msfconsole"])
            self.launch_metasploit()
        except FileNotFoundError:
            print(f"{Fore.RED}[!] msfconsole not found in PATH{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[!] Failed to start Metasploit: {e}{Style.RESET_ALL}")
    
    # Alternative implementation with ASCII art
    def cinematic_msf_intro_ascii(self):
        """ASCII art cinematic intro for Metasploit"""
        ascii_art = [
            r"  __  __      _        _____       _     _ _   ",
            r" |  \/  | ___| |_ __ _|  ___|_ __ | | __(_) |_ ",
            r" | |\/| |/ _ \ __/ _` | |_ | '_ \| |/ _| | __|",
            r" | |  | |  __/ || (_| |  _|| |_) | | (_| | |_ ",
            r" |_|  |_|\___|\__\__,_|_|  | .__/|_|\__,_|\__|",
            r"                           |_|                "
        ]
        
        for line in ascii_art:
            self.typewriter_effect(line, 0.02, Fore.RED)
            time.sleep(0.05)
        
        # Matrix-like falling code effect
        print(f"\n{Fore.GREEN}")
        matrix_chars = "01█▓▒░█▓▒░"
        for _ in range(10):
            line = ''.join([matrix_chars[i % len(matrix_chars)] for i in range(50)])
            print(line, end="\r")
            time.sleep(0.1)
        print(Style.RESET_ALL + " " * 50)
 
# ---------========-----------------metasplo ends here from above-----------------------------
    ALLOWED_NMAP_FLAGS = {"-p", "-sT", "-sS", "-sV", "-T4", "-Pn"}
    def check_nmap_installed(self):
        return shutil.which("nmap") is not None


    def handle_nmap(self, args):
        if not self.check_nmap_installed():
            print("[!] Nmap is not installed on this system")
            return

        if len(args) < 2 or args[0] != "scan":
            print("Usage: nmap scan <target> [flags]")
            return

        target = args[1]
        flags = args[2:]

        cmd = ["nmap"]

        for f in flags:
            if f.startswith("-"):
                if f not in self.ALLOWED_NMAP_FLAGS:
                    print(f"[!] Flag not allowed: {f}")
                    return
            cmd.append(f)

        cmd.append(target)

    # Ensure scans directory exists
        scans_dir = os.path.join(self.workspace_root, "scans")
        os.makedirs(scans_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(
            scans_dir,
            f"nmap_{target}_{timestamp}.txt"
        )

        cmd.extend(["-oN", output_file])

        print(f"[+] Running nmap scan on {target}...")
        print(f"[+] Output → scans/{os.path.basename(output_file)}")

        try:
            subprocess.run(
                cmd,
                shell=self.is_windows(),
                check=True
            )
        except subprocess.CalledProcessError as e:
            print(f"[!] Nmap failed: {e}")


# =====================end nmap here----

    def handle_ls(self):
        path = os.getcwd()
        for item in os.listdir(path):
            print(item)
    def handle_touch(self, filename):
        open(filename, "a").close()
        print(f"[+] File created: {filename}")
    def handle_cat(self, filename):
        if not os.path.exists(filename):
            print("[!] File not found")
            return
        with open(filename, "r") as f:
            print(f.read())
    def handle_echo(self, user_input):
 
        tokens = shlex.split(user_input)

        if len(tokens) < 2:
            print()
            return

        if ">" in tokens:
            idx = tokens.index(">")
            mode = "w"
        elif ">>" in tokens:
            idx = tokens.index(">>")
            mode = "a"
        else:
            print(" ".join(tokens[1:]))
            return

        content = " ".join(tokens[1:idx])
        filename = tokens[idx + 1]

        try:
            with open(filename, mode) as f:
                f.write(content + "\n")
            print(f"[+] Written to {filename}")
        except Exception as e:
            print(f"[!] Echo failed: {e}")

# =-------------------------------------------
 

    def scan_system(self):
        """Real system scanner with live OS-backed results"""
 

        if not hasattr(self, "console"):
            self.console = Console()

    # ✅ instance attributes (THREAD SAFE)
        self.found_threats = False
        self.scan_stages = [
            ("[cyan]Scanning Memory...", "Memory Scan"),
            ("[yellow]Analyzing Processes...", "Process Scan"),
            ("[magenta]Inspecting Temp Files...", "Temp File Scan"),
            ("[blue]Checking Network...", "Network Scan"),
            ("[green]Auditing Installed Software...", "Software Audit"),
            ("[white]Verifying System Integrity...", "System Integrity"),
            ("[red]Reviewing User Accounts...", "User Audit"),
            ("[bright_cyan]Checking Security Configs...", "Security Configs"),
            ("[bright_magenta]Behavioral Analysis...", "Heuristics"),
        ]

        scan_thread = Thread(target=self.run_scan, daemon=False)
        scan_thread.start()
        return scan_thread


    def generate_scan_results(self, stage_name):    
        results = []

        if stage_name == "Memory Scan" and psutil:
            mem = psutil.virtual_memory()
            swap = psutil.swap_memory()
            results.extend([
                ("RAM Usage", f"{mem.percent}%", "green" if mem.percent < 80 else "yellow"),
                ("Available RAM", f"{mem.available // (1024**2)} MB", "cyan"),
                ("Swap Usage", f"{swap.percent}%", "green" if swap.percent < 50 else "yellow"),
            ])

        elif stage_name == "Process Scan" and psutil:
            procs = list(psutil.process_iter(["pid", "name"]))
            results.append(("Running Processes", str(len(procs)), "cyan"))

            suspicious = []
            for p in procs:
                if p.info["name"]:
                    name = p.info["name"].lower()
                    if any(x in name for x in ["keylog", "miner", "backdoor", "exploit"]):
                        suspicious.append(p.info["name"])

            if suspicious:
                self.found_threats = True
                results.append(("Suspicious Processes", ", ".join(suspicious[:3]), "red"))
            else:
                results.append(("Suspicious Processes", "None detected", "green"))

        elif stage_name == "Heuristics":
            score = 70 if self.found_threats else 100
            color = "red" if score < 80 else "green"
            results.append(("Threat Score", f"{score}/100", color))

        return results


    def display_stage_results(self, stage_name):

        results = self.generate_scan_results(stage_name)

        table = Table(title=stage_name, header_style="bold magenta")
        table.add_column("Check", style="cyan", width=25)
        table.add_column("Result", width=30)
        table.add_column("Status", width=12)

        for check, result, color in results:
            table.add_row(
                check,
                result,
                f"[{color}]{color.upper()}[/{color}]"
            )

        self.console.print(Panel(table, border_style="bright_blue"))


    def run_scan(self):
 
        with Live(console=self.console, refresh_per_second=15) as live:
            for label, stage in self.scan_stages:
                progress = Progress(
                    TextColumn("[bold cyan]{task.description}"),
                    BarColumn(),
                    TextColumn("{task.percentage:>3.0f}%"),
                    console=self.console,
                )

                task = progress.add_task(label, total=100)

                for _ in range(100):
                    progress.update(task, advance=1)
                    live.update(
                        Panel(
                            Align.center(progress),
                            title="[bold]System Security Scan[/bold]",
                            subtitle=stage,
                            border_style="bright_blue",
                        )
                    )
                    time.sleep(0.03)

                self.display_stage_results(stage)
                time.sleep(0.6)

    # ✅ Final verdict
        if self.found_threats:
            self.console.print(Panel(
                "[bold red]⚠ THREATS DETECTED[/bold red]",
                border_style="red",
            ))
        else:
            self.console.print(Panel(
                "[bold green]✓ SYSTEM SECURE[/bold green]",
                border_style="green",
            ))

 
#  network monitoring implementation from here to below

    def init_bandwidth(self):
        self.prev_io = psutil.net_io_counters()

    def get_bandwidth(self):
        current = psutil.net_io_counters()
        sent = current.bytes_sent - self.prev_io.bytes_sent
        recv = current.bytes_recv - self.prev_io.bytes_recv
        self.prev_io = current
        return sent, recv

    def network_monitor(self):
        """Animated network monitoring with hacking-style visuals (stable version)"""
        self.init_bandwidth()

        console = Console()
        scanning_icons = ["🜂", "🜁", "🜃", "🜄", "⦿", "⌾", "⍟", "⋙"]

    # ----------------------------
    # Generate connection table
    # ----------------------------
        def generate_connection_table(connections):
            table = Table()

            table.add_column("LOCAL", style="cyan")
            table.add_column("→", justify="center")
            table.add_column("REMOTE", style="magenta")
            table.add_column("PID", justify="right")
            table.add_column("STATUS", justify="right")
            table.add_column("THREAT", justify="right")
            table.add_column("COUNTRY")
            table.add_column("ISP")
            table.add_column("SCORE", justify="right")

            for conn in connections:
                if conn.status == "ESTABLISHED" and conn.raddr:
                    geo = get_geo_ip(conn.raddr.ip)
                    level, icon, score = calculate_threat_score(conn, geo)
                    country = geo["country"] if geo else "N/A"
                    isp = geo["isp"] if geo else "N/A"
                    local = f"{conn.laddr.ip}:{conn.laddr.port}"
                    remote = f"{conn.raddr.ip}:{conn.raddr.port}"

                    table.add_row(local, "⋙", remote,
                                str(conn.pid) if conn.pid else "N/A",
                                "[green]ACTIVE", icon,
                                country, isp, str(score))
            return table

        # Threat scoring
                    # level, icon, score = calculate_threat_score(conn, geo)

                    # country = geo["country"] if geo else "N/A"
                    # isp = geo["isp"] if geo else "N/A"

                    # table.add_row(
                    #     local,
                    #     "⋙",
                    #     remote,
                    #     str(conn.pid) if conn.pid else "N/A",
                    #     "[green]ACTIVE",
                    #     icon,
                    #     country,
                    #     isp,
                    #     str(score)
                    # )

            # return table  # 🔥 IMPORTANT: Only returns Table (no recursion!)

    # ----------------------------
    # Pre-scan animation
    # ----------------------------
        def threat_scan_animation():
            with console.status("[bold green]Initializing network sensors..."):
                for i in range(5):
                    console.log(f"[cyan]Scanning layer {i+1}/5...")
                    time.sleep(1)

    # ----------------------------
    # Live Monitor (NO recursion)
    # ----------------------------
        from collections import Counter

        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.lib import colors
        from reportlab.lib.units import inch
        from reportlab.platypus import Table as PDFTable
        from reportlab.platypus import TableStyle
        from reportlab.lib.styles import getSampleStyleSheet

        def export_forensic_report(connections, filename="forensic_report.pdf"):
            doc = SimpleDocTemplate(filename)
            elements = []

            styles = getSampleStyleSheet()
            elements.append(Paragraph("DSTerminal Forensic Network Report", styles["Heading1"]))
            elements.append(Spacer(1, 0.5 * inch))

            data = [["Local", "Remote", "PID", "Status", "Country", "ISP", "Score"]]

            for conn in connections:
                if conn.raddr:
                    geo = get_geo_ip(conn.raddr.ip)
                    level, icon, score = calculate_threat_score(conn, geo)
                    country = geo["country"] if geo else "N/A"
                    isp = geo["isp"] if geo else "N/A"

                    local = f"{conn.laddr.ip}:{conn.laddr.port}"
                    remote = f"{conn.raddr.ip}:{conn.raddr.port}"

                    data.append([local, remote, str(conn.pid), conn.status, country, isp, str(score)])

            table = PDFTable(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.grey),
                ('GRID', (0,0), (-1,-1), 0.5, colors.black),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('ALIGN', (2, 1), (-1, -1), 'CENTER')
            ]))

            elements.append(table)
            doc.build(elements)
            print(f"[✓] Forensic report exported to {filename}")




        def detect_intrusion(connections):
            ips = [c.raddr.ip for c in connections if c.raddr]
            counts = Counter(ips)

            alerts = []
            for ip, count in counts.items():
                if count > 15:
                    alerts.append(f"Possible port scan from {ip}")

            return alerts


        def live_monitor(duration=15):
            sent, recv = self.get_bandwidth()

            upload_kb = sent / 1024
            download_kb = recv / 1024

            bandwidth_bar = "█" * int(download_kb / 5)

            bandwidth_panel = Panel(
            f"Download: {download_kb:.2f} KB/s\nUpload: {upload_kb:.2f} KB/s\n\n{bandwidth_bar}",
            title="Bandwidth Activity",
            border_style="green"
        )

            start_time = time.time()

            with Live(console=console, refresh_per_second=2) as live:
                while time.time() - start_time < duration:

                    try:
                        connections = psutil.net_connections()
                    except Exception as e:
                        console.print(f"[red]Access Error: {e}")
                        break

                    table = generate_connection_table(connections)

                    stats = Table()
                    stats.add_column("Metric")
                    stats.add_column("Value")

                    stats.add_row("Total Connections", str(len(connections)))
                    stats.add_row(
                        "ESTABLISHED",
                        str(sum(1 for c in connections if c.status == "ESTABLISHED"))
                    )
                    stats.add_row(
                        "LISTEN",
                        str(sum(1 for c in connections if c.status == "LISTEN"))
                    )

                    alerts = detect_intrusion(connections)

                    for alert in alerts:
                        console.print(f"[bold red]⚠ INTRUSION ALERT: {alert}")

                    dashboard = Table.grid(expand=True)
                    dashboard.add_row(bandwidth_panel)
                    dashboard.add_row(
                        Panel(
                            table,
                            title="[bold red]NETWORK TRAFFIC ANALYSIS[/bold red]",
                            border_style="bright_blue"
                        )
                    )
                    dashboard.add_row(
                        Panel(
                            stats,
                            title="[bold yellow]Network Statistics[/bold yellow]",
                            border_style="yellow"
                        )
                    )

                    live.update(dashboard)
                    time.sleep(2)

            # 🔥 Auto-generate PDF after live monitoring
            export_forensic_report(connections)

                    

    # ----------------------------
    # Run Monitor
    # ----------------------------
        console.print(
            Panel(
                "[bold red] INITIATING NETWORK MONITORING SURVEILLANCE [/bold red]",
                border_style="red"
            )
        )

        threat_scan_animation()
        live_monitor(duration=15)

        console.print(
            Panel(
                "[bold green] SCAN COMPLETED [/bold green]",
                border_style="green"
            )
        )

        connections = psutil.net_connections()
        export_forensic_report(connections)
    # ==================== NEW ADVANCED COMMANDS ====================
    def check_exploits(self):
        vulns = {
            "CVE-2021-44228": "Log4j RCE",
            "CVE-2017-0144": "EternalBlue"
        }
        print("\n[+] Checking for critical CVEs...")
        for cve, desc in vulns.items():
            print(f"{cve}: {desc} - {'[!] VULNERABLE' if random.random() > 0.7 else '[+] Secure'}")

    
    def spoof_mac(self, interface=None):
        """Enhanced MAC spoofing with progress indicators and persistent output"""
        console = Console()

    # Animation frames
        FRAMES = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

        def create_panel(content, title="", border_style="blue"):
            return Panel(
                content,
                title=title,
                border_style=border_style,
                width=60,
                padding=(1, 2)
            )

        def generate_display(debug_msgs, status_msgs, progress=None):
            debug_panel = create_panel(
                "\n".join(debug_msgs[-5:]),
                title="[blue]DEBUG LOG[/blue]",
                border_style="blue"
            )
        
            status_panel = create_panel(
                "\n".join(status_msgs[-5:]),
                title="[green]STATUS[/green]",
                border_style="green"
            )
        
            progress_panel = create_panel(
                progress if progress else "Initializing...",
                title="[red]PROGRESS[/red]",
                border_style="red"
            )
        
            return Columns([debug_panel, status_panel, progress_panel])

        debug_messages = []
        status_messages = []
        current_frame = 0

        try:
        # Main display context
            with Live(generate_display(debug_messages, status_messages), console=console) as live:
            # 1. Admin Check
                debug_messages.append("Checking admin privileges...")
                live.update(generate_display(debug_messages, status_messages))
            
                if not self.is_admin():
                    status_messages.append("[red]✖ Requires admin privileges[/red]")
                    live.update(generate_display(debug_messages, status_messages))
                    raise PermissionError("Admin rights required")
            
                status_messages.append("[green]✔ Admin privileges confirmed[/green]")
                live.update(generate_display(debug_messages, status_messages))
            
            # 2. Interface Detection
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    transient=True
                ) as progress:
                    task = progress.add_task("Detecting interface...", total=100)
                    for i in range(100):
                        progress.update(task, advance=1)
                        time.sleep(0.02)
                        if i % 10 == 0:
                            live.update(generate_display(debug_messages, status_messages))
            
                def get_active_interface():
                    try:
                        if platform.system() in ['Linux', 'Darwin']:
                            route = subprocess.check_output("ip route show default", 
                                                        shell=True, 
                                                        stderr=subprocess.PIPE).decode()
                            if len(route.split()) >= 5:
                                return route.split()[4]
                        elif platform.system() == 'Windows':
                            output = subprocess.check_output("getmac /v /fo csv", 
                                                        shell=True, 
                                                        stderr=subprocess.PIPE).decode()
                            lines = [l for l in output.split('\n') if l.strip()]
                            if len(lines) > 1:
                                return lines[1].split(',')[0].strip('"')
                    except Exception as e:
                        debug_messages.append(f"Error: {str(e)}")
                    return None
            
                if not interface:
                    interface = get_active_interface()
                    if not interface:
                        status_messages.append("[red]✖ Interface detection failed[/red]")
                        live.update(generate_display(debug_messages, status_messages))
                        raise ValueError("No interface detected")
            
                status_messages.append(f"[green]✔ Interface: [bold]{interface}[/bold][/green]")
                live.update(generate_display(debug_messages, status_messages))
            
            # 3. MAC Generation
                new_mac = "02:%02x:%02x:%02x:%02x:%02x" % (
                    random.randint(0x00, 0x7f),
                    random.randint(0x00, 0xff),
                    random.randint(0x00, 0xff),
                    random.randint(0x00, 0xff),
                    random.randint(0x00, 0xff)
                )
                status_messages.append(f"[yellow]New MAC: [bold]{new_mac}[/bold][/yellow]")
                live.update(generate_display(debug_messages, status_messages))
            
            # 4. Execution with live progress
                commands = []
                if platform.system() in ['Linux', 'Darwin']:
                    commands = [
                        f"ifconfig {interface} down",
                        f"ifconfig {interface} hw ether {new_mac}",
                        f"ifconfig {interface} up",
                        f"dhclient -r {interface}",
                        f"dhclient {interface}"
                    ]
                elif platform.system() == 'Windows':
                    interface_key = interface.split('_')[-1]
                    commands = [
                        f'netsh interface set interface \"{interface}\" admin=disable',
                        rf'reg add HKLM\SYSTEM\CurrentControlSet\Control\Class'
                        rf'\{{4D36E972-E325-11CE-BFC1-08002BE10318}}'
                        rf'\{interface_key} /v NetworkAddress /d {new_mac} /f',
                        f'netsh interface set interface \"{interface}\" admin=enable'
                    ]
            
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    BarColumn(),
                    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                    transient=True
                ) as progress:
                    task = progress.add_task("Changing MAC...", total=len(commands)*100)
                
                    for i, cmd in enumerate(commands):
                        debug_messages.append(f"Executing: {cmd}")
                        live.update(generate_display(debug_messages, status_messages))
                    
                        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                    
                        for step in range(100):
                            progress.update(task, advance=1, 
                                        description=f"{cmd[:20]}...")
                            time.sleep(0.01)
                            if step % 10 == 0:
                                live.update(generate_display(debug_messages, status_messages))
                    
                        if result.returncode != 0:
                            debug_messages.append(f"Error: {result.stderr.strip()}")
                            live.update(generate_display(debug_messages, status_messages))
            
            # 5. Verification
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    transient=True
                ) as progress:
                    task = progress.add_task("Verifying...", total=100)
                    for i in range(100):
                        progress.update(task, advance=1)
                        time.sleep(0.02)
                        if i % 10 == 0:
                            live.update(generate_display(debug_messages, status_messages))
            
                verification_passed = False
                if platform.system() in ['Linux', 'Darwin']:
                    result = subprocess.run(f"ifconfig {interface}",
                                        shell=True,
                                        capture_output=True,
                                        text=True)
                    verification_passed = new_mac.lower() in result.stdout.lower()
                elif platform.system() == 'Windows':
                    result = subprocess.run("getmac /v /fo csv",
                                        shell=True,
                                        capture_output=True,
                                        text=True)
                    verification_passed = new_mac.lower() in result.stdout.lower()
            
                if verification_passed:
                    status_messages.append("[bold green]✓ MAC changed successfully![/bold green]")
                else:
                    status_messages.append("[yellow]⚠ MAC changed but verification failed[/yellow]")
                    debug_messages.append("Note: Some systems require restart for verification")
            
            # Final output
                live.update(generate_display(debug_messages, status_messages))
                console.print("\n[bold]Press Enter to continue...[/bold]", end="")
                
                input()
            
        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/red]")
            debug_messages.append(f"Failed: {str(e)}")
            console.print(generate_display(debug_messages, status_messages))
            console.print("\n[bold]Press Enter to continue...[/bold]", end="")
            input()

        # end here macspoof
    def sql_injection_scan(self, url=None):
        """Interactive SQL injection scanner with cinematic animations"""
        console = Console()
    
    # Animation frames
        SQL_FRAMES = [
            "SELECT * FROM users",
            "UNION SELECT 1,2,3",
            "1' OR '1'='1",
            "WAITFOR DELAY '0:0:5'",
            "CONVERT(int,@@version)"
        ]

    # Get URL if not provided
        if not url:
            url = console.input("\n[bold cyan]Enter target URL (with http://): [/]").strip()
    
        if not url.startswith(("http://", "https://")):
            console.print(Panel(
                "[red]Invalid URL format! Must include http:// or https://[/red]",
                title="Input Error",
                border_style="red"
            ))
            return

    # Check sqlmap installation
        if not which("sqlmap"):
            console.print(Panel(
                "[red]sqlmap not found![/red]\n\n"
                "Install with:\n"
                "[green]git clone --depth 1 https://github.com/sqlmapproject/sqlmap.git[/green]\n\n"
                "Or visit: [blue]https://sqlmap.org[/blue]",
                title="Dependency Missing",
                border_style="red"
            ))
            return

    # Prepare display panels
        def create_panel(content, title="", border_style="blue"):
            return Panel(
                content,
                title=title,
                border_style=border_style,
                width=50,
                padding=(1, 1)
            )

    # Main display generator
        def generate_display(scan_log, status_msg, animation_frame):
            log_panel = create_panel(
                "\n".join(scan_log[-5:]),
                title="[blue]SCAN LOG[/blue]",
                border_style="blue"
            )
        
            status_panel = create_panel(
                status_msg,
                title="[green]STATUS[/green]",
                border_style="green"
            )
        
            anim_panel = create_panel(
                animation_frame,
                title="[red]SQL INJECTION[/red]",
                border_style="red"
            )
        
            return Columns([log_panel, status_panel, anim_panel])

        scan_log = []
        status_msg = "Initializing scan..."
        current_frame = random.choice(SQL_FRAMES)

    # Prepare sqlmap command
        report_dir = "./sqlmap_reports"
        os.makedirs(report_dir, exist_ok=True)
    
        cmd = [
            "sqlmap",
            "-u", url,
            "--batch",
            "--risk=3",
            "--level=3",
            "--crawl=1",
            "--random-agent",
            "--output-dir", report_dir
        ]

        try:
            with Live(generate_display(scan_log, status_msg, current_frame), 
                    console=console, 
                    refresh_per_second=10,
                    transient=False) as live:
            
            # Start scan with progress animation
                scan_log.append(f"Starting scan on: {url}")
                status_msg = "[yellow]Scanning target...[/yellow]"
            
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    BarColumn(),
                    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                    transient=True
                ) as progress:
                    task = progress.add_task("[cyan]Testing parameters", total=100)
                
                # Run sqlmap in background
                    process = subprocess.Popen(
                        cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        universal_newlines=True
                    )
                
                # Animate while scanning
                    frame_counter = 0
                    while process.poll() is None:
                        frame_counter += 1
                        if frame_counter % 5 == 0:
                            current_frame = random.choice(SQL_FRAMES)
                    
                    # Update progress
                        progress.update(task, advance=0.5)
                        if progress.tasks[0].percentage >= 100:
                            progress.update(task, completed=99)
                    
                    # Read output
                        line = process.stdout.readline()
                        if line:
                            if "testing" in line.lower():
                                status_msg = f"[yellow]{line.strip()}[/yellow]"
                            scan_log.append(line.strip())
                    
                        live.update(generate_display(scan_log, status_msg, current_frame))
                        time.sleep(0.1)
                
                    progress.update(task, completed=100)
            
            # Process results
                status_msg = "[green]Scan completed![/green]"
                live.update(generate_display(scan_log, status_msg, current_frame))
            
            # Parse vulnerabilities
                vulns = []
                report_file = os.path.join(report_dir, url.replace("://", "_").replace("/", "_"), "log")
                if os.path.exists(report_file):
                    with open(report_file, "r") as f:
                        for line in f:
                            if any(x in line for x in ["injectable", "vulnerable", "payload:"]):
                                vulns.append(line.strip())
            
            # Show results
                if vulns:
                    status_msg = "[red]VULNERABILITIES FOUND![/red]"
                    scan_log.extend([""] + vulns[-3:] + [f"\nFull report: {report_file}"])
                else:
                    status_msg = "[green]No vulnerabilities found[/green]"
            
                live.update(generate_display(scan_log, status_msg, current_frame))
                console.print("\n[bold]Press Enter to continue...[/]", end="")
                input()
            
        except Exception as e:
            console.print(Panel(
                f"[red]Error: {str(e)}[/red]",
                title="Scan Failed",
                border_style="red"
            ))
            console.print("\n[bold]Press Enter to continue...[/]", end="")
            input()
 
    # ==================== UTILITY METHODS ====================
 

    def clear_logs(self):
        """Securely clear system logs with admin verification and visual feedback"""
        console = Console()

        def create_panel(content, title="", border_style="blue"):
            return Panel(
                content,
                title=title,
                border_style=border_style,
                width=60,
                padding=(1, 1)
            )

    # Verify admin privileges first
        if not self.is_admin():
            console.print(
                create_panel(
                    "[red]✖ Requires administrator privileges[/red]",
                    title="Access Denied",
                    border_style="red"
                )
            )
            return

        try:
            with Progress(transient=True) as progress:
                task = progress.add_task("[cyan]Clearing system logs...", total=100)

            # Animated clearing process
                for i in range(5):
                    progress.update(task, advance=20, description=f"[cyan]Clearing {['event','application','security','setup','system'][i]} logs...")
                    time.sleep(0.5)

            # Actual log clearing commands
                if platform.system() == "Windows":
                    logs_cleared = []
                    for log_type in ["Application", "System", "Security"]:
                        result = os.system(f"wevtutil cl {log_type}")
                        if result == 0:
                            logs_cleared.append(log_type)
                    progress.update(task, completed=100)
                
                    console.print(
                        create_panel(
                            f"[green]✔ Cleared Windows logs: {', '.join(logs_cleared)}[/green]",
                            title="Success",
                            border_style="green"
                        )
                    )

                else:  # Linux/Mac
                    try:
                        os.system("sudo rm -rf /var/log/*")
                        os.system("sudo journalctl --vacuum-time=1s")
                        progress.update(task, completed=100)
                        console.print(
                            create_panel(
                                "[green]✔ Cleared system logs successfully[/green]",
                                title="Success",
                                border_style="green"
                            )
                        )
                    except Exception as e:
                        progress.update(task, visible=False)
                        console.print(
                            create_panel(
                                f"[red]✖ Error clearing logs: {str(e)}[/red]",
                                title="Error",
                                border_style="red"
                            )
                        )

        except Exception as e:
            console.print(
                create_panel(
                    f"[red]✖ Critical error: {str(e)}[/red]",
                    title="Operation Failed",
                    border_style="red"
                )
            )


# FINANCIAL SECTION
    def financial_simulator(self):
        """Interactive financial attack simulator with real-time money transfer animations"""
        console = Console()
    
    # Financial database
        BANKS = {
            "SWIFT": ["JPMorgan", "HSBC", "BankofAmerica", "StandardChartered"],
            "Crypto": ["Binance", "Coinbase", "Kraken"],
            "Payment": ["Visa", "Mastercard", "PayPal"]
        }

        def create_panel(content, title="", border_style="blue", width=40):
            return Panel(
                content,
                title=title,
                border_style=border_style,
                width=width,
                padding=(1, 1)
            )

    # Animation frames for money transfer
        MONEY_FRAMES = [
            "▁▂▃▄▅▆▇█",
            "▁▂▃▄▅▆▇▆▅▄▃▂▁",
            "←══════✪══════→",
            "▰▰▰▰▰▰▰▰▰▰",
            "[green]$$$[/][yellow]$$[/][red]$$[/]"
        ]

    # Get user input
        console.print(Panel.fit("[bold red]FINANCIAL SIMULATOR[/]", border_style="red"))
    
    # Bank selection
        bank_type = console.input("\n[bold cyan]Enter bank type (SWIFT/Crypto/Payment): [/]").strip()
        if bank_type not in BANKS:
            console.print(Panel("[red]Invalid bank type![/]", border_style="red"))
            return
    
        bank = random.choice(BANKS[bank_type])
        amount = console.input("[bold cyan]Enter amount to transfer: [/]").strip()
        recipient = console.input("[bold cyan]Enter recipient account: [/]").strip()

    # Transaction simulation
        try:
            layout = Layout()
            layout.split(
                Layout(name="header", size=3),
                Layout(name="main", ratio=1),
                Layout(name="footer", size=7)
            )
        
        # Create panels
            transaction_panel = create_panel(
                f"[bold]From:[/] DSTerminal_Acct\n"
                f"[bold]To:[/] {recipient}\n"
                f"[bold]Bank:[/] {bank}\n"
                f"[bold]Amount:[/] [green]{amount}[/]",
                title="[blue]TRANSACTION[/]",
                border_style="blue",
                width=45
            )
        
            network_panel = create_panel(
                f"[bold]Network:[/] {bank_type}\n"
                f"[bold]Status:[/] [yellow]Pending[/]\n"
                f"[bold]Fee:[/] ${random.uniform(0.1, 5.0):.2f}",
                title="[yellow]NETWORK[/]",
                border_style="yellow",
                width=45
            )

        # Animation function
            def generate_frame(frame_num):
                animation = MONEY_FRAMES[frame_num % len(MONEY_FRAMES)]
                return create_panel(
                    f"\n\n[bold]{animation}[/]\n\n"
                    f"[dim]Encrypting transaction...[/]",
                    title="[red]TRANSFER IN PROGRESS[/]",
                    border_style="red",
                    width=50
                )

        # Live progress display
            with Live(layout, refresh_per_second=10, screen=True) as live:
            # Header
                layout["header"].update(
                    Panel.fit(
                        f"[bold]Simulating {bank_type} Transfer[/] → [green]{amount}[/]",
                        border_style="green"
                    )
                )
            
            # Main content
                layout["main"].update(Columns([transaction_panel, network_panel]))
            
            # Animated transfer
                for i in range(1, 101):
                    layout["footer"].update(generate_frame(i))
                
                # Update status at different stages
                    if i == 30:
                        network_panel.border_style = "green"
                        network_panel.title = "[green]NETWORK[/]"
                        network_panel.renderable = network_panel.renderable.replace(
                            "[yellow]Pending[/]", 
                            "[green]Processing[/]"
                        )
                
                    if i == 70:
                        network_panel.renderable = network_panel.renderable.replace(
                            "[green]Processing[/]", 
                            "[blue]Verifying[/]"
                        )
                
                    time.sleep(0.08)
                    live.refresh()

            # Completion
                layout["footer"].update(
                    create_panel(
                        f"[bold green]✓ TRANSFER COMPLETE[/]\n\n"
                        f"[dim]Confirmation: DST-{random.randint(10000,99999)}[/]",
                        title="[green]SUCCESS[/]",
                        border_style="green",
                        width=50
                    )
                )
                network_panel.renderable = network_panel.renderable.replace(
                    "[blue]Verifying[/]", 
                    "[green]Completed[/]"
                )
                live.refresh()
                time.sleep(2)

        # Generate report
            console.print(Panel(
                f"[bold]Transaction Report[/]\n\n"
                f"• Amount: [green]{amount}[/]\n"
                f"• Bank: {bank}\n"
                f"• Recipient: {recipient}\n"
                f"• Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"• Network: {bank_type}\n"
                f"• Status: [green]Verified[/]",
                title="Receipt",
                border_style="bright_white"
            ))

        except KeyboardInterrupt:
            console.print(Panel("[yellow]Transfer cancelled by user[/]", border_style="yellow"))
    
        console.print("\n[bold]Press Enter to return to menu...[/]", end="")
        input()

# FINANCIAL SECTION ENDS HERE
    def check_integrity(self):
        """Check system file integrity"""
        print("\n[+] Checking critical system files...")
        critical_files = {
            "Windows": ["C:\\Windows\\System32\\kernel32.dll", "C:\\Windows\\System32\\cmd.exe"],
            "Linux": ["/bin/bash", "/usr/bin/sudo"],
            "Darwin": ["/bin/bash", "/usr/bin/sudo"]
        }
        
        os_type = platform.system()
        for file in critical_files.get(os_type, []):
            if os.path.exists(file):
                size = os.path.getsize(file)
                mtime = datetime.fromtimestamp(os.path.getmtime(file)).strftime('%Y-%m-%d %H:%M:%S')
                print(f"  {file} - Size: {size} bytes, Modified: {mtime}")
            else:
                print(f"  [!] Missing critical file: {file}")

    def show_crypto_status(self):
        """Show encryption system status"""
        print("\n🔐 ENCRYPTION SYSTEM STATUS")
        print("="*40)
    
        key_file = os.path.expanduser("~/.dsterminal_key")
    
        if os.path.exists(key_file):
            with open(key_file, 'r') as f:
                key = f.read().strip()
                key_id = hashlib.sha256(key.encode()).hexdigest()[:16]
        
            print(f"✅ Encryption: ENABLED")
            print(f"🔑 Key ID: {key_id}")
            print(f"📁 Key file: {key_file}")
        
        # Test cipher
            try:
                Fernet(key.encode())
                print("🔒 Key status: VALID")
            except:
                print("🔒 Key status: INVALID")
        else:
            print("❌ Encryption: NOT CONFIGURED")
            print("   Run 'encrypt-setup' to configure")
    
        print(f"\n📊 Cipher initialized: {'✅' if self.cipher else '❌'}")
        print(f"📁 VFS root: {self.vfs_root}")

    def encrypt_file(self, file_path):
        """Encrypt a file using AES-256 with enhanced features"""
        # Resolve path
        resolved_path = self.resolve_path(file_path)
        if not resolved_path:
            print(f"[!] File '{file_path}' not found in VFS or current directory")
            self.show_vfs_files()
            return
        
        if not self.cipher:
            print("[!] Encryption not initialized. Run 'encrypt-init' first.")
            return
        
        try:
            print(f"\n{'='*50}")
            print(f"🔒 ENCRYPTING: {os.path.basename(resolved_path)}")
            print(f"{'='*50}")
            
            # Get file info
            file_size = os.path.getsize(resolved_path)
            print(f"📁 File size: {self.human_readable_size(file_size)}")
            
            # Confirm encryption
            confirm = input("\n⚠️  Confirm encryption? (y/N): ").lower()
            if confirm != 'y':
                print("[*] Encryption cancelled")
                return
            
            # Read and encrypt
            with open(resolved_path, 'rb') as f:
                data = f.read()
            
            print("[+] Encrypting data...")
            encrypted = self.cipher.encrypt(data)
            
            # Save encrypted file
            encrypted_path = resolved_path + '.enc'
            with open(encrypted_path, 'wb') as f:
                f.write(encrypted)
            
            # Calculate hash
            file_hash = hashlib.sha256(data).hexdigest()
            enc_hash = hashlib.sha256(encrypted).hexdigest()
            
            # Secure delete original (optional)
            secure_delete = input("\n🗑️  Securely delete original file? (y/N): ").lower()
            if secure_delete == 'y':
                self.secure_delete(resolved_path)
                print("[+] Original file securely deleted")
            else:
                os.remove(resolved_path)
                print("[+] Original file deleted")
            
            print(f"\n{'✓'*50}")
            print("✅ ENCRYPTION SUCCESSFUL")
            print(f"{'✓'*50}")
            print(f"\n📄 Encrypted file: {os.path.basename(encrypted_path)}")
            print(f"📁 Location: {encrypted_path}")
            print(f"🔑 Key ID: {hashlib.sha256(CONFIG['ENCRYPT_KEY'].encode()).hexdigest()[:16]}")
            print(f"📊 Original hash: {file_hash[:32]}...")
            print(f"📊 Encrypted hash: {enc_hash[:32]}...")
            print(f"💾 Size increase: {len(encrypted) - file_size} bytes")
            print(f"\n⚠️  IMPORTANT: Keep your key safe! Without it, files cannot be decrypted.")
            print("   Store key in secure location.")
            
        except Exception as e:
            print(f"\n{'✗'*50}")
            print(f"❌ ENCRYPTION FAILED: {e}")
            print(f"{'✗'*50}")
    
    def decrypt_file(self, file_path, key=None):
        """Decrypt a file with enhanced features"""
        # Check if file has .enc extension
        if not file_path.endswith('.enc'):
            # Try with .enc extension
            enc_path = self.resolve_path(file_path + '.enc')
            if enc_path:
                file_path = file_path + '.enc'
            else:
                print("[!] File must have .enc extension or be found with it")
                return
        
        resolved_path = self.resolve_path(file_path)
        if not resolved_path:
            print(f"[!] File '{file_path}' not found")
            return
        
        try:
            print(f"\n{'='*50}")
            print(f"🔓 DECRYPTING: {os.path.basename(resolved_path)}")
            print(f"{'='*50}")
            
            # Get file info
            file_size = os.path.getsize(resolved_path)
            print(f"📁 Encrypted size: {self.human_readable_size(file_size)}")
            
            # Check if we have the key
            if not self.cipher:
                print("[!] No encryption key available")
                key_option = input("Enter key manually? (y/N): ").lower()
                if key_option == 'y':
                    key = getpass("🔑 Enter decryption key: ")
                    self.cipher = Fernet(key.encode())
                else:
                    print("[*] Decryption cancelled")
                    return
            
            # Confirm decryption
            confirm = input("\n⚠️  Confirm decryption? (y/N): ").lower()
            if confirm != 'y':
                print("[*] Decryption cancelled")
                return
            
            # Read and decrypt
            with open(resolved_path, 'rb') as f:
                encrypted = f.read()
            
            print("[+] Decrypting data...")
            decrypted = self.cipher.decrypt(encrypted)
            
            # Save decrypted file
            output_name = os.path.basename(resolved_path).replace('.enc', '')
            output_path = os.path.join(os.path.dirname(resolved_path), output_name)
            
            # Check if file already exists
            if os.path.exists(output_path):
                overwrite = input(f"\n⚠️  File '{output_name}' already exists. Overwrite? (y/N): ").lower()
                if overwrite != 'y':
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    output_name = f"{output_name}_{timestamp}"
                    output_path = os.path.join(os.path.dirname(resolved_path), output_name)
            
            with open(output_path, 'wb') as f:
                f.write(decrypted)
            
            # Verify decryption
            dec_hash = hashlib.sha256(decrypted).hexdigest()
            
            print(f"\n{'✓'*50}")
            print("✅ DECRYPTION SUCCESSFUL")
            print(f"{'✓'*50}")
            print(f"\n📄 Decrypted file: {output_name}")
            print(f"📁 Location: {output_path}")
            print(f"📊 File hash: {dec_hash}")
            print(f"💾 Size: {len(decrypted)} bytes")
            
            # Option to delete encrypted file
            delete_enc = input("\n🗑️  Delete encrypted file? (y/N): ").lower()
            if delete_enc == 'y':
                os.remove(resolved_path)
                print("[+] Encrypted file deleted")
            
        except Exception as e:
            print(f"\n{'✗'*50}")
            print(f"❌ DECRYPTION FAILED: {e}")
            print(f"{'✗'*50}")
            print("\nPossible issues:")
            print("1. Wrong encryption key")
            print("2. File corrupted")
            print("3. File not encrypted with this system")
    
    def human_readable_size(self, size):
        """Convert bytes to human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} PB"
    
    def secure_delete(self, file_path, passes=3):
        """Securely delete a file by overwriting it"""
        try:
            file_size = os.path.getsize(file_path)
            with open(file_path, 'wb') as f:
                for i in range(passes):
                    f.write(os.urandom(file_size))
                    f.flush()
                    os.fsync(f.fileno())
            os.remove(file_path)
            return True
        except:
            return False
    
    def show_vfs_files(self):
        """Show files in virtual filesystem"""
        print("\n📁 Virtual Filesystem Contents:")
        print("-" * 40)
        
        if not os.path.exists(self.vfs_root):
            print("VFS not initialized")
            return
        
        for item in os.listdir(self.vfs_root):
            item_path = os.path.join(self.vfs_root, item)
            if os.path.isfile(item_path):
                size = os.path.getsize(item_path)
                print(f"📄 {item:30} {self.human_readable_size(size):>10}")
            else:
                print(f"📁 {item}/")
    
    def handle_encrypt_test(self, args=None):
        """Test encryption system with a sample file"""
        if args is None:
            args = []
        print("\n🧪 ENCRYPTION SYSTEM TEST")
        print("="*60)
    
        try:
        # Create test file
            test_file = os.path.join(self.vfs_root, "test_encrypt.txt")
            with open(test_file, 'w') as f:
                f.write("This is a test file for encryption validation.\n")
                f.write(f"Timestamp: {datetime.now()}\n")
                f.write(f"Random data: {os.urandom(16).hex()}\n")
        
            print(f"[+] Created test file: {test_file}")
            print(f"[+] File size: {os.path.getsize(test_file)} bytes")
        
        # Test encryption
            print("\n[1] Testing encryption...")
            self.encrypt_file("test_encrypt.txt")
        
        # Check encrypted file exists
            enc_file = test_file + '.enc'
            if os.path.exists(enc_file):
                print(f"[+] Encrypted file created: {enc_file}")
                print(f"[+] Encrypted size: {os.path.getsize(enc_file)} bytes")
            
            # Test decryption
                print("\n[2] Testing decryption...")
            # Temporarily rename to avoid conflict
                temp_enc = enc_file + ".test"
                shutil.copy(enc_file, temp_enc)
            
            # Decrypt
                self.decrypt_file("test_encrypt.txt.enc.test")
            
            # Cleanup
                for f in [test_file, enc_file, temp_enc]:
                    if os.path.exists(f):
                        os.remove(f)
            
                print("\n✅ ENCRYPTION TEST PASSED")
                print("   All encryption/decryption operations completed successfully")
            else:
                print("[!] Encryption test failed - no encrypted file created")
            
        except Exception as e:
            print(f"\n❌ ENCRYPTION TEST FAILED: {e}")
            print("   Check your encryption system setup")
    
    def handle_decrypt(self, args):
        """Handle decrypt command"""
        if not args:
            file_path = input("File to decrypt: ")
            key = None
        elif len(args) == 1:
            file_path = args[0]
            key = None
        else:
            file_path = args[0]
            key = args[1]
        
        self.decrypt_file(file_path, key)
    
    def handle_encryption_setup(self, args):
        """Setup encryption system"""
        print("\n🔐 ENCRYPTION SYSTEM SETUP")
        print("="*40)
        
        key_file = os.path.expanduser("~/.dsterminal_key")
        
        if os.path.exists(key_file):
            print("[+] Encryption key already exists")
            print(f"[+] Key file: {key_file}")
            
            with open(key_file, 'r') as f:
                key = f.read().strip()
                key_id = hashlib.sha256(key.encode()).hexdigest()[:16]
                print(f"[+] Key ID: {key_id}")
            
            print("\nOptions:")
            print("1. Use existing key")
            print("2. Generate new key (WARNING: Old encrypted files won't be decryptable)")
            print("3. Import key from file")
            
            choice = input("\nSelect option (1-3): ")
            
            if choice == '2':
                # Generate new key
                new_key = Fernet.generate_key().decode()
                backup = input("\nBackup old key? (y/N): ").lower()
                if backup == 'y':
                    backup_path = key_file + ".backup"
                    with open(backup_path, 'w') as f:
                        f.write(key)
                    print(f"[+] Old key backed up to {backup_path}")
                
                with open(key_file, 'w') as f:
                    f.write(new_key)
                print("[+] New key generated")
                self.init_cipher()
                
            elif choice == '3':
                import_path = input("Path to key file: ")
                if os.path.exists(import_path):
                    with open(import_path, 'r') as f:
                        imported_key = f.read().strip()
                    
                    # Test key
                    try:
                        Fernet(imported_key.encode())
                        with open(key_file, 'w') as f:
                            f.write(imported_key)
                        print("[+] Key imported successfully")
                        self.init_cipher()
                    except:
                        print("[!] Invalid key format")
                else:
                    print("[!] Key file not found")
        else:
            # Generate new key
            print("[+] Generating new encryption key...")
            key = Fernet.generate_key().decode()
            
            with open(key_file, 'w') as f:
                f.write(key)
            
            os.chmod(key_file, 0o600)
            print(f"[+] Key saved to {key_file}")
            print(f"[+] Key ID: {hashlib.sha256(key.encode()).hexdigest()[:16]}")
            print("\n⚠️  IMPORTANT: Backup this key file! Without it, encrypted files cannot be recovered.")
            
            self.init_cipher()
        
        print("\n✅ Encryption system ready")

# encryptions ends below-------------------

    def handle_encrypted_files(self, args=None):
        """Show all encrypted files in the system"""
        if args is None:
            args= []
        print("\n🔐 ENCRYPTED FILES INVENTORY")
        print("="*60)
    
        encrypted_files = []
    
    # Search for .enc files in current directory and subdirectories
        for root, dirs, files in os.walk(self.current_dir):
            for file in files:
                if file.endswith('.enc'):
                    full_path = os.path.join(root, file)
                    size = os.path.getsize(full_path)
                    rel_path = os.path.relpath(full_path, self.current_dir)
                
                    encrypted_files.append({
                        'name': file,
                        'path': rel_path,
                        'full_path': full_path,
                        'size': size,
                        'modified': os.path.getmtime(full_path)
                    })
    
        if not encrypted_files:
            print("No encrypted files found.")
            print("\n💡 To encrypt a file: encrypt <filename>")
            return
        
        print(f"Found {len(encrypted_files)} encrypted file(s):\n")
    
        for i, ef in enumerate(encrypted_files, 1):
            mod_time = datetime.fromtimestamp(ef['modified']).strftime('%Y-%m-%d %H:%M')
            original_name = ef['name'].replace('.enc', '')
        
            print(f"{i:2}. 🔒 {ef['name']:25}")
            print(f"    📁 {ef['path']}")
            print(f"    📊 {self.human_readable_size(ef['size']):>10}  📅 {mod_time}")
            print(f"    🔓 Original: {original_name}")
            print()
    
        print("="*60)
        print("Commands:")
        print("  decrypt <filename.enc>    - Decrypt a file")
        print("  crypto-info <filename.enc> - Show encryption info")
        print("  crypto-verify             - Verify encryption system")

    def handle_crypto_info(self, args=None):
        """Show information about an encrypted file"""
        if args is None:
            args = []
        if not args:
            print("[!] Usage: crypto-info <filename.enc>")
            return
    
        filename = args[0]
        if not filename.endswith('.enc'):
            filename += '.enc'
    
        filepath = self.resolve_file_path(filename)
        if not filepath or not os.path.exists(filepath):
            print(f"[!] File '{filename}' not found")
            return
    
        try:
            print(f"\n🔐 ENCRYPTION INFORMATION")
            print("="*60)
        
        # File stats
            size = os.path.getsize(filepath)
            modified = datetime.fromtimestamp(os.path.getmtime(filepath))
            created = datetime.fromtimestamp(os.path.getctime(filepath))
        
            print(f"📄 File: {os.path.basename(filepath)}")
            print(f"📁 Path: {filepath}")
            print(f"📊 Size: {self.human_readable_size(size)}")
            print(f"📅 Created: {created.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"📅 Modified: {modified.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Read encrypted data
            with open(filepath, 'rb') as f:
                encrypted_data = f.read()
        
        # Calculate hash
            file_hash = hashlib.sha256(encrypted_data).hexdigest()
        
            print(f"🔢 SHA-256: {file_hash}")
            print(f"🔢 MD5: {hashlib.md5(encrypted_data).hexdigest()}")
        
        # Try to detect encryption type
            print(f"\n🔍 Encryption Analysis:")
        
        # Check if it's Fernet encrypted
            try:
            # Fernet tokens are URL-safe base64 encoded
                import base64
                decoded = base64.urlsafe_b64decode(encrypted_data)
                if len(decoded) > 0:
                    print("  ✅ Appears to be Fernet encrypted (AES-256)")
                
                # Try to get timestamp from Fernet token
                    if len(encrypted_data) > 50:
                        try:
                            from cryptography.fernet import Fernet
                        # Just checking format, not actually decrypting
                            Fernet(b'0'*44).decrypt(encrypted_data, ttl=0)
                            print("  ✅ Valid Fernet token format")
                        except:
                            print("  ⚠️  Fernet format but invalid token")
                else:
                    print("  ⚠️  Unknown encryption format")
            except:
                print("  ⚠️  Unknown encryption format")
        
        # Show first few bytes in hex
            print(f"\n📊 First 32 bytes (hex):")
            hex_dump = ' '.join(f'{b:02x}' for b in encrypted_data[:32])
            print(f"  {hex_dump}")
        
            if len(encrypted_data) > 32:
                print(f"  ... (truncated)")
        
        # Check if original file exists
            original_path = filepath.replace('.enc', '')
            if os.path.exists(original_path):
                print(f"\n⚠️  WARNING: Original file still exists!")
                print(f"   {original_path}")
                print("   Consider deleting it for security.")
        
            print(f"\n💡 To decrypt: decrypt {os.path.basename(filepath)}")
        
        except Exception as e:
            print(f"[!] Error analyzing file: {e}")

    def handle_crypto_verify(self, args=None):
        """Verify encryption system is working"""
        if args is None:
            args = []
        print("\n🔐 ENCRYPTION SYSTEM VERIFICATION")
        print("="*60)
    
    # Check key file
        key_file = os.path.expanduser("~/.dsterminal_key")
        if os.path.exists(key_file):
            print(f"✅ Key file found: {key_file}")
        
            with open(key_file, 'r') as f:
                key = f.read().strip()
                key_hash = hashlib.sha256(key.encode()).hexdigest()[:16]
        
            print(f"✅ Key ID: {key_hash}")
        
        # Check key format
            try:
                from cryptography.fernet import Fernet
                Fernet(key.encode())
                print("✅ Key format: VALID (44-character base64)")
            except:
                print("❌ Key format: INVALID")
        else:
            print("❌ Key file NOT found")
            print("   Run 'encrypt-setup' to create one")
            return
    
    # Check cipher initialization
        if self.cipher:
            print("✅ Cipher initialized: YES")
        else:
         print("❌ Cipher initialized: NO")
    
    # Test encryption/decryption
        print("\n🧪 Running self-test...")
    
        try:
            test_data = b"DSTerminal encryption test " + os.urandom(16)
        
        # Encrypt
            encrypted = self.cipher.encrypt(test_data)
        
        # Decrypt
            decrypted = self.cipher.decrypt(encrypted)
        
            if test_data == decrypted:
                print("✅ Self-test: PASSED")
                print(f"   Test data: {len(test_data)} bytes")
                print(f"   Encrypted: {len(encrypted)} bytes")
                print(f"   Overhead: {len(encrypted) - len(test_data)} bytes")
            else:
                print("❌ Self-test: FAILED - Decrypted data doesn't match")
            
        except Exception as e:
            print(f"❌ Self-test: FAILED - {e}")
    
    # Check for encrypted files
        enc_count = 0
        for root, dirs, files in os.walk(self.current_dir):
            for file in files:
                if file.endswith('.enc'):
                    enc_count += 1
    
        print(f"\n📊 Statistics:")
        print(f"Encrypted files in current dir: {enc_count}")
    
        print("\n✅ Encryption system is READY")

    def handle_crypto_backup(self, args=None):
        """Backup encryption key"""
        if args is None:
            args = []
        print("\n💾 ENCRYPTION KEY BACKUP")
        print("="*60)
    
        key_file = os.path.expanduser("~/.dsterminal_key")
    
        if not os.path.exists(key_file):
            print("[!] No encryption key found")
            print("[*] Run 'encrypt-setup' first")
            return
    
    # Read key
        with open(key_file, 'r') as f:
            key = f.read().strip()
    
        key_hash = hashlib.sha256(key.encode()).hexdigest()[:16]
    
        print(f"🔑 Key ID: {key_hash}")
        print(f"📁 Current key file: {key_file}")
    
        print("\n⚠️  WARNING: This key can decrypt ALL files encrypted with it!")
        print("   Store backups in secure locations (encrypted USB, password manager).")
    
        backup_option = input("\nBackup to: (1) File, (2) Print to screen, (3) QR code: ").strip()
    
        if backup_option == '1':
            backup_path = input("Backup file path [~/dsterminal_key.backup]: ").strip()
            if not backup_path:
                backup_path = os.path.expanduser("~/dsterminal_key.backup")
        
            with open(backup_path, 'w') as f:
                f.write(key)
        
        # Set secure permissions
            os.chmod(backup_path, 0o600)
        
            print(f"✅ Key backed up to: {backup_path}")
            print(f"📊 File size: {os.path.getsize(backup_path)} bytes")
        
        elif backup_option == '2':
            print("\n🔑 ENCRYPTION KEY (Keep this safe!):")
            print("="*40)
            print(key)
            print("="*40)
            print(f"\nKey ID: {key_hash}")
        
        elif backup_option == '3':
            try:
                import qrcode
                qr = qrcode.QRCode(version=1, box_size=10, border=5)
                qr.add_data(f"DSTerminal Key:{key}")
                qr.make(fit=True)
            
                img = qr.make_image(fill_color="black", back_color="white")
            
                qr_path = os.path.expanduser("~/dsterminal_key_qr.png")
                img.save(qr_path)
            
                print(f"✅ QR code saved to: {qr_path}")
                print("📱 Scan with a QR code reader to view key")
            
            except ImportError:
                print("[!] Install qrcode module: pip install qrcode[pil]")
    
        print("\n💡 Store backups in multiple secure locations!")
        print("   Without this key, encrypted files are LOST FOREVER.")
# ---------------------ends here---------------
    def watch_folder(self, path):
        """Monitor a folder for changes"""
        if not os.path.exists(path):
            print("[!] Path not found")
            return

        print(f"\n[+] Monitoring {path} for changes (Ctrl+C to stop)...")
        before = dict([(f, None) for f in os.listdir(path)])
        
        try:
            while True:
                time.sleep(5)
                after = dict([(f, None) for f in os.listdir(path)])
                added = [f for f in after if f not in before]
                removed = [f for f in before if f not in after]
                
                if added: print(f"  [+] Files added: {', '.join(added)}")
                if removed: print(f"  [-] Files removed: {', '.join(removed)}")
                
                before = after
        except KeyboardInterrupt:
            print("\n[+] Folder monitoring stopped")

    def trace_route(self, target):
        """Perform a traceroute to target"""
        print(f"\n[+] Tracing route to {target}...")
        try:
            if platform.system() == "Windows":
                os.system(f"tracert {target}")
            else:
                os.system(f"traceroute {target}")
        except Exception as e:
            print(f"[!] Error: {e}")

    def monitor_ransomware(self):
        """Check for ransomware indicators"""
        print("\n[+] Scanning for ransomware indicators...")
        suspicious_extensions = ['.encrypted', '.locked', '.crypt', '.ransom']
        found = False
        
        for root, _, files in os.walk('/' if platform.system() != 'Windows' else 'C:\\'):
            for file in files:
                if any(file.endswith(ext) for ext in suspicious_extensions):
                    print(f"  [!] Suspicious file: {os.path.join(root, file)}")
                    found = True
            if found:  # Prevent full disk scan
                break
        
        if not found:
            print("[+] No obvious ransomware files detected")

    def wifi_audit(self, interface):
        """Perform WiFi security audit"""
        if platform.system() != "Linux":
            print("[!] This command requires Linux")
            return

        print(f"\n[+] Auditing WiFi on {interface}...")
        try:
            result = subprocess.run(['iwconfig', interface], capture_output=True, text=True)
            print(result.stdout)
            
            if "unassociated" in result.stdout:
                print("[!] Interface not connected")
                return
                
            print("\n[+] Nearby access points:")
            subprocess.run(['sudo', 'iwlist', interface, 'scan'], check=True)
        except Exception as e:
            print(f"[!] Error: {e}")


    def _scan_bar(self, label, duration=10, width=30):
        """Animated progress bar for cinematic scanning"""
        sys.stdout.write(f"    ├─ {label}: ")
        sys.stdout.flush()
        steps = 20
        for i in range(steps):
            sys.stdout.write("█")
            sys.stdout.flush()
            time.sleep(duration / steps)
        print(" ✓")


    def check_steganography(self, image_path):
        """
        Perform non-invasive steganalysis checks on an image.
        Detection only – no extraction or execution.
        """

        if not os.path.exists(image_path):
            print("[!] Image not found")
            return

        try:
            print(f"\n[+] Loading image: {image_path}")
            time.sleep(2)

            file_size = os.path.getsize(image_path)
            print(f"[+] File size: {round(file_size / 1024, 2)} KB")
            time.sleep(2)

            with open(image_path, "rb") as f:
                content = f.read()

            print("\n[+] Performing steganalysis checks...")
            time.sleep(2)

        # --- Animated scan stages ---
            self._scan_bar("File structure inspection",duration=10)
            self._scan_bar("Signature scan", duration=10)
            self._scan_bar("Entropy evaluation", duration=10)
            self._scan_bar("LSB pattern sampling", duration=10)

            anomalies = []

        # --- Known steganography signatures (light detection) ---
            steg_signatures = {
                b"STEGO": "Generic steganography marker",
                b"Steghide": "Steghide tool reference",
                b"outguess": "OutGuess tool reference"
            }

            for sig, desc in steg_signatures.items():
                if sig.lower() in content.lower():
                    anomalies.append(f"Possible {desc}")

        # --- Entropy check (real forensic concept) ---
            byte_counts = Counter(content)
            entropy = 0.0

            for count in byte_counts.values():
                p = count / len(content)
                entropy -= p * math.log2(p)

            entropy = round(entropy, 2)

            if entropy > 7.5:
                anomalies.append("High entropy detected (possible embedded data)")

            time.sleep(3)

        # --- Result output ---
            if anomalies:
                print("\n[!] WARNING: Potential anomalies detected")
                for a in anomalies:
                    time.sleep(1.5)
                    print(f"    ├─ {a}")

                confidence = "MEDIUM" if len(anomalies) > 1 else "LOW"
                print(f"\n[+] Confidence level: {confidence}")
                print("[+] Recommendation: Manual forensic review advised")
            else:
                print("\n[✓] No obvious steganographic indicators detected")
                print("[+] Confidence level: LOW")
                print("[+] Image appears normal")

            time.sleep(2)
            print("\n[✓] Steganalysis completed successfully")

        except Exception as e:
            print(f"[!] Analysis error: {e}")
# certificate check impleme below

    def certcheck(self, domain=None):
        """
        DSTerminal SSL/TLS Certificate Checker with cinematic hacking animation.
        """
        try:
        # Prompt for domain if not provided
            if not domain:
                domain = input("\nEnter domain to check (e.g., starkexpo.com): ").strip()
                if not domain:
                    print("[!] No domain provided")
                    return

        # Cinematic header
            banner = """
            ████╗  █████╗  ██╔██╗ ██║█████╗   ╚███╔╝
            ██║  ██║██╔══╝  ██╔══╝  ██╔══╝  ██║╚██╗██║
            ██████╔╝██║     ██║     ███████╗██║ ╚████║
            ╚═════╝ ╚═╝     ╚═╝     ╚══════╝╚═╝  ╚═══╝
            """
            print(banner)
            print(f"\n[-- DFFENEX@DSTerminal ]-[] certcheck")
            time.sleep(0.5)

        # Stage animations for cinematic effect
            stages = [
                "Initializing SSL Inspection Engine",
                "Analyzing TLS Handshake",
                "Validating Certificate Chain",
                "Mapping Trust Relationships",
                "Running Risk Assessment Engine",
                "Generating Defense Recommendations"
            ]

            for stage in stages:
                self._loading_animation(stage, 5)  # 5 seconds per stage for cinematic pacing

        # Run the comprehensive SSL check
            self.check_ssl(domain)

            print(f"\n[-- DFFENEX@DSTerminal ]-[]")

        except Exception as e:
            print(f"[!] Certificate check failed: {e}")

    def check_ssl(self, domain=None):
        """Comprehensive SSL certificate analyzer with export options"""
        try:
            if not domain:
                domain = input("Enter domain to check (e.g., starkexpo.com): ").strip()
                if not domain:
                    print("[!] No domain provided")
                    return
        
        # Run cinematic scanning sequence
            self._animated_ssl_scan()
        
        # Configure enhanced SSL context
            context = ssl.create_default_context()
            context.check_hostname = True
            context.verify_mode = ssl.CERT_REQUIRED
            context.load_default_certs()
        
        # Set timeout and create connection
            socket.setdefaulttimeout(10)
        
            with socket.create_connection((domain, 443)) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert(binary_form=True)
                    x509 = ssl.DER_cert_to_PEM_cert(cert)
                    cert_obj = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, x509)
                
                # Get certificate details
                    peer_cert = ssock.getpeercert()
                    issuer = dict(x[0] for x in peer_cert['issuer'])
                    subject = dict(x[0] for x in peer_cert['subject'])
                    expires = datetime.strptime(peer_cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                    valid_days = (expires - datetime.now()).days
                
                # Get certificate chain using OpenSSL
                    chain = []
                    store = OpenSSL.crypto.X509Store()
                    store_ctx = OpenSSL.crypto.X509StoreContext(store, cert_obj)
                
                    try:
                        chain_result = store_ctx.get_verified_chain()
                        for i, chain_cert in enumerate(chain_result):
                            chain.append({
                                'subject': dict(chain_cert.get_subject().get_components()),
                                'issuer': dict(chain_cert.get_issuer().get_components()),
                                'expires': chain_cert.get_notAfter().decode('utf-8'),
                                'serial': chain_cert.get_serial_number(),
                                'version': chain_cert.get_version() + 1
                            })
                    except OpenSSL.crypto.X509StoreContextError:
                        chain.append({
                            'subject': dict(cert_obj.get_subject().get_components()),
                            'issuer': dict(cert_obj.get_issuer().get_components()),
                            'expires': cert_obj.get_notAfter().decode('utf-8'),
                            'serial': cert_obj.get_serial_number(),
                            'version': cert_obj.get_version() + 1
                        })
                
                # Check OCSP revocation status
                    ocsp_status = "Unknown"
                    if len(chain) > 1:
                        ocsp_status = self._check_ocsp(cert_obj, chain[1])
                
                # Print comprehensive report with animated table
                    self._print_ssl_report(domain, ssock, cert_obj, chain, ocsp_status, valid_days)
    
        except ssl.SSLError as e:
            self._cinematic_box(f"[!] SSL Error: {e}", seconds=2, error=True)
        except socket.timeout:
            self._cinematic_box("[!] Connection timed out", seconds=2, error=True)
        except ImportError as e:
            self._cinematic_box(f"[!] Required module missing: {str(e)}", seconds=3, error=True)
            print("[!] Please install pyOpenSSL: pip install pyopenssl")
        except Exception as e:
            self._cinematic_box(f"[!] Analysis failed: {str(e)}", seconds=2, error=True)

    def _cinematic_box(self, title, seconds=3, error=False):
        """Display a centered colored box with progress and flickering messages"""
        terminal_width = shutil.get_terminal_size((80, 20)).columns
        box_width = min(60, terminal_width - 10)
    
    # Center the box
        left_padding = (terminal_width - box_width - 2) // 2
    
    # Random colors or error color
        if error:
            colors = [Fore.RED, Fore.LIGHTRED_EX]
        else:
            colors = [Fore.GREEN, Fore.CYAN, Fore.MAGENTA, Fore.YELLOW, Fore.LIGHTGREEN_EX]
        color = random.choice(colors)
        blink = "\033[5m" if not error else ""
    
    # Clear line and create centered box
        sys.stdout.write("\033[K")  # Clear current line
    
    # Top border (centered)
        print(" " * left_padding + color + "┌" + "─" * box_width + "┐" + Style.RESET_ALL)
    
    # Title with blinking effect
        title_text = f"{blink}{title}{Style.RESET_ALL}" if not error else title
        print(" " * left_padding + color + "│" + Style.RESET_ALL + f" {title_text}".ljust(box_width + 1) + color + "│" + Style.RESET_ALL)
        print(" " * left_padding + color + "├" + "─" * box_width + "┤" + Style.RESET_ALL)
    
    # Animation inside box
        spinner = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]
        flickers = [
            "[SCANNING...]", "[TLS CHECK]", "[OCSP QUERY]", 
            "[CERT VERIFY]", "[RISK ASSESS]", "[CHAIN ANALYZE]",
            "[PROTOCOL SCAN]", "[CIPHER CHECK]", "[SIGNATURE VERIFY]"
        ]
        end_time = time.time() + seconds
        i = 0
    
        while time.time() < end_time:
            progress = int(((time.time() % seconds) / seconds) * (box_width - 10))
            bar = "█" * progress + "░" * (box_width - 10 - progress)
            flicker_text = random.choice(flickers)
        
        # Create the content line
            content = f"{spinner[i%len(spinner)]} {bar} {flicker_text}"
            content = content[:box_width-2].ljust(box_width-2)
        
        # Position cursor and update
            sys.stdout.write(f"\033[s")  # Save position
            sys.stdout.write(f"\033[{left_padding+1}G")  # Move to start of box content
            sys.stdout.write(color + "│" + Style.RESET_ALL + f" {content} " + color + "│" + Style.RESET_ALL)
            sys.stdout.write(f"\033[u")  # Restore position
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1
    
    # Bottom border (centered)
        print("\n" + " " * left_padding + color + "└" + "─" * box_width + "┘" + Style.RESET_ALL)
        sys.stdout.flush()

    def _animated_ssl_scan(self):
        """Run animated scanning stages"""
        stages = [
            "INITIALIZING SSL INSPECTION ENGINE",
            "ANALYZING TLS HANDSHAKE PROTOCOL",
            "VALIDATING CERTIFICATE CHAIN",
            "MAPPING TRUST RELATIONSHIPS",
            "RUNNING RISK ASSESSMENT ENGINE",
            "GENERATING DEFENSE RECOMMENDATIONS"
        ]
    
        terminal_width = shutil.get_terminal_size((80, 20)).columns
    
        for i, stage in enumerate(stages):
        # Clear screen effect between stages (optional)
            if i > 0:
                time.sleep(0.3)
        
            self._cinematic_box(stage, seconds=3)
        
        # Glitch effect between stages
            if i < len(stages) - 1:
                glitch_color = random.choice([Fore.GREEN, Fore.CYAN, Fore.MAGENTA])
                glitch_text = f"{glitch_color}[SYSTEM]{Style.RESET_ALL} Stage {i+1} complete..."
                print(" " * ((terminal_width - len(glitch_text) + 30) // 2) + glitch_text)
                time.sleep(0.2)

    def _animated_ssl_table(self, cert_data):
        """Display certificate info in colored, blinking table"""
        terminal_width = shutil.get_terminal_size((80, 20)).columns
        table_width = min(70, terminal_width - 10)
        left_padding = (terminal_width - table_width - 2) // 2
    
        colors = [Fore.GREEN, Fore.CYAN, Fore.MAGENTA, Fore.YELLOW, Fore.LIGHTGREEN_EX]
        blink = "\033[5m"
    
    # Clear screen area for table
        print("\n" * 2)
    
    # Top border with title
        print(" " * left_padding + Fore.CYAN + "╔" + "═" * table_width + "╗" + Style.RESET_ALL)
        title = "🔐 DSTERMINAL SSL/TLS SECURITY AUDIT 🔐"
        print(" " * left_padding + Fore.CYAN + "║" + Style.RESET_ALL + f"{blink}{Fore.LIGHTYELLOW_EX}{title:^{table_width}}{Style.RESET_ALL}" + Fore.CYAN + "║" + Style.RESET_ALL)
        print(" " * left_padding + Fore.CYAN + "╠" + "═" * table_width + "╣" + Style.RESET_ALL)
    
    # Table content with blinking effect
        for key, value in cert_data.items():
            color = random.choice(colors)
        
        # Format key with color and blink
            key_str = f"{color}{blink}{key.upper()}{Style.RESET_ALL}"
        
        # Format value based on type
            if isinstance(value, (int, float)):
                if value < 0:
                    value_str = f"{Fore.RED}{value}{Style.RESET_ALL}"
                elif value < 30:
                    value_str = f"{Fore.YELLOW}{value}{Style.RESET_ALL}"
                else:
                    value_str = f"{Fore.GREEN}{value}{Style.RESET_ALL}"
            elif "HIGH" in str(value) or "CRITICAL" in str(value):
                value_str = f"{Fore.RED}{blink}{value}{Style.RESET_ALL}"
            elif "MEDIUM" in str(value):
                value_str = f"{Fore.YELLOW}{value}{Style.RESET_ALL}"
            else:
                value_str = f"{Fore.WHITE}{value}{Style.RESET_ALL}"
        
        # Create row with proper spacing
            row = f" {key_str:<20} {value_str:<{table_width-23}}"
        
        # Print row with animation
            print(" " * left_padding + Fore.CYAN + "║" + Style.RESET_ALL + row + " " * (table_width - len(row) + 1) + Fore.CYAN + "║" + Style.RESET_ALL)
            time.sleep(0.1)  # Typing effect
    
    # Bottom border
        print(" " * left_padding + Fore.CYAN + "╚" + "═" * table_width + "╝" + Style.RESET_ALL)
    
    # Add status line
        status = f"{Fore.GREEN}[✓] SCAN COMPLETE • {datetime.now().strftime('%H:%M:%S')}{Style.RESET_ALL}"
        print(" " * ((terminal_width - len(status)) // 2) + status)

    def _print_ssl_report(self, domain, ssock, cert_obj, chain, ocsp_status, valid_days):
        """Enhanced SSL report with centered animated display"""
    
    # Stage 1-6: Animated scanning
        self._animated_ssl_scan()
    
    # Gather certificate data
        protocol = ssock.version()
        cipher = ssock.cipher()[0]
        sig_algo = cert_obj.get_signature_algorithm().decode()
    
    # Calculate risk level
        risk = 0
        if valid_days < 60:
            risk += 2
        if "SHA1" in sig_algo:
            risk += 3
        if protocol in ["TLSv1", "TLSv1.1"]:
            risk += 4
        if protocol != "TLSv1.3":
            risk += 1
        if ocsp_status != "VALID":
            risk += 2
    
        if risk == 0:
            level = "LOW"
            risk_color = Fore.GREEN
        elif risk <= 3:
            level = "MEDIUM"
            risk_color = Fore.YELLOW
        elif risk <= 6:
            level = "HIGH"
            risk_color = Fore.RED
        else:
            level = "CRITICAL"
            risk_color = Fore.RED + "\033[5m"  # Blinking red for critical
    
    # Prepare certificate data for table
        cert_data = {
            "domain": domain,
            "issuer": cert_obj.get_issuer().CN,
            "subject": cert_obj.get_subject().CN,
            "expires": f"{cert_obj.get_notAfter().decode()} ({valid_days} days)",
            "protocol": protocol,
            "cipher": cipher[:40] + "..." if len(cipher) > 40 else cipher,
            "signature": sig_algo,
            "ocsp status": ocsp_status,
            "risk level": f"{risk_color}{level}{Style.RESET_ALL}",
            "chain length": len(chain)
        }
    
    # Display animated table
        self._animated_ssl_table(cert_data)
    
    # Certificate chain display
        print("\n" + "═" * shutil.get_terminal_size().columns)
        chain_title = f"{Fore.CYAN}🔗 CERTIFICATE CHAIN ANALYSIS{Style.RESET_ALL}"
        print(chain_title.center(shutil.get_terminal_size().columns))
        print("═" * shutil.get_terminal_size().columns)
    
        for i, cert in enumerate(chain):
            indent = "  " * i
            subject = cert['subject'].get(b'CN', b'Unknown').decode()
            issuer = cert['issuer'].get(b'CN', b'Unknown').decode()
        
        # Color based on depth
            if i == 0:
                color = Fore.GREEN  # Leaf certificate
            elif i == len(chain) - 1:
                color = Fore.YELLOW  # Root certificate
            else:
                color = Fore.CYAN  # Intermediate
        
            print(f"{indent} {color}├─ {subject}{Style.RESET_ALL}")
            if i == 0:
                print(f"{indent}    Issuer: {issuer}")
                print(f"{indent}    Valid: {cert['expires'][:8]}")
    
    # Security assessment
        print("\n" + "═" * shutil.get_terminal_size().columns)
        assess_title = f"{Fore.MAGENTA}🛡️ SECURITY ASSESSMENT{Style.RESET_ALL}"
        print(assess_title.center(shutil.get_terminal_size().columns))
        print("═" * shutil.get_terminal_size().columns)
    
        warnings = []
        if valid_days < 60:
            warnings.append(f"{Fore.YELLOW}⚠ Certificate expires soon ({valid_days} days){Style.RESET_ALL}")
        if "SHA1" in sig_algo:
            warnings.append(f"{Fore.RED}✗ Weak signature algorithm (SHA-1){Style.RESET_ALL}")
        if protocol in ["TLSv1", "TLSv1.1"]:
            warnings.append(f"{Fore.RED}✗ Deprecated TLS protocol{Style.RESET_ALL}")
        if protocol != "TLSv1.3":
            warnings.append(f"{Fore.YELLOW}⚠ TLS 1.3 not enabled{Style.RESET_ALL}")
        if ocsp_status != "VALID":
            warnings.append(f"{Fore.YELLOW}⚠ OCSP revocation not verified{Style.RESET_ALL}")
    
        if warnings:
            for warning in warnings:
                print(f"  {warning}")
        else:
            print(f"  {Fore.GREEN}✓ No security issues detected{Style.RESET_ALL}")
    
    # Recommendations
        print("\n" + "═" * shutil.get_terminal_size().columns)
        rec_title = f"{Fore.BLUE}💡 RECOMMENDATIONS{Style.RESET_ALL}"
        print(rec_title.center(shutil.get_terminal_size().columns))
        print("═" * shutil.get_terminal_size().columns)
    
        if valid_days < 60:
            print(f"  {Fore.YELLOW}→ Renew SSL certificate immediately{Style.RESET_ALL}")
        if protocol != "TLSv1.3":
            print(f"  {Fore.CYAN}→ Upgrade server to support TLS 1.3{Style.RESET_ALL}")
        if ocsp_status != "VALID":
            print(f"  {Fore.CYAN}→ Enable OCSP stapling{Style.RESET_ALL}")
        if not warnings:
            print(f"  {Fore.GREEN}→ No action required. System secure.{Style.RESET_ALL}")
    
        print("\n" + "═" * shutil.get_terminal_size().columns)
    
    # Build report data
        data = {
            "domain": domain,
            "subject": cert_obj.get_subject().CN,
            "valid_days": valid_days,
            "protocol": ssock.version(),
            "cipher": ssock.cipher()[0],
            "ocsp": ocsp_status,
            "risk_level": level,
            "renewal_warning": valid_days < 60,
            "tls13": ssock.version() == "TLSv1.3",
            "scan_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "certificate": {
                "subject": {"CN": cert_obj.get_subject().CN},
                "issuer": {"CN": cert_obj.get_issuer().CN},
                "expires": cert_obj.get_notAfter().decode(),
                "serial": str(cert_obj.get_serial_number()),
                "signature": cert_obj.get_signature_algorithm().decode()
            },
            "security_profile": {
                "tls13": ssock.version() == "TLSv1.3",
                "ocsp": ocsp_status,
                "forward_secrecy": "ECDHE" in ssock.cipher()[0]
            }
        }
    
    # Export options
        choice = input(f"\n{Fore.CYAN}Export security report to file? (y/N): {Style.RESET_ALL}").lower()
        if choice == "y":
            self._export_ssl_results(domain, ssock, cert_obj, chain)
    
        pdf_choice = input(f"{Fore.CYAN}Generate PDF compliance report? (y/N): {Style.RESET_ALL}").lower()
        if pdf_choice == "y":
            self._generate_pdf_report(data)



    def _check_ocsp(self, cert, issuer_cert):
        """Check OCSP revocation status"""
        try:
            from cryptography.x509.oid import ExtensionOID
            from cryptography.hazmat.backends import default_backend
            from cryptography.x509 import load_pem_x509_certificate
            
            cert = load_pem_x509_certificate(
                OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
            )
        
            if issuer_cert:
                issuer = load_pem_x509_certificate(
                    OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, issuer_cert)
                )
                builder = OCSPRequestBuilder()
                builder = builder.add_certificate(cert, issuer)
                req = builder.build()
            
                ocsp_url = cert.extensions.get_extension_for_class(
                    cryptography.x509.AuthorityInformationAccess
                ).value.get_ocsp_urls()[0]
            
                response = requests.post(
                    ocsp_url,
                    data=req.public_bytes(serialization.Encoding.DER),
                    headers={'Content-Type': 'application/ocsp-request'}
                )
            
                return "REVOKED" if response.status == 1 else "VALID"
        except:
            return "Unknown"

    def _export_ssl_results(self, domain, ssock, cert_obj, chain):

        subject = self._bytes_to_str_dict(
            dict(cert_obj.get_subject().get_components())
        )

        issuer = self._bytes_to_str_dict(
            dict(cert_obj.get_issuer().get_components())
        )

        data = {
            "domain": domain,
            "scan_time": datetime.now().isoformat(),

            "protocol": ssock.version(),
            "cipher": ssock.cipher()[0],

            "certificate": {
                "subject": subject,
                "issuer": issuer,
                "expires": cert_obj.get_notAfter().decode(),
                "serial": str(cert_obj.get_serial_number()),
                "signature": cert_obj.get_signature_algorithm().decode()
            },

            "chain": self._clean_chain(chain),

            "security_profile": {
                "tls13": ssock.version() == "TLSv1.3",
                "ocsp": "checked",
                "forward_secrecy": "ECDHE" in ssock.cipher()[0]
            }
        }

        filename = f"dsterminal_ssl_{domain}_{datetime.now().strftime('%Y%m%d_%H%M')}.json"

        with open(filename, "w") as f:
            json.dump(data, f, indent=2)

        print(f"\n[✓] Encrypted audit report saved: {filename}")

    def _bytes_to_str_dict(self, data):
        """Convert bytes dictionary to string dictionary"""

        clean = {}

        for k, v in data.items():

            if isinstance(k, bytes):
                k = k.decode()

            if isinstance(v, bytes):
                v = v.decode()

            clean[k] = v

        return clean

    # string bytes conversions===============
    def _clean_chain(self, chain):
        """Convert certificate chain bytes to strings"""

        cleaned = []

        for cert in chain:

            new_cert = {}

            for k, v in cert.items():

            # Decode key
                if isinstance(k, bytes):
                    k = k.decode()

            # Decode value
                if isinstance(v, bytes):
                    v = v.decode()

            # If value is dict (nested)
                if isinstance(v, dict):

                    temp = {}

                    for kk, vv in v.items():

                        if isinstance(kk, bytes):
                            kk = kk.decode()

                        if isinstance(vv, bytes):
                            vv = vv.decode()

                        temp[kk] = vv

                    v = temp

                new_cert[k] = v

            cleaned.append(new_cert)

        return cleaned

    def _generate_pdf_report(self, data, logo_path="icon.jpg", footer_logo_path="icon.jpg"):
    # Safely get all keys with defaults
        domain = data.get("domain", "unknown_domain")
        certificate = data.get("certificate", {})
        security_profile = data.get("security_profile", {})
        scan_time = data.get("scan_time", datetime.now().strftime('%Y-%m-%d %H:%M'))
        protocol = data.get("protocol", "N/A")
        cipher = data.get("cipher", "N/A")

        subject = certificate.get("subject", {}).get("CN", "N/A")
        issuer = certificate.get("issuer", {}).get("CN", "N/A")
        expires = certificate.get("expires", "N/A")
        serial = certificate.get("serial", "N/A")
        signature = certificate.get("signature", "N/A")

        tls13 = security_profile.get("tls13", False)
        ocsp = security_profile.get("ocsp", "N/A")
        forward_secrecy = security_profile.get("forward_secrecy", False)

        filename = f"dsterminal_report_{domain}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"

        doc = SimpleDocTemplate(
            filename,
            pagesize=A4,
            rightMargin=40,
            leftMargin=40,
            topMargin=40,
            bottomMargin=40
        )

        page_width, page_height = A4
        styles = getSampleStyleSheet()
        elements = []

            # -------- Top Logo (auto-scaled, centered) --------
        if os.path.exists(logo_path):
            logo = Image(logo_path)
            max_width = page_width - doc.leftMargin - doc.rightMargin
            if logo.imageWidth > max_width:
                scale_ratio = max_width / logo.imageWidth
                logo.drawWidth = logo.imageWidth * scale_ratio
                logo.drawHeight = logo.imageHeight * scale_ratio
            logo.hAlign = 'CENTER'
            elements.append(logo)
            elements.append(Spacer(1, 20))

    # Title
        title_style = ParagraphStyle("TitleStyle", fontSize=22, alignment=1, spaceAfter=20, bold=True)
        section_style = ParagraphStyle("SectionStyle", fontSize=14, spaceBefore=20, spaceAfter=10, bold=True)
        normal = styles["Normal"]

        elements.append(Paragraph("DSTerminal Security Compliance Report", title_style))
        elements.append(Paragraph(f"Generated: {scan_time}", normal))
        elements.append(Spacer(1, 20))

    # System Info
        elements.append(Paragraph("System Information", section_style))
        sys_table = [
            ["Domain", domain],
            ["Protocol", protocol],
            ["Cipher", cipher],
            ["Scan Time", scan_time]
        ]
        elements.append(self._styled_table(sys_table))

    # Certificate Info
        elements.append(Paragraph("Certificate Details", section_style))
        cert_table = [
            ["Subject", subject],
            ["Issuer", issuer],
            ["Expiry", expires],
            ["Serial", serial],
            ["Signature", signature]
        ]
        elements.append(self._styled_table(cert_table))

    # Security Profile
        elements.append(Paragraph("Security Profile", section_style))
        sec_table = [
            ["TLS 1.3 Enabled", str(tls13)],
            ["OCSP Checked", ocsp],
            ["Forward Secrecy", str(forward_secrecy)]
        ]
        elements.append(self._styled_table(sec_table))

    # Recommendations
        elements.append(Paragraph("Recommendations", section_style))
        recs = self._build_recommendations(data)
        for rec in recs:
            elements.append(Paragraph(f"• {rec}", normal))
            elements.append(Spacer(1, 5))

    # Footer
        elements.append(Spacer(1, 40))
        footer_data = []

            # Footer logo
        if os.path.exists(footer_logo_path):
            footer_logo = Image(footer_logo_path)
            max_footer_width = 50  # small logo width
            scale_ratio = max_footer_width / footer_logo.imageWidth
            footer_logo.drawWidth = footer_logo.imageWidth * scale_ratio
            footer_logo.drawHeight = footer_logo.imageHeight * scale_ratio
            footer_data.append([footer_logo, Paragraph("AUTOGENERATED CERTIFICATE REPORT | DSTerminal Platform\n© Stark Expo Tech Exchange", normal)])
            footer_table = Table(footer_data, colWidths=[60, page_width - 60 - doc.leftMargin - doc.rightMargin])
            footer_table.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE')]))
            elements.append(footer_table)
        else:
        # fallback if logo missing
            elements.append(Paragraph("AUTOGENERATED REPORT | DSTerminal Platform", normal))
            elements.append(Paragraph("© Stark Expo Tech Exchange LTD", normal))

   
        doc.build(elements)
        print(f"\n[✓] PDF Compliance Report Created: {filename}")

    def _styled_table(self, data):

        table = Table(data, colWidths=[180, 320])

        style = TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), lightgrey),
            ("GRID", (0, 0), (-1, -1), 0.5, black),
            ("FONT", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("ALIGN", (0, 0), (0, -1), "LEFT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("PADDING", (0, 0), (-1, -1), 6),
        ])

        table.setStyle(style)

        return table

    def _build_recommendations(self, data):

        recs = []

        cert = data["certificate"]
        sec = data["security_profile"]

    # Expiry check
        expires = datetime.strptime(cert["expires"][:8], "%Y%m%d")
        days_left = (expires - datetime.utcnow()).days

        if days_left < 60:
            recs.append("Renew SSL certificate within 30 days")

        if not sec["tls13"]:
            recs.append("Upgrade server configuration to support TLS 1.3")

        if sec["ocsp"] != "VALID":
            recs.append("Enable OCSP stapling for revocation validation")

        if sec["forward_secrecy"] is False:
            recs.append("Enable Perfect Forward Secrecy (ECDHE)")

        if not recs:
            recs.append("No critical risks detected. Maintain current security posture.")

        return recs
# added animated effects for the ssl certificate checks================
    def _type_print(self, text, delay=0.02):
        """Cinematic typing effect"""
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()

    def _loading_animation(self, text, seconds=5):
        """Cinematic hacking-style animated loader with glitch and progress effects"""
    # Print main stage text centered
        terminal_width = 80
        print("\n" + text.center(terminal_width))
    
        spinner = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]
        end_time = time.time() + seconds
        i = 0

    # Build cinematic random messages
        flickers = [
            "[ACCESSING CERT DATA]", "[TLS HANDSHAKE INIT]", "[VALIDATING CHAIN]",
            "[OCSP CHECK]", "[ASSESSING RISK]", "[GENERATING RECOMMENDATIONS]",
            "[ANALYZING PROTOCOL]", "[CIPHER SCAN]", "[SIGNATURE VERIFY]"
        ]

        while time.time() < end_time:
        # Glitchy flicker text
            flicker_text = random.choice(flickers)
        
        # Animated spinner + sliding progress
            bar_length = 30
            progress = int(((time.time() % seconds) / seconds) * bar_length)
            bar = "█" * progress + "-" * (bar_length - progress)

        # Random colors
            color = random.choice([Fore.GREEN, Fore.CYAN, Fore.MAGENTA, Fore.YELLOW])
            sys.stdout.write(f"\r{color}{spinner[i % len(spinner)]} {bar} {flicker_text.center(40)}{Style.RESET_ALL}")
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1

    # Finish with a completed checkmark
        sys.stdout.write(f"\r{Fore.GREEN}[✓] {text} Completed{' ' * 40}{Style.RESET_ALL}\n")
        sys.stdout.flush()

    def dump_memory(self):
        """Create a memory dump (requires admin)"""
        if not self.is_admin():
            print("[!] Requires admin privileges")
            return

        print("\n[+] Creating memory dump...")
        try:
            if platform.system() == "Windows":
                os.system("procdump -ma -accepteula")
                print("[+] Memory dump saved as .dmp files")
            else:
                print("[!] Linux memory dump requires LiME or fmem")
        except Exception as e:
            print(f"[!] Error: {e}")

    def enable_tor_routing(self):
        """Route traffic through Tor"""
        print("\n[+] Configuring Tor routing...")
        try:
            if platform.system() == "Linux":
                os.system("sudo apt install tor -y")
                os.system("sudo service tor start")
                print("[+] Tor service started. Configure your apps to use 127.0.0.1:9050")
            else:
                print("[!] Automatic Tor setup requires Linux. Install Tor Browser manually.")
        except Exception as e:
            print(f"[!] Error: {e}")
#  --------------------for updates below==================

    def port_scan(self, target):
        """Basic port scanning"""
        print(f"\n[+] Scanning {target} for common ports...")
        common_ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 3389]
    
        for port in common_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((target, port))
                if result == 0:
                    print(f"  [+] Port {port}: OPEN")
                sock.close()
            except:
                pass


    def kill_process(self, pid):
        """Kill a process by PID"""
        try:
            if platform.system() == "Windows":
                os.system(f"taskkill /F /PID {pid}")
            else:
                os.system(f"kill -9 {pid}")
            print(f"[+] Process {pid} terminated")
        except Exception as e:
            print(f"[!] Failed to kill process: {e}")



    def system_info(self):
        """Display comprehensive system information"""
        print("\n[+] System Information:")
        print(f"  OS: {platform.system()} {platform.release()}")
        print(f"  Architecture: {platform.machine()}")
        print(f"  Processor: {platform.processor()}")
        print(f"  Python: {platform.python_version()}")
    
        if psutil:
            print(f"  CPU Cores: {psutil.cpu_count()}")
            print(f"  RAM: {psutil.virtual_memory().total / 1024**3:.1f} GB")

    def check_updates(self):
        """Cinematic update check with real GitHub API integration"""
        console = Console()

    # ===================== ANIMATIONS =====================
        def hacker_animation():
            symbols = "█▓▒░▄▀■►▼▲◄▶◀◢◣◥◤▬▭▮▯┌┐└┘├┤┬┴┼╔╗╚╝╠╣╦╩╬═║"
            width = console.size.width
            with console.status("[bold red]ACCESSING UPDATE SERVERS...[/]", spinner="dots"):
                for _ in range(3):
                    console.print(
                        "".join(random.choice(symbols) for _ in range(width)),
                        style="bold green"
                    )
                    time.sleep(1.5)

        def satellite_scan():
            frames = ["🛰", "📡", "📶", "🔍", "🎯"]
            with Progress(
                SpinnerColumn(style="cyan"),
                TextColumn("[bold blue]{task.description}"),
                transient=True,
                console=console
            ) as progress:
                task = progress.add_task("Establishing secure connection...", total=100)
                for i in range(100):
                    progress.update(task, advance=1,
                                    description=f"{frames[i % len(frames)]} Scanning {i}%")
                    time.sleep(1.5)

        def version_comparison_animation(current_ver, latest_ver):
            with Live(refresh_per_second=20, console=console) as live:
                for i in range(1, 6):
                    bar = "█" * (i * 10)
                    live.update(
                        Panel(
                            f"[bold]Comparing Versions[/]\n\n"
                            f"[yellow]Current:[/] {current_ver}\n{bar}\n\n"
                            f"[green]Latest:[/] {latest_ver}\n{bar}",
                            border_style="cyan"
                        )
                    )
                    time.sleep(1.5)

    # ===================== UPDATE LOGIC =====================
        def parse_version(v):
            parts = [int(p) if p.isdigit() else 0 for p in str(v).lstrip("vV").split(".")]
            while len(parts) < 3:
                parts.append(0)
            return tuple(parts)

        def check_github_release():
            try:
                api_url = (
                    "https://api.github.com/repos/"
                    "Stark-Expo-Tech-Exchange/DSTerminal_releases_latest/releases/latest"
                )
                r = requests.get(api_url, timeout=10)
                if r.status_code != 200:
                    return None

                data = r.json()
                assets = {
                    a["name"]: a["browser_download_url"]
                    for a in data.get("assets", [])
                }

                return {
                    "version": data.get("tag_name", "").lstrip("v"),
                    "url": data.get("html_url", ""),
                    "assets": assets,
                    "notes": data.get("body", ""),
                    "prerelease": data.get("prerelease", False),
                }

            except requests.RequestException:
                return None
        
# ---------------------another update function ends here from above===========

        def perform_update(latest_tag):
            """
            Downloads the latest DSTerminal release and updates local version.
            latest_tag: string, e.g., "v2.1.0"
            """

            os_type = platform.system().lower()  # 'linux', 'windows', 'darwin'
            print(f"[+] Detected OS: {os_type}")

    # Determine download URL based on OS
            if os_type == "linux":
                filename = f"dsterminal_{latest_tag}_amd64.deb"
                download_url = f"https://github.com/Stark-Expo-Tech-Exchange/DSTerminal_releases_latest/releases/download/{latest_tag}/{filename}"
            elif os_type == "windows":
                filename = f"DSTerminalInstaller_{latest_tag}.exe"
                download_url = f"https://github.com/Stark-Expo-Tech-Exchange/DSTerminal_releases_latest/releases/download/{latest_tag}/{filename}"
            else:
                print("[!] Your OS is not supported for auto-update.")
                return

    # Download the file
            try:
                print(f"[+] Downloading {filename} from GitHub...")
                r = requests.get(download_url, stream=True)
                r.raise_for_status()
                with open(filename, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"[+] Download complete: {filename}")

            except Exception as e:
                print(f"[!] Download failed: {e}")
                return

    # Auto-install depending on OS
            if os_type == "linux":
                print("[+] Installing .deb package...")
                try:
                    subprocess.run(["sudo", "dpkg", "-i", filename], check=True)
                    print("[+] Update installed successfully!")
                except subprocess.CalledProcessError as e:
                    print(f"[!] Installation failed: {e}")
                    print(f"[+] You may try: sudo dpkg -i {filename}")
            elif os_type == "windows":
                print(f"[+] Please run the downloaded installer manually: {filename}")
                print("[+] After installation, restart DSTerminal.")

    # Update local VERSION file
            version_file = os.path.join(os.path.dirname(__file__), "VERSION")
            try:
                with open(version_file, "w") as vf:
                    vf.write(latest_tag.strip("v"))
                print(f"[+] Local version updated to {latest_tag}")
            except Exception as e:
                print(f"[!] Could not update local VERSION file: {e}")

    # ===================== MAIN FLOW =====================
        try:
            console.print("\n")
            console.print(Panel(
                "[bold cyan]▄︻デ══━ INITIATING SYSTEM UPDATE PROTOCOL ══━︻▄[/]",
                border_style="cyan"
            ))

            time.sleep(0.5)
            hacker_animation()
            satellite_scan()

            current_version = CONFIG.get("CURRENT_VERSION", "1.0.0").lstrip("v")
            console.print(Panel(f"[bold]Current version:[/] v{current_version}",
            border_style="white"
            ))

            latest = check_github_release()
            if not latest:
                console.print(Panel(
                    "[yellow]Unable to reach update servers[/]",
                    border_style="yellow"
                ))
                return True

            version_comparison_animation(
                f"v{current_version}", f"v{latest['version']}"
            )

            if parse_version(latest["version"]) > parse_version(current_version):
                console.print(Panel(
                    f"[bold red]UPDATE AVAILABLE[/]\n\n"
                    f"Latest: v{latest['version']}\n"
                    f"{latest['notes'][:300]}",
                    border_style="red"
                ))

                if console.input("Install update now? (y/N): ").lower() == "y":
                    return perform_update(latest)

            else:
                console.print(Panel(
                    f"[bold green]DSTerminal is up to date[/]\n\n"
                    f"Checked: {datetime.now():%Y-%m-%d %H:%M:%S}",
                    border_style="green"
                ))

            return True

        except Exception as e:
            console.print(Panel(
                f"[bold red]UPDATE ERROR[/]\n\n{str(e)}",
                border_style="red"
            ))
            return True

# --------------------------for updates above code--------------------

# ---------------------------wipe tracks and terminal clearing
    def clear_terminal(self):
        """Advanced terminal clearing with spinning boxes and centered animations"""
        from rich.console import Console
        from rich.panel import Panel
        from rich.align import Align
        from rich.live import Live
        from rich.layout import Layout
        import platform
    
        console = Console()
        terminal_width = shutil.get_terminal_size((80, 20)).columns
        panel_width = min(70, terminal_width - 10)
    
    # Multiple spinner types for variety
        spinners = {
            'dots': ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"],
            'arrows': ["←", "↖", "↑", "↗", "→", "↘", "↓", "↙"],
            'pipes': ["┤", "┘", "┴", "└", "├", "┌", "┬", "┐"],
            'circles': ["◴", "◷", "◶", "◵"]
        }
    
    # Glitch text fragments
        glitch_texts = [
            "CLEARING...", "WIPING...", "PURGING...", 
            "RESETTING...", "REFRESHING...", "RELOADING..."
        ]
    
    # Create a box with spinning animation
        with Live(console=console, refresh_per_second=12, screen=True) as live:
            for phase in range(4):  # 4 phases of clearing
                for step in range(25):  # 25 steps per phase
                # Select spinner based on phase
                    spinner_type = list(spinners.keys())[phase % len(spinners)]
                    spinner = spinners[spinner_type][step % len(spinners[spinner_type])]
                
                # Phase-based colors
                    if phase == 0:
                        color = "bright_red"
                        phase_text = "PHASE 1: MEMORY CLEAR"
                    elif phase == 1:
                        color = "bright_yellow"
                        phase_text = "PHASE 2: BUFFER FLUSH"
                    elif phase == 2:
                        color = "bright_green"
                        phase_text = "PHASE 3: CACHE WIPE"
                    else:
                        color = "bright_cyan"
                        phase_text = "PHASE 4: DISPLAY RESET"
                
                # Progress calculation
                    total_progress = (phase * 25 + step) / 100
                    progress_bar_width = panel_width - 30
                    progress_filled = int(total_progress * progress_bar_width)
                    progress_bar = "█" * progress_filled + "░" * (progress_bar_width - progress_filled)
                
                # Random glitch effect
                    if random.random() > 0.7:
                        glitch = random.choice(glitch_texts)
                    else:
                        glitch = ""
                
                # Create stats content
                    stats_content = (
                        f"[cyan]CPU: [green]{random.randint(20, 95)}%[/green]\n"
                        f"[cyan]MEM: [yellow]{random.randint(100, 500)}MB[/yellow]\n"
                        f"[cyan]PID: [white]{os.getpid()}[/white]"
                    )
                
                # Create main content
                    main_content = Panel(
                        Align.center(
                            f"[bold {color}]{spinner} {phase_text} {spinner}[/bold {color}]\n\n"
                            f"[white]{progress_bar}[/white] [{int(total_progress*100)}%]\n\n"
                            f"[dim]{glitch}[/dim]",
                            vertical="middle"
                        ),
                        title=f"[bold {color}]╔ TERMINAL WIPE SEQUENCE ╗[/bold {color}]",
                        border_style=color,
                        padding=(1, 2),
                        width=panel_width
                    )
                
                # Create stats box
                    stats_box = Panel(
                        Align.center(stats_content, vertical="middle"),
                        title="[bold white]SYS STATS[/bold white]",
                        border_style="bright_black",
                        width=panel_width - 4,
                        padding=(1, 1)
                    )
                
                # Create layout to combine panels
                    layout = Layout()
                    layout.split_column(
                        Layout(main_content),
                        Layout(stats_box)
                    )
                
                # Center everything
                    final_display = Align.center(layout)
                
                    live.update(final_display)
                    time.sleep(0.05)
    
    # Execute actual terminal clear
        os.system("clear" if platform.system() != "Windows" else "cls")
    
    # Create a dramatic banner reveal
        banner = """
        ╔═══════════════════════════════════════════════════════════════════╗
        ║                                                                    ║
        ║    ██████╗ ███████╗███████╗███████╗███╗   ██╗███████╗██╗  ██╗    ║
        ║    ██╔══██╗██╔════╝██╔════╝██╔════╝████╗  ██║██╔════╝╚██╗██╔╝    ║
        ║    ██║  ██║█████╗  █████╗  █████╗  ██╔██╗ ██║█████╗   ╚███╔╝     ║
        ║    ██║  ██║██╔══╝  ██╔══╝  ██╔══╝  ██║╚██╗██║██╔══╝   ██╔██╗     ║
        ║    ██████╔╝██║     ██║     ███████╗██║ ╚████║███████╗██╔╝ ██╗    ║
        ║    ╚═════╝ ╚═╝     ╚═╝     ╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝    ║
        ║                                                                    ║
        ╚═══════════════════════════════════════════════════════════════════╝
        """
    
    # Animate banner with scan line effect
        banner_lines = banner.split('\n')
        centered_banner = []
    
    # Center each line
        for line in banner_lines:
            if line.strip():
                centered_banner.append(line.center(terminal_width))
            else:
                centered_banner.append('')
    
    # Display with scan line animation
        for i, line in enumerate(centered_banner):
            if i == 0 or i == len(centered_banner)-1:
                console.print(f"[bright_cyan]{line}[/bright_cyan]")
            elif i == 1 or i == 7:
                console.print(f"[bright_blue]{line}[/bright_blue]")
            elif 2 <= i <= 6:
            # Gradient effect on logo
                colors = ["cyan", "bright_cyan", "blue", "bright_blue", "green"]
                color = colors[(i-2) % len(colors)]
                console.print(f"[bold {color}]{line}[/bold {color}]")
            else:
                console.print(f"[dim]{line}[/dim]")
            time.sleep(0.03)
    
    # Add a status message with blink effect
        status_panel = Panel(
            Align.center(
                "[blink][bright_green]✦ SYSTEM INITIALIZED ✦[/bright_green][/blink]\n\n"
                f"[cyan]Session ID:[/cyan] [white]{datetime.now().strftime('%Y%m%d%H%M%S')}[/white]\n"
                f"[cyan]Ready for:[/cyan] [yellow]SSL/TLS Security Audit[/yellow]",
                vertical="middle"
            ),
            title="[bold white]SYSTEM STATUS[/bold white]",
            border_style="bright_green",
            padding=(1, 2),
            width=panel_width
        )
    
        console.print(Align.center(status_panel))
        print()

    # =======ends here from above-==============
    def emergency_shutdown(self):
        console = Console()

        def authenticate():
            console.print("\n[bold yellow]Authentication Required:[/bold yellow] Confirm emergency shutdown.")
            response = Prompt.ask("Type [red]YES[/red] to confirm", default="NO")
            return response.strip().lower() == "yes"

        if not authenticate():
            console.print("\n[bold cyan]Shutdown aborted.[/bold cyan]")
            return

        countdown_panel = Panel(
            Align.center("[bold red]\u26a0 EMERGENCY SHUTDOWN INITIATED \u26a0[/bold red]", vertical="middle"),
            title="[red bold]SYSTEM OVERRIDE[/red bold]",
            border_style="red",
            padding=(1, 4),
            width=60
        )

        with Live(console=console, refresh_per_second=4, screen=True) as live:
            for i in reversed(range(1, 16)):
                live.update(Panel(f"[bold red]Shutting down in {i} seconds...[/bold red]", border_style="bright_red", width=60))
                time.sleep(1)
            live.update(countdown_panel)
            time.sleep(1)

        console.print("[bold red]Powering down system...[/bold red]")
        time.sleep(1)

        if platform.system() == "Linux":
            os.system("sudo shutdown now")
        elif platform.system() == "Windows":
            os.system("shutdown /s /t 0")
        else:
            console.print("[yellow]Unsupported OS for shutdown command.[/yellow]")

# shutting down ends here
    # def clear_terminal(self):
    #     console = Console()

    #     panel = Panel(
    #         Align.center("[cyan]Resetting interface...[/cyan]", vertical="middle"),
    #         title="[bold white]TERMINAL WIPE[/bold white]",
    #         border_style="bright_cyan",
    #         padding=(1, 2),
    #         width=50
    #     )

    #     with Live(console=console, refresh_per_second=5, screen=True) as live:
    #         for i in range(10):
    #             live.update(Panel(f"[cyan]Wiping in progress... {10 - i}[/cyan]", title="[bold]CLEANING TERMINAL[/bold]", border_style="bright_cyan", width=50))
    #             time.sleep(1)

    #     os.system("clear" if platform.system() != "Windows" else "cls")

    #     banner = """
    #         ██████╗ ███████╗███████╗███████╗███╗   ██╗███████╗██╗  ██╗
    #         ██╔══██╗██╔════╝██╔════╝██╔════╝████╗  ██║██╔════╝╚██╗██╔╝
    #         ██║  ██║█████╗  █████╗  █████╗  ██╔██╗ ██║█████╗   ╚███╔╝ 
    #         ██║  ██║██╔══╝  ██╔══╝  ██╔══╝  ██║╚██╗██║██╔══╝   ██╔██╗ 
    #         ██████╔╝██║     ██║     ███████╗██║ ╚████║███████╗██╔╝ ██╗
    #         ╚═════╝ ╚═╝     ╚═╝     ╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝
    #     """
    #     centered_banner = Align.center(f"[bold cyan]{banner}[/bold cyan]", vertical="middle")
    #     console.print(centered_banner)


# =======testing code from above ends here for shutdown command
    def vt_scan_menu(self):
        """Enhanced VirusTotal scanning interface"""
        print("\n[VirusTotal Scanner]")
        print("1. Hash lookup")
        print("2. File scan")
        print("3. Bulk scan folder")
        print("4. Check previous scan")
        choice = input("Select option: ")
        
        if choice == "1":
            file_hash = input("Enter file hash (MD5/SHA1/SHA256): ").strip()
            self.vt_hash_lookup(file_hash)
        elif choice == "2":
            file_path = input("File path to scan: ").strip()
            self.vt_file_scan(file_path)
        elif choice == "3":
            folder_path = input("Folder path to scan: ").strip()
            max_files = input("Max files to scan (default 10): ").strip() or 10
            self.vt_bulk_scan(folder_path, int(max_files))
        elif choice == "4":
            scan_id = input("Enter previous scan ID: ").strip()
            self.check_scan_result(scan_id)
        else:
            print("[!] Invalid choice")

    def vt_hash_lookup(self, file_hash):
        """Enhanced hash lookup with detailed results"""
        if not self._validate_vt_api():
            return

        try:
            url = f"https://www.virustotal.com/api/v3/files/{file_hash}"
            headers = {"x-apikey": CONFIG['VT_API_KEY']}
            
            print(f"\n[+] Checking hash: {file_hash}...")
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                attrs = result['data']['attributes']
                
                # Detailed report
                print(f"\n╔{'═'*60}╗")
                print(f"║ {'VirusTotal Report':^58} ║")
                print(f"╠{'═'*60}╣")
                print(f"║ {'Detection:':<15} {attrs['last_analysis_stats']['malicious']}/{sum(attrs['last_analysis_stats'].values())} ║")
                print(f"║ {'First Seen:':<15} {attrs['first_submission_date']} ║")
                print(f"║ {'File Type:':<15} {attrs.get('type_tag', 'Unknown')} ║")
                
                # Top detections
                malicious = [k for k,v in attrs['last_analysis_results'].items() if v['category'] == 'malicious']
                if malicious:
                    print(f"╠{'═'*60}╣")
                    print(f"║ {'Top Detections:':<58} ║")
                    for engine in malicious[:3]:
                        print(f"║ - {engine:<55} ║")
                print(f"╚{'═'*60}╝")
                
                # Auto-quarantine recommendation
                if attrs['last_analysis_stats']['malicious'] > 0:
                    print("\n[!] MALICIOUS FILE DETECTED!")
                    if input("Quarantine file? (y/N): ").lower() == 'y':
                        self.quarantine_file(None, file_hash=file_hash)
            else:
                print("[!] Hash not found in VirusTotal")
        except Exception as e:
            print(f"[!] Error: {e}")
  

    def vt_file_scan(self, file_path):
        """Upload file to VirusTotal with debug output"""
        print(f"\n[DEBUG] Starting scan for: {file_path}")  # Debug line
    
        if not os.path.exists(file_path):
            print("[!] Error: File not found")
            print(f"[DEBUG] Resolved path: {os.path.abspath(file_path)}")  # Debug line
            return

            print("[DEBUG] File exists check passed")  # Debug line
    
        if not self._validate_vt_api():
            print("[!] Error: VirusTotal API validation failed")
            print(f"[DEBUG] API Key: {'Set' if CONFIG.get('VT_API_KEY') else 'Not Set'}")  # Debug line
            return

        print("[DEBUG] API validation passed")  # Debug line
    
        MAX_SIZE = 32 * 1024 * 1024  # 32MB
        file_size = os.path.getsize(file_path)
        print(f"[DEBUG] File size: {file_size} bytes")  # Debug line

        if file_size > MAX_SIZE:
            print(f"[!] Error: File too large ({file_size/1024/1024:.2f}MB > 32MB)")
            return

        print("[DEBUG] Size check passed")  # Debug line
    
        try:
            print(f"\n[+] Analyzing {os.path.basename(file_path)}...")
            print(f"  ↳ Size: {file_size/1024:.2f}KB")
            print("  ↳ Uploading...", end='', flush=True)
        
            with open(file_path, 'rb') as f:
                files = {'file': (os.path.basename(file_path), f)}
                headers = {"x-apikey": CONFIG['VT_API_KEY']}
                print(f"\n[DEBUG] Sending request to VirusTotal...")  # Debug line
                response = requests.post(
                    "https://www.virustotal.com/api/v3/files",
                    headers=headers,
                    files=files,
                    timeout=30
                )
            print(" Done!")

            print(f"[DEBUG] Response status: {response.status_code}")  # Debug line
            if response.status_code == 200:
                result = response.json()
                scan_id = result['data']['id']
                print(f"\n[+] Scan ID: {scan_id}")
                print(f"[+] Report URL: https://www.virustotal.com/gui/file/{scan_id}")
                self._cache_scan_id(file_path, scan_id)
            else:
                print(f"[!] Error: Upload failed (HTTP {response.status_code})")
                print(f"[DEBUG] Response text: {response.text}")  # Debug line

        except Exception as e:
            print(f"\n[!] Critical Error: {str(e)}")
            print("[DEBUG] Exception occurred during upload")  # Debug line

        if response.status_code == 200:
            result = response.json()
            scan_id = result['data']['id']
            print(f"\n[+] Scan ID: {scan_id}")
        
        # Start polling in background
        Thread(target=self._poll_results, args=(scan_id, file_path), daemon=True).start()
 
    def _cache_scan_id(self, file_path, scan_id):
        """Store scan IDs for future reference"""
        cache_file = os.path.expanduser("~/.dstenex_scans.log")
        with open(cache_file, "a") as f:
            f.write(f"{file_path}|{scan_id}|{datetime.now()}\n")

    def vt_bulk_scan(self, folder_path, max_files=10):
        """Scan multiple files in a folder"""
        if not os.path.isdir(folder_path):
            print("[!] Invalid folder path")
            return
            
        print(f"\n[+] Scanning up to {max_files} files in {folder_path}...")
        scanned = 0
        
        for root, _, files in os.walk(folder_path):
            for file in files:
                if scanned >= max_files:
                    break
                    
                file_path = os.path.join(root, file)
                print(f"\n[File {scanned+1}/{max_files}] {file}")
                
                # First try local scan
                local_result = self.local_scan(file_path, silent=True)
                if local_result and local_result['infected']:
                    print("[!] LOCAL SCAN DETECTED THREAT!")
                    self.quarantine_file(file_path)
                    scanned += 1
                    continue
                
                # Fall back to VT if file < 32MB
                if os.path.getsize(file_path) <= 32 * 1024 * 1024:
                    self.vt_file_scan(file_path)
                else:
                    print("[!] File too large for VT, skipped")
                
                scanned += 1
                time.sleep(15)  # Respect VT API rate limits
        
        print("\n[+] Bulk scan completed")

    def _poll_results(self, scan_id, original_path=None):
        """Background result polling"""
        url = f"https://www.virustotal.com/api/v3/analyses/{scan_id}"
        headers = {"x-apikey": CONFIG['VT_API_KEY']}
        
        print("\n[+] Waiting for results... (Ctrl+C to check later)")
        try:
            for _ in range(10):  # Max 10 checks
                time.sleep(30)
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    result = response.json()
                    status = result['data']['attributes']['status']
                    
                    if status == 'completed':
                        stats = result['data']['attributes']['stats']
                        print(f"\n[+] Final Results: {stats['malicious']} malicious / {stats['harmless']} clean")
                        
                        if stats['malicious'] > 0 and original_path:
                            self.quarantine_file(original_path)
                        return
                    else:
                        print(f"\r  ↳ Status: {status}...", end='', flush=True)
        except Exception:
            print("\n[!] Polling interrupted. Check later with 'check_result'")

    def check_scan_result(self, scan_id):
        """Check existing scan results"""
        url = f"https://www.virustotal.com/api/v3/analyses/{scan_id}"
        headers = {"x-apikey": CONFIG['VT_API_KEY']}
        
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                result = response.json()
                stats = result['data']['attributes']['stats']
                print(f"\n[+] Results: {stats['malicious']} malicious / {stats['harmless']} clean")
                
                if stats['malicious'] > 0:
                    print("[!] MALICIOUS CONTENT DETECTED")
            else:
                print("[!] Results not available yet")
        except Exception as e:
            print(f"[!] Error checking results: {e}")

    def local_scan(self, file_path, silent=False):
        """Integrate ClamAV for local scanning"""
        try:
            import pyclamd
            cd = pyclamd.ClamdAgnostic()
            scan_result = cd.scan_file(file_path)
            
            if scan_result and scan_result.get(file_path) == 'OK':
                if not silent:
                    print("[+] Local scan: Clean")
                return {'infected': False}
            else:
                if not silent:
                    print("[!] Local scan: Infected!")
                    print(f"Detection: {scan_result.get(file_path, 'Unknown threat')}")
                return {'infected': True, 'threat': scan_result.get(file_path)}
                
        except ImportError:
            if not silent:
                print("[!] ClamAV not installed (pip install pyclamd)")
        except Exception as e:
            if not silent:
                print(f"[!] Local scan failed: {e}")
        return None

    def quarantine_file(self, file_path, file_hash=None):
        """Move dangerous files to quarantine"""
        quarantine_dir = os.path.join(os.path.expanduser("~"), "quarantine")
        os.makedirs(quarantine_dir, exist_ok=True)
        
        try:
            if file_path:
                filename = os.path.basename(file_path)
                new_path = os.path.join(quarantine_dir, f"quarantined_{filename}")
                shutil.move(file_path, new_path)
                print(f"[+] File moved to quarantine: {new_path}")
            elif file_hash:
                with open(os.path.join(quarantine_dir, "quarantined_hashes.txt"), "a") as f:
                    f.write(f"{file_hash}\n")
                print("[+] Malicious hash recorded")
        except Exception as e:
            print(f"[!] Quarantine failed: {e}")

    def _validate_vt_api(self):
        """Check if API key is configured"""
        if not CONFIG.get('VT_API_KEY') or CONFIG['VT_API_KEY'] == 'YOUR_VIRUSTOTAL_API_KEY':
            print("[!] Configure VirusTotal API key first:")
            print("1. Get key from: https://www.virustotal.com/gui/join-us")
            print("2. Edit CONFIG['VT_API_KEY'] in your code")
            return False
        return True


        # go up to change

    def monitor_registry(self):
        """Monitor Windows registry changes"""
        if platform.system() != "Windows":
            return "[!] Registry monitoring requires Windows"

        suspicious_keys = [
            r"HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run",
            r"HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run",
            r"HKLM\SYSTEM\CurrentControlSet\Services"
        ]
        
        try:
            import winreg
            changes = []
            
            for key_path in suspicious_keys:
                hive, path = key_path.split('\\', 1)
                hive = getattr(winreg, {
                    'HKLM': 'HKEY_LOCAL_MACHINE',
                    'HKCU': 'HKEY_CURRENT_USER'
                }[hive])
                
                with winreg.OpenKey(hive, path) as key:
                    for i in range(winreg.QueryInfoKey(key)[1]):
                        name, value, _ = winreg.EnumValue(key, i)
                        changes.append(f"{key_path}\\{name} = {value}")
            
            if changes:
                return "\n".join(["[!] Suspicious registry entries:"] + changes)
            else:
                return "[+] No suspicious registry entries found"
        except Exception as e:
            return f"[!] Registry scan failed: {e}"
 
    #  starts here
    def _print_banner(self, text):
        subprocess.run(["figlet", text])
        """Display hacking-style banner with fallback"""
        try:
            ascii_art = figlet_format(text, font='slant')
            if os.environ.get('TERM') and 'color' in os.environ.get('TERM', ''):
                colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]
                flicker = random.choice(colors) + ascii_art.replace(random.choice(text), '▒') + Style.RESET_ALL
                print(f"\n{flicker}")
            else:
                # print(f"\n{ascii_art}")
                print(f"\n")
        except ImportError:
            border = "═" * (len(text) + 4)
            print(f"\n")
            # print(f"\n{border}\n  {text.upper()}  \n{border}\n")

        except Exception as e:
            print(f"\n=== {text.upper()} ===\n")
 
    def _hacking_animation(duration, graphics):
        console = Console()
        symbols = list("▣⚙⧫◎◉⛏⊠⊞⌁⍟☍█▓▒░▌▎#@$=%/\\*~^↯⎈⛶∞∴∵")

        class RotatingSymbol:
            def __init__(self):
                self.frames = random.sample(symbols, k=4)
                self.frame_iter = itertools.cycle(self.frames)
                self.color = random.choice(["cyan", "magenta", "green", "yellow", "red", "blue", "bright_white"])

            def next(self):
                symbol = next(self.frame_iter)
                self.color = random.choice(["cyan", "magenta", "green", "yellow", "red", "blue", "bright_white"])
                return Text(symbol, style=self.color)

        rows, cols = 2, 150
        symbol_grid = [[RotatingSymbol() for _ in range(cols)] for _ in range(rows)]

    # Progress bar setup
        progress = Progress(
            TextColumn("[bold green]HARDENING...[/bold green]"),
            BarColumn(bar_width=None),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            expand=False,
        )
        task = progress.add_task("HARDENING", total=100)

        start_time = time.time()
        duration = 15  # seconds

        def render():
        # Background grid
            text = Text()
            for row in symbol_grid:
                for symbol in row:
                    text.append(symbol.next())
                text.append("\n")

        # Centered panel with progress bar
            elapsed = time.time() - start_time
            percent = min(100, int((elapsed / duration) * 100))
            progress.update(task, completed=percent)

            panel = Panel(
                Align.center(progress, vertical="middle"),
                title="[bold cyan]System Hardening Phase [1, 2 & 3][/bold cyan]",
                border_style="bright_white",
                width=40,
                padding=(1, 2),
            )

            combined = Group(text, Align.center(panel, vertical="middle"))
            return combined

        with Live(render(), console=console, refresh_per_second=10, screen=True) as live:
            try:
                while time.time() - start_time < duration:
                    time.sleep(0.1)
                    live.update(render())
            except KeyboardInterrupt:
                console.print("\n[bold red]Animation interrupted.[/bold red]")

        console.print("[bold green]✓ Access Granted.[/bold green]")

    def _cyber_attack_simulation(self):
        """Simulate incoming attacks being blocked (randomized)"""
        attack_types = ["Brute Force", "SQL Injection", "XSS", "RCE", "Zero-Day"]
        protocols = ["SSH", "HTTP", "HTTPS", "FTP", "SMTP"]

        print(f"\n{Fore.RED}▄︻デ══━ INTRUSION DETECTED ══━︻▄{Style.RESET_ALL}")
        for _ in range(random.randint(3, 5)):
            attack = random.choice(attack_types)
            protocol = random.choice(protocols)
            ip = ".".join(str(random.randint(1, 255)) for _ in range(4))
            time.sleep(random.uniform(0.3, 0.7))
            print(f"{Fore.YELLOW}▶ {ip} | {protocol} | {attack}{Style.RESET_ALL}", end='')
            time.sleep(random.uniform(0.5, 1.2))
            print(f"\r{Fore.GREEN}✓ {ip} | {protocol} | {attack} {Fore.BLACK}▶ BLOCKED{Style.RESET_ALL}")

    def _network_scan_animation(self):
        """Simulate network scanning visualization"""
        print(f"\n{Fore.CYAN}═════════⋘ NETWORK TOPOLOGY ⋙═════════{Style.RESET_ALL}")
        devices = [
            ("Router", "192.168.1.1", "Cisco IOS"),
            ("Workstation", "192.168.1.15", "Windows 11"),
            ("Server", "192.168.1.100", "Ubuntu 22.04")
        ]

        for device, ip, osys in devices:
            print(f"{Fore.MAGENTA}⌖ {device}: {ip}", end='')
            for _ in range(3):
                print(".", end='', flush=True)
                time.sleep(0.3)
            print(f" {Fore.WHITE}[{osys}]{Style.RESET_ALL}")

# Initialize colorama for Windows compatibility
    
    def _get_terminal_width(self):
        """Get terminal width for centering"""
        try:
            import shutil
            return shutil.get_terminal_size().columns
        except:
            return 80  # Default width
    
    def _center_text(self, text):
        """Center text based on terminal width"""
        return text.center(self.terminal_width)
    
    def _blinking_text(self, text, color=Fore.GREEN, duration=2):
        """Create blinking text effect"""
        end_time = time.time() + duration
        while time.time() < end_time:
            print(f"\r{color}{text}{Style.RESET_ALL}", end="", flush=True)
            time.sleep(0.3)
            print(f"\r{' ' * len(text)}", end="", flush=True)
            time.sleep(0.3)
        print(f"\r{color}{text}{Style.RESET_ALL}")
    
    def _enlarged_ascii_banner(self):
        """Display enlarged, centered, blinking CYBER DEFENSE banner"""
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear screen
        
        # Create the banner lines
        banner_line1 = "=" * 50
        banner_line2 = " " * 18 + "CYBER DEFENSE" + " " * 18
        banner_line3 = "=" * 50
        
        # Enlarge by repeating each character (double size)
        enlarged_lines = []
        for line in [banner_line1, banner_line2, banner_line3]:
            enlarged_line = ""
            for char in line:
                enlarged_line += char * 2  # Double each character horizontally
            enlarged_lines.append(enlarged_line)
        
        # Center each line
        centered_lines = []
        for line in enlarged_lines:
            centered_lines.append(self._center_text(line))
        
        centered_banner = "\n".join(centered_lines)
        
        # Print with blinking and color cycling effect
        colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]
        for _ in range(4):  # Blink 4 times
            for color in colors:
                os.system('cls' if os.name == 'nt' else 'clear')
                print(f"\n{color}{centered_banner}{Style.RESET_ALL}")
                print(f"\n{Fore.CYAN}{self._center_text('═' * 60)}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}{self._center_text('DEFENSIVE SECURITY TERMINAL v2.0.59')}{Style.RESET_ALL}")
                print(f"{Fore.CYAN}{self._center_text('═' * 60)}{Style.RESET_ALL}")
                print(f"{Fore.GREEN}{self._center_text('⚡ System Ready | Mode: ADMIN ⚡')}{Style.RESET_ALL}")
                time.sleep(0.2)
        
        time.sleep(1)
    
    def _print_banner(self, text):
        """Print a decorative banner with centering"""
        print(f"\n{Fore.CYAN}{self._center_text('=' * 50)}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{self._center_text(text)}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{self._center_text('=' * 50)}{Style.RESET_ALL}\n")
    
    def _matrix_rain_effect(self, duration=2):
        """Create Matrix-style digital rain effect"""
        end_time = time.time() + duration
        chars = "01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン"
        
        while time.time() < end_time:
            line = ''.join(random.choice(chars) for _ in range(self.terminal_width // 2))
            print(f"\r{Fore.GREEN}{line}{Style.RESET_ALL}", end="", flush=True)
            time.sleep(0.05)
        print()
    
    def is_admin(self):
        """Check if the script is running with admin privileges"""
        try:
            if platform.system() == "Windows":
                import ctypes
                return ctypes.windll.shell32.IsUserAnAdmin() != 0
            else:
                return os.getuid() == 0
        except:
            return False
    
    def _cinematic_typing(self, text, delay=0.03):
        """Print text character by character for cinematic effect"""
        for char in text:
            print(char, end="", flush=True)
            time.sleep(delay)
        print()
    
    def _hacking_animation(self, text):
        """Simple hacking animation"""
        print(f"{Fore.GREEN}[*] {text}...{Style.RESET_ALL}")
        time.sleep(0.5)
    
    def _progress_bar(self, task_name, duration=2, length=30):
        """Show a simple text-based progress bar for cinematic effect"""
        print(f"{task_name}: ", end="", flush=True)
        for i in range(length + 1):
            bar = "█" * i + "▒" * (length - i)
            percent = int((i / length) * 100)
            color = Fore.GREEN if percent < 50 else Fore.YELLOW if percent < 80 else Fore.RED
            print(f"\r{task_name}: {color}|{bar}| {percent}%{Style.RESET_ALL}", end="", flush=True)
            time.sleep(duration / length)
        print()
    
    def _network_scan_animation(self):
        """Simulate network scanning with visual effects"""
        print(f"\n{Fore.CYAN}{self._center_text('═════════⋘ NETWORK TOPOLOGY ⋙═════════')}{Style.RESET_ALL}")
        ips = [
            (f"⌖ Router: 192.168.1.1... [Cisco IOS]", Fore.YELLOW),
            (f"⌖ Workstation: 192.168.1.15... [Windows 11]", Fore.GREEN),
            (f"⌖ Server: 192.168.1.100... [Ubuntu 22.04]", Fore.BLUE),
            (f"⌖ IoT Device: 192.168.1.50... [Smart Hub]", Fore.MAGENTA),
            (f"⌖ Printer: 192.168.1.30... [HP LaserJet]", Fore.CYAN)
        ]
        
        for ip, color in ips:
            self._cinematic_typing(f"{color}{ip}{Style.RESET_ALL}", 0.02)
            time.sleep(0.3)
    
    def _vulnerability_scan(self):
        """Simulated vulnerability assessment with randomized output"""
        sample_vulns = [
            ("CVE-2023-1234", "Critical", "SMB Protocol"),
            ("CVE-2022-4567", "High", "OpenSSL"),
            ("CVE-2021-8910", "Medium", "Linux Kernel"),
            ("CVE-2020-4455", "Low", "Apache Server"),
            ("CVE-2019-1111", "Critical", "Docker")
        ]
        vulns = random.sample(sample_vulns, k=random.randint(2, 4))
        
        print(f"\n{Fore.RED}{self._center_text('▄︻デ══━ VULNERABILITY SCAN ══━︻▄')}{Style.RESET_ALL}")
        for cve, severity, component in vulns:
            time.sleep(0.5)
            severity_color = Fore.RED if severity == "Critical" else Fore.YELLOW if severity == "High" else Fore.GREEN
            print(f"{severity_color}{severity.upper().ljust(8)} {cve} → {component}{Style.RESET_ALL}")
            time.sleep(0.3)
        print(f"{Fore.GREEN}✓ {len(vulns)} vulnerabilities patched{Style.RESET_ALL}")
    
    def _cyber_attack_simulation(self):
        """Simulate cyber attack detection with blinking effects"""
        print(f"\n{Fore.RED}{self._center_text('▄︻デ══━ INTRUSION DETECTED ══━︻▄')}{Style.RESET_ALL}")
        attacks = [
            (f"✓ 225.242.61.205 | HTTPS | RCE ▶ BLOCKED", Fore.GREEN),
            (f"✓ 188.101.45.207 | HTTPS | XSS ▶ BLOCKED", Fore.GREEN),
            (f"✓ 43.77.112.198 | HTTP | Brute Force ▶ BLOCKED", Fore.YELLOW),
            (f"✓ 250.124.212.130 | HTTPS | Brute Force ▶ BLOCKED", Fore.YELLOW),
            (f"⚠ 78.95.143.67 | SSH | Dictionary Attack ▶ MITIGATED", Fore.RED)
        ]
        
        for attack, color in attacks:
            self._cinematic_typing(f"{color}{attack}{Style.RESET_ALL}", 0.03)
            time.sleep(0.3)
        
        # Blinking threat neutralized
        self._blinking_text(self._center_text("⚠ THREAT NEUTRALIZED ⚠"), Fore.RED, 2)
    
    def harden_system(self, dry_run=False):
        """Cinematic system hardening with typing, animations, and progress bars"""
        try:
            # Show enlarged blinking banner at start - THIS WAS MISSING!
            self._enlarged_ascii_banner()
            
            # Matrix rain effect for style
            self._matrix_rain_effect(1)
            
            # Check admin privileges
            if not self.is_admin():
                self._hacking_animation("Checking Privileges")
                print(f"{Fore.RED}[!] Warning: Running without administrator privileges. Some features may be limited.{Style.RESET_ALL}")
                # Don't return, continue with limited functionality
            
            # ----------------------------
            # Pre-hardening animations
            # ----------------------------
            self._hacking_animation("Initializing Threat Assessment")
            self._cinematic_typing("Scanning system threats...")
            self._progress_bar("Threat Assessment", duration=3)
            
            self._network_scan_animation()
            self._hacking_animation("Scanning Exploit Database")
            self._cinematic_typing("Analyzing known vulnerabilities...")
            self._progress_bar("Exploit Database Scan", duration=3)
            
            self._vulnerability_scan()
            self._cyber_attack_simulation()
            self._cinematic_typing("Threat analysis complete.")
            self._progress_bar("Threat Analysis", duration=2)
            
            # ----------------------------
            # Dry-run simulation
            # ----------------------------
            if dry_run:
                self._hacking_animation("Simulating Countermeasures")
                self._cinematic_typing("[SIMULATION] No changes were actually made.", 0.05)
                self._progress_bar("Simulation", duration=2)
            
            # ----------------------------
            # Actual hardening
            # ----------------------------
            else:
                self._hacking_animation("Deploying Cyber Armor")
                self._cinematic_typing("Applying system fortifications...", 0.04)
                self._progress_bar("Deploying Armor", duration=3)
                
                try:
                    system = platform.system()
                    
                    # Windows Hardening
                    if system == "Windows":
                        try:
                            self._cinematic_typing("Disabling SMB1 protocol...", 0.04)
                            powershell_cmd = "powershell -Command Disable-WindowsOptionalFeature -Online -FeatureName smb1protocol -NoRestart"
                            self._progress_bar("SMB1 Disable", duration=2)
                            
                            if self.is_admin():
                                result = subprocess.run(powershell_cmd, shell=True, capture_output=True, text=True)
                                
                                if result.returncode == 0:
                                    self._cinematic_typing("[OK] SMB1 protocol disabled.", 0.04)
                                    logging.info("SMB1 protocol disabled successfully on Windows")
                                else:
                                    self._cinematic_typing(f"[!] PowerShell command failed: {result.stderr}", 0.04)
                                    logging.error(f"PowerShell command failed: {result.stderr}")
                            else:
                                self._cinematic_typing("[!] Skipping SMB1 disable (requires admin rights)", 0.04)
                            
                        except Exception as e:
                            self._cinematic_typing(f"[!] Could not disable SMB1: {str(e)}", 0.04)
                            logging.error(f"Error disabling SMB1: {str(e)}")
                    
                    # Linux Hardening
                    elif system == "Linux":
                        ufw_path = shutil.which("ufw")
                        if ufw_path:
                            self._cinematic_typing("Enabling UFW firewall...", 0.04)
                            self._progress_bar("UFW Firewall", duration=2)
                            try:
                                subprocess.run(["sudo", ufw_path, "--force", "enable"], check=True)
                                self._cinematic_typing("[OK] UFW firewall enabled.", 0.04)
                                logging.info("UFW firewall enabled successfully on Linux")
                            except subprocess.CalledProcessError as e:
                                self._cinematic_typing(f"[!] Failed to enable UFW: {str(e)}", 0.04)
                                logging.error(f"Failed to enable UFW: {str(e)}")
                        else:
                            self._cinematic_typing("[!] UFW firewall not found — skipping Linux hardening", 0.04)
                
                except Exception as e:
                    logging.error(f"Hardening failed: {str(e)}")
                    print(f"{Fore.RED}[!] Error during hardening: {str(e)}{Style.RESET_ALL}")
            
            # ----------------------------
            # Cinematic completion with blinking
            # ----------------------------
            self._cinematic_typing("System fortification complete!", 0.05)
            
            # Blinking completion banner
            for _ in range(3):
                print(f"\r{Fore.GREEN}{self._center_text('▄︻デ══━ SYSTEM FORTIFICATION COMPLETE ══━︻▄')}{Style.RESET_ALL}", end="")
                time.sleep(0.3)
                print(f"\r{' ' * self.terminal_width}", end="")
                time.sleep(0.3)
            
            print(f"\n{Fore.GREEN}{self._center_text('▄︻デ══━ SYSTEM FORTIFICATION COMPLETE ══━︻▄')}{Style.RESET_ALL}")
            threat_level = random.randint(1, 10)
            
            # Blinking threat level
            threat_text = f" Firewall Active | Intrusion Prevention Engaged | Threat Level: {threat_level}/10"
            self._blinking_text(self._center_text(threat_text), Fore.YELLOW, 3)
            
        except Exception as e:
            # Catch-all to preserve cinematic end even on errors
            print(f"{Fore.RED}[!] Critical error: {str(e)}{Style.RESET_ALL}")
            self._cinematic_typing("System fortification complete with errors.", 0.05)
            print(f"\n{Fore.GREEN}{self._center_text('▄︻デ══━ SYSTEM FORTIFICATION COMPLETE ══━︻▄')}{Style.RESET_ALL}")
            threat_level = random.randint(1, 10)
            print(f"{Fore.YELLOW}{self._center_text(f' Firewall Active | Intrusion Prevention Engaged | Threat Level: {threat_level}/10')}{Style.RESET_ALL}")


    # go down here, don't remove these lines below
    def nikto_scan(self, target_url, port=80, output_file=None):
        """Run Nikto scan on a target URL."""
        cmd = f"nikto -h {target_url} -p {port}"
        if output_file:
            cmd += f" -o {output_file}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout

    def legitify_scan_github(self, org_or_repo, token=None):
        """Scan a GitHub org/repo for security issues."""
        cmd = f"legitify scan --github {org_or_repo}"
        if token:
            cmd += f" --token {token}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout

    def hash_file(self, filepath):
        hashes = {
            "md5": hashlib.md5(),
            "sha1": hashlib.sha1(),
            "sha256": hashlib.sha256()
        }

        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                for h in hashes.values():
                    h.update(chunk)

        return {name: h.hexdigest() for name, h in hashes.items()}

#   ---------------------------------
    def handle_command(self, cmd):
        cmd = cmd.strip()
        if not cmd:
            return

        original_cmd = cmd
        parts = cmd.split()
        cmd = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []


# -----------------------------starts here-------------
        if parts[0] == "mkdir" and len(parts) == 2:
            self.mkdir(parts[1])
            return

        elif parts[0] == "touch" and len(parts) == 2:
            self.touch(parts[1])
            return
 
        elif parts[0] == "ls":
            self.ls()
            return

            # Fix 2: Add the missing command handlers
        elif cmd == "crypto-list":
            self.handle_encrypted_files(args)
        elif cmd == "crypto-info":
            self.handle_crypto_info(args)
        elif cmd == "crypto-verify":
            self.handle_crypto_verify(args)
        elif cmd == "crypto-backup":
            self.handle_crypto_backup(args)

        elif cmd == "recon":
            if len(args) == 0:
                print("Usage: recon <target> OR recon -full <target>")
                return

            if args[0] == "-full":
                if len(args) < 2:
                    print("Usage: recon -full <target>")
                    return
                target = args[1]
                os.system(f"{sys.executable} recon_full.py {target}")
            else:
                target = args[0]
                os.system(f"{sys.executable} recon.py {target}")
            return

        elif cmd == "encrypt-test":
            self.handle_encrypt_test(args)

        elif parts[0] == "pwd":
            self.pwd()
            return
 
        elif parts[0] == "cd" and len(parts) == 2:
            self.cd(parts[1])
            return
            
        elif parts[0] == "cat" and len(parts) == 2:
            self.cat(parts[1])
            return
        
        elif parts[0] == "echo":
            self.handle_echo(cmd)
            return

# nmap-------------------
        elif parts[0] == "nmap":
            self.handle_nmap(parts[1:])
            return

# metasplo----------------
        elif parts[0] == "msf":
            self.handle_msf(parts[1:])
            return

    # ===== TruffleHog =====
        if parts[0] == "trufflehog":
            if "--git" in parts:
                try:
                    git_url = parts[parts.index("--git") + 1]
                    print(self.trufflehog_scan_git(git_url))
                except IndexError:
                    print("[!] Missing Git URL. Usage: trufflehog --git <URL>")
            elif "--fs" in parts:
                try:
                    fs_path = parts[parts.index("--fs") + 1]
                    print(self.trufflehog_scan_filesystem(fs_path))
                except IndexError:
                    print("[!] Missing filesystem path. Usage: trufflehog --fs <PATH>")
            else:
                print("Usage: trufflehog --git <URL> OR --fs <PATH>")

    # ===== Nikto =====
        elif parts[0] == "nikto":
            if "--url" not in parts:
                print("Usage: nikto --url <TARGET> [--port PORT] [--output FILE]")
                return
            try:
                target = parts[parts.index("--url") + 1]
                port = parts[parts.index("--port") + 1] if "--port" in parts else "80"
                output = parts[parts.index("--output") + 1] if "--output" in parts else None
                print(self.nikto_scan(target, port, output))
            except IndexError:
                print("[!] Invalid arguments. Usage: nikto --url <TARGET> [--port PORT] [--output FILE]")

    # ===== Legitify =====
        elif parts[0] == "legitify":
            if "--github" not in parts:
                print("Usage: legitify --github <ORG/REPO> [--token TOKEN]")
                return
            try:
                repo = parts[parts.index("--github") + 1]
                token = parts[parts.index("--token") + 1] if "--token" in parts else None
                print(self.legitify_scan_github(repo, token))
            except IndexError:
                print("[!] Invalid arguments. Usage: legitify --github <ORG/REPO> [--token TOKEN]")

    # Original commands (scan, netmon, etc.)
        elif original_cmd.lower() == "system scan -all":
            self.scan_system()
            self.show_tip("system scan -all")
            return

        elif original_cmd.lower() == "net -n mon":
            self.network_monitor()
            self.show_tip("net -n mon")
            return

        # ===================================

        elif cmd == "crypto-list" or cmd == "encrypted-files":
            self.handle_encrypted_files(args)
        elif cmd == "crypto-info":
            self.handle_crypto_info(args)
        elif cmd == "crypto-verify":
            self.handle_crypto_verify(args)
        elif cmd == "crypto-backup":
                self.handle_crypto_backup(args)
        elif cmd == "encrypt-test":
            self.handle_encrypt_test(args)

    #  for clear command to clean terminal
    # Add to  command handler:
        elif cmd == "transfertrace":
            self.financial_simulator()
            # Add to your command handler:
        elif original_cmd.lower() == "extract -money":
            self.financial_simulator()
        elif original_cmd.lower() == "clear terminal":
            self.clear_terminal()
            self.show_tip(cmd)

        elif cmd == "clear":
            self.clear_terminal()
            self.show_tip(cmd)
        elif original_cmd.lower() == "shutdown":
            self.emergency_shutdown()
    

# ================================================
    # exploit check and mac address change
        elif cmd == "exploitcheck": 
            self.check_exploits()
            self.show_tip(cmd)
        elif cmd.startswith("macspoof"): 
            self.spoof_mac(cmd.split()[1] if len(cmd.split()) > 1 else "enp3s0")
            self.show_tip(cmd)

    #  sqlmap and log clearing
        elif cmd.startswith("sqlmap"): 
            self.sql_injection_scan(cmd.split()[1] if len(cmd.split()) > 1 else input("Target URL: "))
            self.show_tip(cmd)
        elif cmd == "clearlogs": 
            self.clear_logs()
            self.show_tip(cmd)

    # portsweep and hashing file commands
        elif cmd.startswith("portsweep"): 
            target = cmd.split()[1] if len(cmd.split()) > 1 else "127.0.0.1"
            self.port_scan(target)
            self.show_tip(cmd)

        elif cmd.startswith("hashfile"): 
            file_path = cmd.split()[1] if len(cmd.split()) > 1 else input("File path: ")
            hashes = self.hash_file(file_path)
            for algo, hash_val in hashes.items():
                print(f"{algo.upper()}: {hash_val}")
            self.show_tip(cmd)

    #  system information detailed part and force killing of running processes
        elif cmd == "sysinfo": 
            self.system_info()
            self.show_tip(cmd)

        elif cmd.startswith("killproc"): 
            self.kill_process(int(cmd.split()[1])) if len(cmd.split()) > 1 else print("Usage: killproc PID")
            self.show_tip(cmd)

    # ==================check integrity and encrypt or decrypt files/folders
        elif original_cmd.lower() == "check integrity": 
            self.check_integrity()
            self.show_tip(cmd)
        elif cmd.startswith("encrypt"): 
            self.encrypt_file(cmd.split()[1] if len(cmd.split()) > 1 else input("File to encrypt: "))
            self.show_tip(cmd)
        elif cmd.startswith("decrypt"): 
            args = cmd.split()
            if len(args) > 2: 
                self.decrypt_file(args[1], args[2])
                self.show_tip(cmd)
            else: 
                print("Usage: decrypt FILE.enc KEY")
                

    # =====================================

        elif cmd == "encrypt":
            self.handle_encrypt(args)
        elif cmd == "decrypt":
            self.handle_decrypt(args)

        elif cmd in ["encrypt-setup", "crypto-init"]:
            self.handle_encryption_setup(args)

        elif cmd == "crypto-status":
            self.show_crypto_status()

        elif cmd.startswith("watchfolder"): 
            self.watch_folder(cmd.split()[1] if len(cmd.split()) > 1 else ".")
            self.show_tip(cmd)
        elif cmd.startswith("traceroute"): 
            self.trace_route(cmd.split()[1] if len(cmd.split()) > 1 else "8.8.8.8")
            self.show_tip(cmd)
        elif cmd == "ransomwatch": 
            self.monitor_ransomware()
            self.show_tip(cmd)
        elif cmd.startswith("wificrack"): 
            self.wifi_audit(cmd.split()[1] if len(cmd.split()) > 1 else "wlp2s0")
            self.show_tip(cmd)
        elif cmd.startswith("stegcheck"): 
            self.check_steganography(cmd.split()[1] if len(cmd.split()) > 1 else input("Image path: "))
            self.show_tip(cmd)

        elif cmd.startswith("certcheck"):
        # Handle both command line input and interactive prompt
            if len(cmd.split()) > 1:
                domain = cmd.split()[1]
                self.check_ssl(domain)
                self.show_tip(cmd)
            else:
                self.check_ssl()  # Will prompt for domain inside the method

        elif cmd == "memdump": 
            self.dump_memory()
            self.show_tip(cmd)
        elif cmd == "torify": 
            self.enable_tor_routing()
            self.show_tip(cmd)
        elif cmd == "update": 
            print(f"\n[+] {self.check_updates()}")
            self.show_tip(cmd)
        elif cmd == "vt-scan": 
            self.vt_scan_menu()
            self.show_tip(cmd)
            # return
        elif original_cmd.lower() == "registry -n mon": 
            print(self.monitor_registry())
            self.show_tip(cmd)
        elif original_cmd.lower() == "harden -t sys": 
            self.harden_system(dry_run=False)
            self.show_tip(cmd)

        elif cmd == "help": 
            self.show_help()
        elif cmd == "exit": 
            print("\n[*] Exiting Defensive Security Terminal")
            sys.exit(0)
        else: 
            print("[!] Unknown command. Type 'help' for more command options.")
            self.show_tip(cmd)  # <-- Add this line at the end

    # ==================== HELP MENU ====================
    def show_help(self):
        help_text = """
                    _____________DSTerminal Commands Help Menu______________:
    
    === Core Security ========
    system scan -All                              - System threat scan (sys, apps, net e.t.c)
    net -n mon                                          - Live network monitoring
    exploitcheck                                        - Check for critical CVEs
    vtscan                                              - VirusTotal file analysis
    clearlogs                                           - Securely wipe system logs
    nikto --url <TARGET>                                - Web vulnerability scan")
    legitify --github <ORG/REPO>                        - Scan GitHub for misconfigurations")

    === Network Tools ========
    portsweep [IP]                                      - Scan target for open ports
    traceroute [IP]                                     - Network path analysis
    torify                                              - Route traffic through Tor
    dnssec [DOMAIN]                                     - Validate DNSSEC
    
    === Forensics & Financial Crime Analysis ============
    memdump                       - Capture volatile memory (for analysis)
    hashfile [PATH]               - Generate file integrity hashes
    stegcheck [IMG]               - Detect hidden or embedded image data
    ransomwatch                   - Identify ransomware indicators
    finanalyze                    - Analyze suspicious financial transactions
    transfertrace                 - Trace and simulate transaction flows
     
    === System Management ====
    sysinfo                                             - Detailed system report
    killproc PID                                        - Terminate process
    macspoof [IFACE]                                    - Randomize MAC address
    harden -t sys                                       - Apply security hardening
    
    ===  Cryptography (Crypto Tools) ===
    encrypt FILE                                        - AES-256 file encryption
    decrypt FILE KEY                                    - File decryption
    
    === Web Security ========
    sqlmap [URL]                                        - SQL injection scan
                                                        - "-u", url,
                                                        - "--batch",  # Non-interactive
                                                        - "--risk=3",  # Higher risk level
                                                        - "--level=5",  # Thorough testing
                                                        - "--crawl=1",  # Limited crawling
                                                        - "--random-agent",
                                                        - "--output-dir=./sqlmap_results"

    certcheck [DOMAIN]                                  - SSL certificate audit
    
    === Monitoring ==========
    watchfolder [PATH]                                  - Directory change detection
    regmon                                              - Windows registry monitor
    
    === Utilities ===========
    update                                              - Check for DST updates
    help                                                - Show this menu
    exit                                                - Quit terminal
    clear                                               - Cleaning up your terminal previous commands
    clear terminal                                      - Cleaning up your terminal history commands
    shutdown                                            - Emergency shutting down
    shutdown now                                        - To shutdown your machine immediately

    ===🔐 ENCRYPTION COMMANDS:
    encrypt <file>                                      - Encrypt a file
    decrypt <file.enc>                                  - Decrypt a file
    crypto-list                                         - List all encrypted files
    crypto-info <file.enc>                              - Show encryption info
    crypto-verify                                       - Verify encryption system
    crypto-backup                                       - Backup encryption key
    encrypt-test                                        - Run encryption test
    encrypt-setup                                       - Setup encryption system
  
    ===📁 FILE COMMANDS:
    ls                                                  - List files
    cat <file>                                          - Show file contents
    touch <file>                                        - Create file
    echo <text> > <file>                                - Write to file
    pwd                                                 - Show current directory
  
    ⚡ SECURITY COMMANDS:
    sysinfo                                             - System information
    metasploit                                          - Launch Metasploit
    tor-start                                           - Start Tor proxy
    tor-check                                           - Check Tor connection
    """
        print(help_text)

    def run(self):
            self.print_banner()
            while True:
                try:
                        prompt_text = HTML('<ansigreen><b>[-- DFFENEX</b></ansigreen>'
                               '<ansiblue>@</ansiblue>'
                               '<ansigreen><b>DSTerminal</b></ansigreen> '
                               '<ansired>]-[]</ansired> ')
                        user_input = self.session.prompt(prompt_text)
                        self.handle_command(user_input.strip())
                except KeyboardInterrupt:
                    print("\n[*] Use 'exit' to quit")
                except Exception as e:
                    print(f"[!] Error: {str(e)}")

if __name__ == "__main__":
    terminal = SecurityTerminal()
    terminal.run()