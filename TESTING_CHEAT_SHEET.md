# 🎯 Testing Cheat Sheet
**Quick Reference Guide - ISTQB & OWASP Aligned**

---

## 🤖 **AUTOMATION TESTING** (ISTQB Foundation)

### 📊 **Test Design Techniques**

| Technique | 🎯 What It Is | 📝 Example | ✅ When to Use |
|-----------|---------------|------------|----------------|
| **Equivalence Partitioning** | Group similar inputs | Age: 0-17, 18-65, 66+ | One test per group |
| **Boundary Value Analysis** | Test edge values | Min: 0, Max: 100, Min-1: -1, Max+1: 101 | Form limits, ranges |
| **Decision Table** | All input combos | Login: Valid/Invalid user × Valid/Invalid pass | Complex logic |
| **State Transition** | Test state changes | Login → Logout → Login | Workflows |
| **Use Case Testing** | User scenarios | "As user, I want to checkout" | End-to-end flows |

### 📈 **Test Levels**

```
🔹 Unit Testing        → Test individual functions
🔹 Integration Testing → Test components together
🔹 System Testing      → Test entire system
🔹 Acceptance Testing   → Test user requirements
```

### 🎨 **Test Types**

| Type | 🎯 Purpose | 🛠️ Tools |
|------|-----------|----------|
| **Functional** | Does it work? | Playwright, Selenium |
| **Non-Functional** | How well does it work? | Performance, Security tools |
| **Structural** | Code coverage | pytest-cov, coverage.py |
| **Change-Related** | Regression | Test suites |

### ✅ **Quick Commands**

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Run specific test
pytest tests/saucedemo/test_login.py

# Run with HTML report
pytest --html=report.html --self-contained-html
```

---

## ⚡ **PERFORMANCE TESTING** (ISTQB Performance)

### 📊 **Test Types**

| Type | 🎯 Purpose | 📈 Load | ⏱️ Duration | 🎯 Goal |
|------|-----------|--------|-------------|---------|
| **Load Testing** | Normal load | Expected users | 30-60 min | Verify performance |
| **Stress Testing** | Beyond capacity | Max + 20% | Until failure | Find breaking point |
| **Spike Testing** | Sudden traffic | 0 → Max → 0 | 5-10 min | Handle spikes |
| **Volume Testing** | Large data | Normal load | 1+ hour | Data handling |
| **Endurance Testing** | Long duration | Normal load | 4+ hours | Memory leaks |

### 📈 **Key Metrics**

| Metric | 🎯 What It Means | ✅ Good | ❌ Bad |
|--------|-------------------|---------|--------|
| **Response Time** | Time to respond | < 2s | > 5s |
| **Throughput** | Requests/second | High | Low |
| **Error Rate** | Failed requests | < 1% | > 5% |
| **CPU Usage** | Processor load | < 70% | > 90% |
| **Memory Usage** | RAM consumption | Stable | Growing |
| **P95/P99** | 95th/99th percentile | < 3s | > 10s |

### 🛠️ **Tools Quick Reference**

| Tool | 🎯 Best For | 📝 Command |
|------|-------------|------------|
| **k6** | Modern, scriptable | `k6 run script.js` |
| **Locust** | Python-based | `locust -f locustfile.py` |
| **JMeter** | GUI + scripting | `jmeter -n -t test.jmx` |
| **Gatling** | Scala, reports | `gatling.sh` |

### ✅ **Performance Checklist**

```
✅ Define performance goals (SLA)
✅ Create realistic test data
✅ Monitor resources (CPU, Memory, Network)
✅ Run baseline test first
✅ Compare before/after changes
✅ Document bottlenecks
✅ Retest after fixes
```

---

## 🔐 **PENETRATION TESTING** (OWASP Top 10)

### 🎯 **OWASP Top 10:2021**

| # | Vulnerability | 🔴 Risk | 🛠️ Test For | ✅ Status |
|---|---------------|---------|-------------|-----------|
| **A01** | Broken Access Control | 🔴🔴🔴 High | IDOR, privilege escalation | ✅ Covered |
| **A02** | Cryptographic Failures | 🔴🔴🔴 High | Plaintext passwords, weak encryption | ⚪ Next |
| **A03** | Injection | 🔴🔴🔴 High | SQLi, NoSQLi, Command Injection | ✅ Covered |
| **A04** | Insecure Design | 🔴🔴 Medium | Business logic flaws | ⚪ Next |
| **A05** | Security Misconfiguration | 🔴🔴 Medium | Default configs, exposed files | ⚪ Next |
| **A06** | Vulnerable Components | 🔴🔴 Medium | Outdated libraries, CVEs | ⚪ Next |
| **A07** | Auth Failures | 🔴🔴🔴 High | Weak passwords, session issues | ✅ Covered |
| **A08** | Data Integrity Failures | 🔴🔴 Medium | Unsigned updates, CI/CD attacks | ⚪ Next |
| **A09** | Logging Failures | 🔴 Low | Missing logs, log injection | ⚪ Next |
| **A10** | SSRF | 🔴🔴 Medium | Internal network access | ⚪ Next |

### 🔍 **Common Attack Vectors**

| Attack | 🎯 Target | 💥 Impact | 🛠️ Tool |
|--------|-----------|-----------|---------|
| **SQL Injection** | Database | Data breach, auth bypass | sqlmap, manual |
| **XSS** | Users | Cookie theft, defacement | Burp Suite, manual |
| **IDOR** | API endpoints | Unauthorized access | Manual testing |
| **CSRF** | State-changing ops | Unauthorized actions | Burp Suite |
| **SSRF** | Internal services | Internal network access | Manual testing |
| **XXE** | XML parsers | File read, SSRF | Manual testing |

### 🎯 **Testing Methodology**

```
1️⃣ Reconnaissance    → 🔍 Info gathering
2️⃣ Scanning          → 🎯 Find vulnerabilities  
3️⃣ Exploitation      → 💥 Prove impact
4️⃣ Post-Exploitation → 📊 Maintain access
5️⃣ Reporting        → 📝 Document findings
```

### ✅ **Quick Commands**

```bash
# SQL Injection test
python tools/attacks/attack_sqli_basic.py

# XSS test
python tools/attacks/attack_xss_basic.py

# API endpoint discovery
python tools/discovery/discovery_api_endpoints.py

# OWASP Top 10 comprehensive test
python tools/testing/test_dvwa_owasp_top10.py
```

---

## 🔗 **CROSS-REPO INTEGRATION**

### 🤖⚡ **Automation + Performance**

```
✅ Add performance assertions to UI tests
✅ Fail test if page load > 3s
✅ Monitor API response times in automation
✅ Track performance trends over time
```

### 🤖🔐 **Automation + Security**

```
✅ Test for XSS in form submissions
✅ Check for exposed secrets in responses
✅ Validate authentication flows
✅ Test authorization boundaries
```

### ⚡🔐 **Performance + Security**

```
✅ Run attacks under load (hybrid testing)
✅ Test if system fails faster under stress + attack
✅ Monitor resource usage during attacks
✅ Find performance bottlenecks during exploitation
```

### 🎯 **Full Stack Testing**

```
1️⃣ Functional (Automation) → Does it work?
2️⃣ Performance → Does it work fast enough?
3️⃣ Security → Can it be broken?
```

---

## 📊 **TEST METRICS & KPIs**

### 🤖 **Automation Metrics**

| Metric | 🎯 What It Shows | ✅ Target |
|--------|-------------------|-----------|
| **Test Coverage** | % code tested | > 80% |
| **Pass Rate** | % tests passing | > 95% |
| **Execution Time** | How long tests take | < 10 min |
| **Flakiness Rate** | % flaky tests | < 5% |

### ⚡ **Performance Metrics**

| Metric | 🎯 What It Shows | ✅ Target |
|--------|-------------------|-----------|
| **Response Time** | Speed | P95 < 2s |
| **Throughput** | Capacity | High req/s |
| **Error Rate** | Reliability | < 1% |
| **Resource Usage** | Efficiency | CPU < 70% |

### 🔐 **Security Metrics**

| Metric | 🎯 What It Shows | ✅ Target |
|--------|-------------------|-----------|
| **Vulnerabilities Found** | Security issues | Track & fix |
| **Time to Fix** | Remediation speed | < 7 days |
| **Risk Score** | Overall security | Low/Medium |
| **Coverage** | OWASP Top 10 coverage | 100% |

---

## 🎓 **ISTQB QUICK REFERENCE**

### 📘 **Foundation Level Concepts**

```
Test Levels:
🔹 Unit → Integration → System → Acceptance

Test Types:
🔹 Functional → Non-Functional → Structural → Change-Related

Test Design:
🔹 Equivalence Partitioning
🔹 Boundary Value Analysis
🔹 Decision Tables
🔹 State Transition
🔹 Use Case Testing

Test Process:
1️⃣ Planning → 2️⃣ Design → 3️⃣ Implementation → 4️⃣ Execution → 5️⃣ Reporting
```

### ✅ **ISTQB Principles**

```
✅ Testing shows presence of defects
✅ Exhaustive testing is impossible
✅ Early testing saves time & money
✅ Defects cluster together
✅ Tests wear out (need updates)
✅ Testing is context dependent
✅ Absence-of-errors fallacy
```

---

## 🎯 **OWASP QUICK REFERENCE**

### 🔐 **Top 10:2021 Summary**

```
A01 🔴 Broken Access Control
A02 🔴 Cryptographic Failures  
A03 🔴 Injection
A04 🟡 Insecure Design
A05 🟡 Security Misconfiguration
A06 🟡 Vulnerable Components
A07 🔴 Identification & Authentication Failures
A08 🟡 Software/Data Integrity Failures
A09 🟢 Security Logging Failures
A10 🟡 SSRF
```

### 🛠️ **OWASP Testing Tools**

| Tool | 🎯 Purpose |
|------|------------|
| **OWASP ZAP** | Web app security scanner |
| **Burp Suite** | Web security testing |
| **sqlmap** | SQL injection tool |
| **Nikto** | Web server scanner |
| **Nmap** | Network discovery |

---

## 🚀 **QUICK START COMMANDS**

### 🤖 **Automation**

```bash
# Install dependencies
pip install -r requirements.txt
playwright install chromium

# Run tests
pytest
pytest --html=report.html
pytest --cov=.
```

### ⚡ **Performance**

```bash
# Cross-repo performance test
python cross_repo_performance_tester.py

# k6 test
k6 run k6/basic_api_test.js

# Locust test
locust -f locust/locustfile.py --users 50
```

### 🔐 **Security**

```bash
# Start vulnerable apps
docker-compose up -d

# Run OWASP Top 10 tests
python tools/testing/test_dvwa_owasp_top10.py

# Specific attacks
python tools/attacks/attack_sqli_basic.py
python tools/attacks/attack_xss_basic.py
```

---

## 📝 **TESTING CHECKLISTS**

### ✅ **Before Testing**

```
✅ Understand requirements
✅ Set up test environment
✅ Prepare test data
✅ Define test objectives
✅ Set up monitoring
✅ Backup data
```

### ✅ **During Testing**

```
✅ Execute test cases
✅ Monitor system resources
✅ Log all findings
✅ Capture screenshots/evidence
✅ Document anomalies
✅ Track metrics
```

### ✅ **After Testing**

```
✅ Analyze results
✅ Identify root causes
✅ Create test reports
✅ Share findings
✅ Retest fixes
✅ Update test suites
```

---

## 🎯 **COMMON PATTERNS**

### 🔄 **Test Pattern: AAA**

```
Arrange → Set up test data
Act     → Execute action
Assert  → Verify result
```

### 📊 **Report Pattern**

```
📋 Summary → What was tested
📈 Results → Pass/Fail counts
🔍 Findings → Issues found
💡 Recommendations → What to fix
```

### 🎯 **Bug Report Pattern**

```
📝 Title → Clear description
🔍 Steps → How to reproduce
✅ Expected → What should happen
❌ Actual → What actually happened
📎 Evidence → Screenshots/logs
```

---

## 🏆 **SUCCESS CRITERIA**

### 🤖 **Automation Success**

```
✅ > 80% test coverage
✅ > 95% pass rate
✅ < 5% flakiness
✅ Fast execution (< 10 min)
✅ Clear reports
```

### ⚡ **Performance Success**

```
✅ P95 response time < 2s
✅ Error rate < 1%
✅ Handles expected load
✅ No memory leaks
✅ Scalable architecture
```

### 🔐 **Security Success**

```
✅ OWASP Top 10 covered
✅ Vulnerabilities documented
✅ Risk assessment complete
✅ Remediation plan in place
✅ Regular security scans
```

---

**📚 Keep this cheat sheet handy! Update as you learn more.** 🚀

