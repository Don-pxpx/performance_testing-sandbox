# 🎯 Testing Cheat Sheet
**Quick Reference Guide - ISTQB & OWASP Aligned**

---

## 🤖 **AUTOMATION TESTING** (ISTQB Test Automation Engineer)

### 🏗️ **Test Automation Architecture**

| Layer | 🎯 Purpose | 🛠️ Components |
|-------|-----------|----------------|
| **Test Generation Layer** | Create test cases | Test data, test scripts |
| **Test Definition Layer** | Define test structure | Test frameworks, BDD specs |
| **Test Execution Layer** | Run tests | Test runners, CI/CD |
| **Test Adaptation Layer** | Interface with SUT | Drivers, stubs, mocks |
| **Testability Layer** | Enable automation | Test hooks, APIs |

### 🎨 **Test Automation Frameworks**

| Framework Type | 🎯 Approach | ✅ Pros | 📝 Example |
|----------------|-------------|---------|------------|
| **Linear Scripting** | Record & playback | Quick start | Selenium IDE |
| **Data-Driven** | Separate data from scripts | Reusable, scalable | CSV/JSON test data |
| **Keyword-Driven** | Keywords = actions | Non-technical friendly | Robot Framework |
| **Modular** | Reusable modules | Maintainable | Page Object Model |
| **Hybrid** | Combines approaches | Best of all | POM + Data-Driven |

### 🔧 **Test Automation Design Patterns**

| Pattern | 🎯 Purpose | 📝 Implementation |
|---------|-----------|-------------------|
| **Page Object Model (POM)** | Encapsulate page logic | Separate page classes |
| **Page Factory** | Initialize page objects | @FindBy annotations |
| **Singleton** | Single instance | Driver management |
| **Factory** | Create objects | Test data generation |
| **Builder** | Construct objects | Test scenario building |
| **Strategy** | Algorithm selection | Different test approaches |
| **Observer** | Event handling | Test listeners |

### 📊 **Test Automation Lifecycle**

```
1️⃣ Planning        → Define scope, tools, approach
2️⃣ Design          → Architecture, patterns, framework
3️⃣ Implementation  → Write scripts, create framework
4️⃣ Execution       → Run tests, CI/CD integration
5️⃣ Maintenance     → Update scripts, refactor
6️⃣ Retirement     → Archive obsolete tests
```

### 🛠️ **Test Automation Tools**

| Tool Category | 🎯 Purpose | 🛠️ Examples |
|---------------|-----------|-------------|
| **Test Execution** | Run tests | pytest, JUnit, TestNG |
| **Test Management** | Organize tests | TestRail, Zephyr |
| **CI/CD Integration** | Automate runs | Jenkins, GitHub Actions |
| **Reporting** | Test results | Allure, pytest-html |
| **Code Coverage** | Measure coverage | pytest-cov, JaCoCo |
| **Mocking/Stubbing** | Isolate components | Mockito, unittest.mock |

### 🔄 **Test Automation Maintenance**

| Activity | 🎯 Purpose | ⚠️ When Needed |
|----------|-----------|----------------|
| **Refactoring** | Improve code quality | Code smells detected |
| **Updating** | Adapt to changes | SUT changes |
| **Debugging** | Fix failures | Tests failing |
| **Optimization** | Improve performance | Slow execution |
| **Version Control** | Track changes | All changes |

### 📈 **Test Automation Metrics**

| Metric | 🎯 What It Shows | ✅ Target |
|--------|-------------------|-----------|
| **Automation Coverage** | % tests automated | > 70% |
| **Test Execution Time** | How fast tests run | < 10 min |
| **Pass Rate** | % tests passing | > 95% |
| **Maintenance Effort** | Time to update tests | < 20% of dev time |
| **ROI** | Return on investment | Positive after 3-6 months |
| **Flakiness Rate** | % unstable tests | < 5% |

### ✅ **Test Automation Best Practices**

```
✅ Start with high-value, stable tests
✅ Use Page Object Model for maintainability
✅ Separate test data from test logic
✅ Implement proper wait strategies
✅ Use meaningful test names
✅ Keep tests independent
✅ Clean up test data
✅ Use version control
✅ Document framework decisions
✅ Regular code reviews
```

### 🚀 **Quick Commands**

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test
pytest tests/saucedemo/test_login.py -v

# Run with HTML report
pytest --html=report.html --self-contained-html

# Run with markers
pytest -m smoke

# Run in parallel
pytest -n auto

# Debug test
pytest --pdb tests/saucedemo/test_login.py
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

### 📘 **Test Automation Engineer Concepts**

```
Test Automation Architecture:
🔹 Test Generation → Test Definition → Test Execution → Test Adaptation → Testability

Framework Types:
🔹 Linear → Data-Driven → Keyword-Driven → Modular → Hybrid

Design Patterns:
🔹 Page Object Model → Factory → Builder → Strategy → Observer

Test Automation Lifecycle:
1️⃣ Planning → 2️⃣ Design → 3️⃣ Implementation → 4️⃣ Execution → 5️⃣ Maintenance → 6️⃣ Retirement
```

### ✅ **ISTQB TAE Principles**

```
✅ Not all tests should be automated
✅ Test automation requires maintenance
✅ Test automation is software development
✅ Test automation should be treated as a project
✅ Test automation requires skills and resources
✅ Test automation should be integrated early
✅ Test automation ROI improves over time
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

