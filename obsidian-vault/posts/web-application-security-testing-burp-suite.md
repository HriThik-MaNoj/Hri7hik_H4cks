# Web Application Security Testing with Burp Suite

> [!info] Tutorial Information
> **Category:** Web Application Security
> **Difficulty:** Beginner
> **Prerequisites:** Basic understanding of HTTP, HTML, and web applications
> **Estimated Time:** 90 minutes

## 📋 Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Step-by-Step Guide](#step-by-step-guide)
- [Best Practices](#best-practices)
- [Common Mistakes](#common-mistakes)
- [Troubleshooting](#troubleshooting)
- [Conclusion](#conclusion)

## Introduction

Burp Suite is the industry-standard web application security testing platform. This comprehensive tutorial will guide you through setting up, configuring, and using Burp Suite for effective web application security testing.

### What You'll Learn

By the end of this tutorial, you'll be able to:

- Install and configure Burp Suite
- Set up your browser to work with Burp Proxy
- Intercept and modify HTTP requests
- Use the Repeater and Intruder tools effectively
- Configure Scanner extensions
- Generate professional security reports
- Test for common web vulnerabilities (SQLi, XSS, CSRF)

### Use Cases

- Penetration testing engagements
- Bug bounty programs
- Web application security assessments
- Secure code review support
- DevSecOps integration

## Prerequisites

> [!warning] Important
> Before starting this tutorial, ensure you have the following:

### Knowledge Prerequisites

- Basic understanding of web technologies (HTTP, HTTPS, HTML, JavaScript)
- Familiarity with web applications and their architectures
- Understanding of the OWASP Top 10 vulnerabilities
- Basic command-line knowledge (Linux/macOS/Windows)

### Tool Prerequisites

> [!tip] Required Tools
> - [Burp Suite Community Edition](https://portswigger.net/burp/communitydownload) (Free) or Professional
> - [Mozilla Firefox](https://www.mozilla.org/) or [Google Chrome](https://www.google.com/chrome/)
> - [Java Runtime Environment](https://www.oracle.com/java/technologies/downloads/) (JRE 11 or higher)

### System Prerequisites

- Minimum 4GB RAM (8GB recommended for professional testing)
- At least 2GB free disk space
- Administrative privileges to install software

## Step-by-Step Guide

### Step 1: Install Burp Suite

Download and install Burp Suite Community Edition from the official website.

**On Linux:**
```bash
# Download the JAR file
wget https://portswigger.net/burp/releases/download?product=community&version=2024.6.1#tab/linux

# Make executable and run
chmod +x burpsuite_community.jar
java -jar burpsuite_community.jar
```

**On Windows:**
- Download the installer from the website
- Run the installer as administrator
- Follow the installation wizard

**On macOS:**
```bash
# Using Homebrew
brew install --cask burp-suite
```

### Step 2: Configure Proxy Settings

Launch Burp Suite and configure the proxy listener.

```bash
# Default proxy settings (can be customized)
Proxy Host: 127.0.0.1
Proxy Port: 8080
```

> [!note] Note
> These are the default settings. You can change them in Proxy > Options.

### Step 3: Configure Browser Proxy Settings

**Firefox:**
1. Open Firefox
2. Go to Settings > General > Network Settings
3. Select "Manual proxy configuration"
4. Set HTTP Proxy: 127.0.0.1, Port: 8080
5. Check "Use this proxy server for all protocols"
6. Click OK

**Chrome:**
- Install "Proxy SwitchyOmega" extension
- Or start Chrome with proxy flags:
```bash
google-chrome --proxy-server=127.0.0.1:8080
```

### Step 4: Install CA Certificate (HTTPS)

1. In Burp Suite, go to Proxy > Options
2. Click "Import/export CA certificate"
3. Export as "Certificate in DER format"
4. In browser, import the certificate into Trusted Root Certification Authorities

> [!danger] Security Warning
> Never export or share your private CA certificate. It allows full interception of HTTPS traffic.

### Step 5: Intercept Your First Request

1. Ensure Burp Proxy is running (Proxy tab, Intercept is on)
2. Navigate to a website through your browser
3. You should see HTTP requests in the Proxy > HTTP history tab

### Step 6: Understanding the Interface

**Proxy Tab:**
- **Intercept**: Capture requests before they're sent
- **HTTP History**: View all requests and responses
- **WebSockets**: Monitor WebSocket connections

**Target Tab:**
- **Site Map**: Organize discovered URLs
- **Issue Definitions**: Configure vulnerability checks
- **Scan Queue**: Monitor scanning progress

**Intruder Tab:**
- **Positions**: Define attack points
- **Payloads**: Configure injection data
- **Options**: Fine-tune attack parameters

**Repeater Tab:**
- Manually modify and resend requests
- Perfect for testing specific injection points

### Step 7: Test for SQL Injection

Select a request with parameters (e.g., login form), send to Repeater.

```bash
# Original request
POST /login.php HTTP/1.1
Host: target.local
Content-Type: application/x-www-form-urlencoded

username=test&password=test
```

**SQL Injection Test (Single Quote):**
```bash
username=test'&password=test
```

**Response Analysis:**
- If error appears: potential SQLi vulnerability
- Use boolean-based testing: `test' OR '1'='1`
- Use time-based testing: `test'; WAITFOR DELAY '00:00:05'--`

### Step 8: Test for Cross-Site Scripting (XSS)

Identify reflected parameters and test:

```bash
# Reflected XSS test
<script>alert('XSS')</script>

# More advanced test
"><script>alert('XSS')</script>
```

### Step 9: Use Intruder for Automated Testing

Send a request to Intruder and configure positions:

1. **Target Definition:**
```bash
POST /search.php?q=§test§ HTTP/1.1
Host: target.local
```

2. **Payload Configuration:**
- Payload Type: Simple List
- Add common SQL injection payloads:
  - `' OR '1'='1`
  - `' OR 1=1--`
  - `admin'--`
  - `' UNION SELECT 1,2,3--`

3. **Start Attack:**
Click "Start Attack" and analyze results for error messages or timing differences.

### Step 10: Configure Extensions

**Essential Extensions:**

1. **J2EEScan**: Tests for J2EE vulnerabilities
2. **Param Miner**: Discovers hidden parameters
3. **Software Vulnerability Scanner**: Checks for known CVEs
4. **WSTL Checker**: Validates Web Application Security Testing Language

### Step 11: Generate Security Reports

1. Go to Target tab
2. Right-click on your target site
3. Select "Report selected issues"
4. Choose HTML format
5. Include: Executive summary, Detailed findings, Remediation advice

### Step 12: Best Practices for Testing

- Always get written authorization before testing
- Test in a non-production environment when possible
- Use the "Scope" feature to limit testing to authorized areas
- Save sessions frequently
- Document all findings with screenshots
- Respect rate limits and server resources

## Best Practices

> [!success] Best Practices
> Follow these best practices to ensure effective and ethical testing:

1. **Scope Management**
   - Define clear scope in written authorization
   - Use Target Scope to limit testing
   - Document out-of-scope targets

2. **Session Management**
   - Use Session Handling Rules for complex authentication
   - Test logout and re-login scenarios
   - Verify session timeouts

3. **Reporting Standards**
   - Classify findings by severity (Critical, High, Medium, Low)
   - Provide proof-of-concept for each vulnerability
   - Include remediation steps for developers

4. **Efficient Testing Workflow**
   - Use Target Site Map for organization
   - Utilize passive scanning features
   - Save and organize your Burp projects

## Common Mistakes

> [!danger] Common Mistakes to Avoid

### Mistake 1: Not Configuring Proxy Correctly

**Incorrect:**
- Using Burp without configuring browser proxy
- HTTPS sites not working due to missing CA certificate

**Correct:**
- Properly configure browser proxy settings
- Import and trust Burp's CA certificate
- Verify all HTTP/HTTPS traffic is intercepted

### Mistake 2: Testing Out of Scope

**Explanation of why this is a mistake:**
Testing systems or endpoints not covered by your authorization can have legal consequences.

**Correct Approach:**
- Define and document scope clearly
- Configure Target Scope in Burp Suite
- Respect robots.txt and rate limits

### Mistake 3: Over-Reliance on Automated Scanning

**Explanation:**
Automated scanners miss business logic vulnerabilities and complex attack chains.

**Correct Approach:**
- Combine automated scanning with manual testing
- Use Scanner for coverage, manual testing for depth
- Test user workflows and business logic

## Troubleshooting

> [!question] Frequently Asked Questions

### Q: Burp Suite won't intercept HTTPS traffic

**A:** This is usually due to SSL certificate issues:
1. Ensure Burp's CA certificate is imported and trusted
2. Check that proxy settings are correct in browser
3. Restart both browser and Burp Suite
4. Verify "Support invisible proxying" is enabled (if using proxy chains)

### Q: How to test mobile applications?

**A:** You can test mobile apps by:
1. Setting your computer as a proxy on the mobile device
2. Install Burp's CA certificate on mobile device
3. Configure mobile device to route traffic through your computer's IP
4. Use "Proxy > Options > Request Handling" to allow other devices

### Q: Scanner doesn't detect vulnerabilities in my application

**A:** This is common with business logic flaws:
1. Scanner only checks for known patterns and signatures
2. Manual testing is essential for custom vulnerabilities
3. Configure active scanning for better coverage
4. Use Intruder for customized attack vectors

## Hands-On Exercise

> [!example] Practice Exercise
> Try this exercise to solidify your understanding:

Set up a vulnerable web application (DVWA) and practice:

1. Configure Burp Suite proxy
2. Intercept login attempts
3. Test SQL injection in the login form
4. Use Intruder for automated brute force
5. Test for reflected XSS in search functionality
6. Generate a professional security report

### Exercise Setup Commands

```bash
# Install DVWA (requires LAMP stack)
sudo apt update
sudo apt install apache2 mysql-server php libapache2-mod-php php-mysql
git clone https://github.com/digininja/DVWA.git /var/www/html/dvwa
sudo chmod -R 755 /var/www/html/dvwa
sudo chown -R www-data:www-data /var/www/html/dvwa

# Configure database connection in /var/www/html/dvwa/config/config.inc.php
```

## Conclusion

Burp Suite is an indispensable tool for web application security testing. This tutorial covered the fundamentals, but there's much more to explore.

### Next Steps

1. Practice with the free **Damn Vulnerable Web Application (DVWA)**
2. Learn **Burp Suite extensions** for specialized testing
3. Explore **API security testing** with REST APIs
4. Study **client-side vulnerabilities** (CSRF, CORS, CSP)
5. Implement Burp Suite in your **CI/CD pipeline**

### Additional Resources

- [PortSwigger Web Security Academy](https://portswigger.net/web-security)
- [Burp Suite Documentation](https://portswigger.net/burp/documentation)
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [Web Application Security Handbook](https://portswigger.net/web-security)

### Key Takeaways

- Burp Suite is essential for web application security testing
- Proper configuration is critical for effective testing
- Combine automated scanning with manual techniques
- Always test ethically with proper authorization
- Documentation and reporting are as important as finding vulnerabilities

### Tags

{{tool "burp suite"}} {{tool "web security"}} {{tool "penetration testing"}} {{tool "vulnerability assessment"}} {{tool "owasp"}}


*Happy learning! Stay curious and keep practicing.*
