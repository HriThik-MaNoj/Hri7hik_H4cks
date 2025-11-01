# {{CTF Name}} - {{Machine Name}} Walkthrough

> [!info] Information
> **Platform:** {{Platform Name}}
> **Difficulty:** {{Difficulty Level}}
> **Target:** {{Target IP}}
> **Objective:** {{Objective Description}}

## 📋 Table of Contents

- [Introduction](#introduction)
- [Reconnaissance](#reconnaissance)
- [Initial Access](#initial-access)
- [Privilege Escalation](#privilege-escalation)
- [Flag Finding](#flag-finding)
- [Summary](#summary)

## Introduction

Brief introduction to the {{CTF Name}} {{Machine Name}} machine. Explain what makes this machine interesting and what techniques will be covered.

### Target Information

- **IP Address:** {{Target IP}}
- **Operating System:** {{OS Name}}
- **Difficulty:** {{Difficulty Level}}
- **Tags:** {{Relevant Tags}}

### What You'll Learn

{{List the key concepts and techniques covered in this walkthrough}}

## Reconnaissance

### Initial Port Scan

> [!tip] Tip
> Always start with a comprehensive port scan to understand what services are running.

```bash
nmap -sC -sV -oA initial_scan {{Target IP}}
```

**Results:**
```
{{Port scan results}}
```

### Detailed Service Enumeration

#### Service 1: {{Service Name}}

{{Description of the service and any interesting findings}}

```bash
{{Relevant enumeration command}}
```

#### Service 2: {{Service Name}}

{{Description of the service and any interesting findings}}

### Web Directory Enumeration

If web services are found, enumerate directories:

```bash
gobuster dir -u http://{{Target IP}} -w /usr/share/wordlists/dirb/common.txt
```

## Initial Access

### Exploitation Method: {{Method Name}}

{{Detailed explanation of the exploitation technique}}

> [!warning] Warning
> {{Important warning or note about the exploitation method}}

```bash
{{Exploitation command}}
```

{{Output or result of the exploitation}}

### Initial Shell

Once we have access, let's gather basic information:

```bash
whoami
id
uname -a
```

## Privilege Escalation

### Enumeration for PrivEsc

{{Step-by-step privilege escalation enumeration}}

```bash
{{Privilege escalation enumeration commands}}
```

### Privilege Escalation: {{Method Name}}

{{Detailed explanation of the privilege escalation technique}}

```bash
{{Privilege escalation command}}
```

### Verify Elevated Privileges

```bash
whoami
id
```

## Flag Finding

{{Description of flag location and retrieval}}

```bash
{{Command to find and read the flag}}
```

**Flag:** `{{Flag Value}}`

> [!success] Success!
> Congratulations! You've successfully completed the {{Machine Name}} box.

## Summary

### What We Learned

1. {{Lesson 1}}
2. {{Lesson 2}}
3. {{Lesson 3}}

### Key Takeaways

{{Important security lessons and best practices}}

### Tools Used

> [!example] Tools
> {{tool "nmap"}} {{tool "gobuster"}} {{tool "netcat"}} {{tool "{{Custom Tool}}"}}

### Commands Summary

- `{{Command 1}}`: {{Description}}
- `{{Command 2}}`: {{Description}}
- `{{Command 3}}`: {{Description}}

## Additional Resources

- [{{Resource Name 1}}]({{URL 1}})
- [{{Resource Name 2}}]({{URL 2}})

## Related Writeups

- [[{{Related Writeup 1}}]]
- [[{{Related Writeup 2}}]]

---

*Remember: Always practice ethical hacking and only test systems you own or have explicit permission to test.*
