---
title: "HackTheBox - Starting Point: Meow Walkthrough"
date: 2025-11-01T21:00:00+05:30
draft: false
categories: ["CTF", "HackTheBox", "Walkthrough"]
tags: ["telnet", "network", "enumeration", "beginner"]
difficulties: ["beginner"]
platforms: ["HackTheBox"]
tools: ["nmap", "telnet"]
description: "Complete walkthrough of the HackTheBox Starting Point Meow machine - a beginner-friendly CTF covering basic enumeration and telnet access."
---

<div class="difficulty-badge difficulty-beginner">Beginner Level</div>

## Introduction

Meow is the first machine in HackTheBox's Starting Point series. This beginner-friendly CTF teaches basic enumeration techniques and demonstrates how simple misconfigurations can lead to system compromise.

**Target:** 10.10.10.10
**Objective:** Find the flag in the `/root` directory

<div class="callout callout-info">
<div class="callout-title">📋 Prerequisites</div>
- Basic understanding of Linux commands
- Familiarity with networking concepts
- Nmap installed (or use the online version)
</div>

## Initial Enumeration

### Port Scanning with Nmap

We'll start with a comprehensive port scan to identify open services:

```bash
nmap -sC -sV -oA initial_scan 10.10.10.10
```

**Results:**
```
PORT   STATE SERVICE VERSION
23/tcp open  telnet  Linux telnetd
```

<div class="callout callout-warning">
<div class="callout-title">⚠️ Important</div>
Port 23 (Telnet) is open. Telnet transmits data in plaintext, making it a security risk.
</div>

### Connecting to Telnet

Since Telnet is open and doesn't require authentication by default (in this case), let's connect:

```bash
telnet 10.10.10.10
```

## Gaining Access

Upon connecting, we might be dropped into a shell directly. Let's check what user we're running as:

```bash
whoami
# Result: root
```

Great! We have root access without any authentication. This demonstrates the dangers of leaving services unsecured.

## Finding the Flag

Navigate to the root directory and locate the flag:

```bash
ls -la /root
cat /root/flag.txt
```

**Flag:** `HTB{xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx}`

<div class="callout callout-success">
<div class="callout-title">✅ Success!</div>
You've successfully compromised your first HTB machine! The flag has been captured.
</div>

## Summary and Key Takeaways

### What We Learned:
1. **Basic Enumeration**: Using nmap to discover open ports
2. **Service Identification**: Recognizing Telnet as a potential entry point
3. **Direct Access**: Exploiting misconfigured services
4. **Privilege Escalation**: Already at root (no escalation needed)

### Security Lessons:
- Never leave services like Telnet exposed without authentication
- Always use encrypted protocols (SSH instead of Telnet)
- Implement proper access controls on all network services

### Commands Used:
- `nmap`: Network scanner
- `telnet`: Insecure remote shell protocol
- `whoami`: Check current user
- `ls` and `cat`: File navigation and reading

## Additional Resources

- [HackTheBox Starting Point Guide](https://help.hackthebox.com)
- [Nmap Documentation](https://nmap.org/docs.html)
- [Telnet Security Risks](https://www.fortinet.com/blog/industry-trends/telnet-is-dead-long-live-secure-shell)

## Related Posts

- [HackTheBox - Dancing Walkthrough](/posts/hackthebox-dancing-walkthrough)
- [Basic Network Enumeration Techniques](/posts/basic-network-enumeration)
- [Understanding Common Services](/posts/understanding-common-services)

---

*Happy hacking! Stay ethical and always get proper authorization before testing.*
