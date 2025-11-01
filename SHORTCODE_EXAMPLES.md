# Shortcode Usage Examples

This file contains all shortcode examples from the blog post for reference.

## Tool Shortcode

```html
{{< tool tool="nmap" />}}
```

```html
{{< tool tool="burp suite" />}}
```

Inline usage:
```
In this walkthrough, we'll use {{< tool tool="nmap" />}} for port scanning.
```

## Difficulty Shortcode

```html
{{< difficulty level="beginner" />}}
```

```html
{{< difficulty level="intermediate" />}}
```

```html
{{< difficulty level="advanced" label="Custom Label" />}}
```

## Callout Shortcode

```html
{{< callout type="info" title="Information" >}}Important info{{< /callout >}}

{{< callout type="warning" title="Warning" >}}Be careful!{{< /callout >}}

{{< callout type="success" title="Success" >}}Task completed{{< /callout >}}

{{< callout type="danger" title="Danger" >}}Critical warning{{< /callout >}}

{{< callout type="tip" title="Tip" >}}Helpful hint{{< /callout >}}

{{< callout type="question" title="Question" >}}Common question{{< /callout >}}

{{< callout type="example" title="Example" >}}Code example{{< /callout >}}

{{< callout type="note" title="Note" >}}Important note{{< /callout >}}

{{< callout type="abstract" title="Abstract" >}}Summary{{< /callout >}}

{{< callout type="quote" title="Quote" >}}Quote{{< /callout >}}

{{< callout type="bug" title="Bug" >}}Bug report{{< /callout >}}

```

## Terminal Shortcode

```html
{{< terminal command="nmap -sC -sV 10.10.10.10" >}}Starting Nmap scan...
Host is up (0.050s latency).{{< /terminal >}}

```

## Complete CTF Walkthrough Example

```markdown
# Machine Overview

{{< difficulty level="beginner" label="Beginner Level" />}}

Platform: {{< tool tool="HackTheBox" />}}

## Initial Reconnaissance

{{< callout type="info" title="Port Scan" >}}Using nmap to find open ports.{{< /callout >}}

Let's scan the target:
```bash
nmap -sC -sV 10.10.10.10
```

## Service Exploitation

{{< terminal command="ftp 10.10.10.10" >}}Connected to target.{{< /terminal >}}

## Success

{{< callout type="success" title="Rooted!" >}}Gained administrative access.{{< /callout >}}

## Tools Used

{{< tool tool="nmap" />}} {{< tool tool="burp suite" />}} {{< tool tool="sqlmap" />}}

This entire walkthrough: {{< difficulty level="beginner" label="Beginner Friendly" />}}
```
