# Nmap Command Reference

> [!info] Quick Reference Guide
> **For:** Penetration Testers, Security Professionals, Network Administrators
> **Version:** 7.94+
> **Last Updated:** November 2024

## 🔍 Common Commands

### Basic Port Scanning

```bash
# Scan a single host
nmap 192.168.1.1

# Scan a range of IPs
nmap 192.168.1.1-100

# Scan multiple specific IPs
nmap 192.168.1.1 192.168.1.10 192.168.1.100

# Scan from file (targets.txt)
nmap -iL targets.txt

# Scan entire subnet
nmap 192.168.1.0/24
```

### Host Discovery

```bash
# Ping scan (no port scan)
nmap -sn 192.168.1.0/24

# ARP scan (local network)
nmap -sn --packet-trace 192.168.1.0/24

# Disable ping (assume host is up)
nmap -Pn 192.168.1.1

# TCP SYN ping
nmap -PS22,80,443 192.168.1.1

# TCP ACK ping
nmap -PA80 192.168.1.1

# UDP ping
nmap -PU53 192.168.1.1
```

### Port Scanning Types

```bash
# TCP connect scan (full connection)
nmap -sT 192.168.1.1

# TCP SYN scan (stealthy)
nmap -sS 192.168.1.1

# UDP scan
nmap -sU 192.168.1.1

# TCP ACK scan
nmap -sA 192.168.1.1

# TCP Window scan
nmap -sW 192.168.1.1

# TCP Maimon scan
nmap -sM 192.168.1.1
```

### Service and Version Detection

```bash
# Service version detection
nmap -sV 192.168.1.1

# Aggressive service detection
nmap -sV --version-intensity 9 192.168.1.1

# Light service detection
nmap -sV --version-intensity 0 192.168.1.1

# Light banner grabbing
nmap -sV --version-intensity 0 192.168.1.1

# OS detection
nmap -O 192.168.1.1

# Aggressive OS detection
nmap -O --osscan-guess 192.168.1.1

# OS and service detection combined
nmap -sV -O 192.168.1.1
```

### Timing and Performance

```bash
# T0 (paranoid) - slowest, stealthy
nmap -T0 192.168.1.1

# T1 (sneaky) - slow, stealthy
nmap -T1 192.168.1.1

# T2 (polite) - slower, less bandwidth
nmap -T2 192.168.1.1

# T3 (normal) - default timing
nmap -T3 192.168.1.1

# T4 (aggressive) - faster
nmap -T4 192.168.1.1

# T5 (insane) - fastest
nmap -T5 192.168.1.1

# Custom timing
nmap --host-timeout 60s 192.168.1.1
nmap --max-rate 1000 192.168.1.1
nmap --min-rate 100 192.168.1.1
```

## 📝 Syntax Reference

### Output Formats

```bash
# Normal output to terminal
nmap 192.168.1.1

# XML output
nmap -oX scan.xml 192.168.1.1

# Grepable output
nmap -oG scan.txt 192.168.1.1

# All output formats
nmap -oA scan 192.168.1.1

# Append to file
nmap -oA scan --append-output 192.168.1.1

# Verbose output
nmap -v 192.168.1.1

# Very verbose
nmap -vv 192.168.1.1

# Debug mode
nmap -d 192.168.1.1

# Maximum debug
nmap -dd 192.168.1.1
```

### Script Engine (NSE)

```bash
# Default safe scripts
nmap --script default 192.168.1.1

# Vuln scripts
nmap --script vuln 192.168.1.1

# Exploit scripts
nmap --script exploit 192.168.1.1

# Discovery scripts
nmap --script discovery 192.168.1.1

# Auth scripts
nmap --script auth 192.168.1.1

# Intrusive scripts (may trigger IDS/IPS)
nmap --script intrusive 192.168.1.1

# All scripts
nmap --script all 192.168.1.1

# Specific script
nmap --script http-title 192.168.1.1

# Multiple scripts
nmap --script http-title,http-headers,ssl-cert 192.168.1.1

# Script arguments
nmap --script smb-vuln-ms17-010 --script-args smbuser=admin,smbpass=password 192.168.1.1
```

## 🎯 Quick Tips

> [!tip] Pro Tips
> - Use `-sS` (SYN scan) instead of `-sT` for faster, stealthier scans
> - Always use `-sV` for service version detection
> - Add `-O` for OS fingerprinting on important targets
> - Use `-Pn` when pings are blocked by firewalls
> - Save output with `-oX` or `-oG` for professional reports
> - Start with `-sn` for host discovery, then port scan live hosts

## 🚨 Common Pitfalls

- **Full TCP Connect Scans**: Using `-sT` instead of `-sS` is slower and more likely to be logged
- **Not Using Scripts**: NSE scripts provide valuable additional information
- **Forgetting `-Pn`**: Systems may block ICMP, making them appear offline
- **Aggressive Timing on Prod**: `-T5` can crash unstable systems or trigger IDS/IPS
- **Ignoring Firewall Rules**: Firewalls may block common ports, use port ranges

## 🔗 Useful Resources

- [Nmap Official Documentation](https://nmap.org/docs.html)
- [Nmap Scripting Engine](https://nmap.org/nsedoc/)
- [Nmap Reference Guide](https://nmap.org/man/man-briefoptions.html)
- [Port Scanning Techniques](https://nmap.org/man/man-port-scanning-techniques.html)
- [NSE Category Reference](https://nmap.org/nsedoc/categories/)

## 📊 Cheat Sheet

| Command | Description | Example |
|---------|-------------|---------|
| `nmap -sS` | TCP SYN stealth scan | `nmap -sS 192.168.1.1` |
| `nmap -sV` | Service version detection | `nmap -sV 192.168.1.1` |
| `nmap -O` | OS fingerprinting | `nmap -O 192.168.1.1` |
| `nmap -p` | Specify ports | `nmap -p 80,443,8080 192.168.1.1` |
| `nmap -A` | Aggressive detection (OS, version, script, traceroute) | `nmap -A 192.168.1.1` |
| `nmap -sU` | UDP scan | `nmap -sU 192.168.1.1` |
| `nmap -sn` | Host discovery only | `nmap -sn 192.168.1.0/24` |
| `nmap -Pn` | Disable ping | `nmap -Pn 192.168.1.1` |
| `nmap -T4` | Aggressive timing | `nmap -T4 192.168.1.1` |
| `nmap --script` | Run NSE scripts | `nmap --script vuln 192.168.1.1` |
| `nmap -oX` | XML output | `nmap -oX scan.xml 192.168.1.1` |
| `nmap -oG` | Grepable output | `nmap -oG scan.txt 192.168.1.1` |
| `nmap -iL` | Targets from file | `nmap -iL targets.txt` |
| `nmap -v` | Verbose output | `nmap -v 192.168.1.1` |
| `nmap --top-ports` | Scan most common ports | `nmap --top-ports 100 192.168.1.1` |
| `nmap -p-` | Scan all 65535 ports | `nmap -p- 192.168.1.1` |
| `nmap --script vuln` | Vulnerability detection scripts | `nmap --script vuln 192.168.1.1` |
| `nmap --script exploit` | Exploitation scripts | `nmap --script exploit 192.168.1.1` |
| `nmap --script http-title` | Get HTTP page titles | `nmap --script http-title 192.168.1.1` |
| `nmap --script ssl-enum-ciphers` | SSL/TLS cipher enumeration | `nmap --script ssl-enum-ciphers 192.168.1.1` |
| `nmap --script smb-vuln-*` | SMB vulnerability checks | `nmap --script smb-vuln-* 192.168.1.1` |

### Port Range Examples

```bash
# Specific ports
nmap -p 22,80,443 192.168.1.1

# Port range
nmap -p 1-1000 192.168.1.1

# All ports
nmap -p- 192.168.1.1

# Top 1000 ports
nmap --top-ports 1000 192.168.1.1

# Fast scan common ports
nmap -F 192.168.1.1
```

### Script Categories

| Category | Description |
|----------|-------------|
| `auth` | Authentication scripts |
| `broadcast` | Network broadcasts |
| `brute` | Password brute force |
| `default` | Default safe scripts |
| `discovery` | Network discovery |
| `dos` | Denial of service |
| `exploit` | Exploitation scripts |
| `external` | External resources |
| `fuzzer` | Fuzzing scripts |
| `intrusive` | Potentially intrusive |
| `malware` | Malware detection |
| `safe` | Safe, non-intrusive |
| `version` | Version detection |
| `vuln` | Vulnerability detection |

### Useful One-Liners

```bash
# Quick service and OS detection
nmap -sV -O 192.168.1.1

# Stealthy scan with scripts
nmap -sS --script vuln 192.168.1.1

# Web server enumeration
nmap -sV --script http-enum,http-title,http-headers 192.168.1.1

# SMB enumeration
nmap -sV --script smb-enum-shares,smb-enum-users 192.168.1.1

# SSL/TLS analysis
nmap -sV --script ssl-cert,ssl-enum-ciphers 192.168.1.1

# UDP service detection
nmap -sU --script dns-query 192.168.1.1

# Comprehensive web scan
nmap -sS -sV -p 80,443,8080,8443 --script http-* 192.168.1.1
```


*Keep this reference handy for quick lookups!*
