# Performance Testing Sandbox

**Personal experimentation sandbox** for exploring performance testing techniques, load testing, stress testing, and performance monitoring using **k6**, **JMeter**, and **Locust**.

This repository is dedicated to performance testing experiments, allowing me to focus on load testing, stress testing, spike testing, and performance analysis without mixing concerns with penetration testing or functional testing.

## 🚀 Quick Start

### Prerequisites

1. **Docker Desktop** (Windows) - [Download here](https://www.docker.com/products/docker-desktop/)
2. **Python 3.10+** with dependencies installed:
   ```bash
   pip install -r requirements.txt
   ```

### Setup

1. **Pull Docker images** (first time only):
   ```bash
   docker pull grafana/k6:latest
   docker pull justb4/jmeter:latest
   ```

2. **Verify setup**:
   ```bash
   python verify_setup.py
   ```

3. **Run Cross-Repository Performance Tests** (NEW!):
   ```bash
   # Discovers and tests targets from automation-testing-playground and pentesting-playground
   python cross_repo_performance_tester.py
   ```

4. **Run Hybrid Attack + Load Tests** (NEW!):
   ```bash
   # ⚠️  WARNING: Only use on systems you own or have explicit permission!
   # Combines vulnerability attacks with load/flood testing
   python hybrid_attack_load_tester.py
   ```

5. **Run individual tests**:
   ```bash
   # List all available tests
   python run_performance_tests.py list

   # Run k6 basic test
   python run_performance_tests.py k6 basic http://localhost:3000

   # Run JMeter test
   python run_performance_tests.py jmeter api http://localhost:3000

   # Run Locust test
   python run_performance_tests.py locust http://localhost:3000 --users 50
   ```

## 📁 Structure

```
performance_testing-sandbox/
├── k6/                    # k6 test scripts
│   ├── basic_api_test.js  # Basic load test
│   ├── stress_test.js     # High load stress test
│   └── spike_test.js      # Sudden traffic spike test
├── jmeter/                # JMeter test plans
│   └── api_test.jmx       # API performance test plan
├── locust/                # Locust test scripts
│   └── locustfile.py      # Locust load test scenarios
├── results/               # Test results (auto-generated)
├── docker-compose.yml      # Docker Compose configuration
├── cross_repo_performance_tester.py  # 🆕 Cross-repo discovery & testing
├── hybrid_attack_load_tester.py  # 🆕 Hybrid attack + load testing
├── run_performance_tests.py  # Unified test runner
├── verify_setup.py        # Setup verification script
└── README.md              # This file
```

## 🎯 Available Tools

- **Cross-Repository Tester** 🆕 - Discovers and tests targets from automation-testing-playground and pentesting-playground
- **Hybrid Attack + Load Tester** 🆕 - Combines vulnerability exploitation with load/flood testing to identify if systems become more vulnerable under stress
- **k6** - Modern, developer-centric performance testing (via Docker)
- **JMeter** - Traditional, feature-rich performance testing (via Docker)
- **Locust** - Python-based load testing (native installation)

## 🔗 Cross-Repository Performance Testing

The `cross_repo_performance_tester.py` script automatically:

1. **🔍 Discovers Targets** from:
   - `automation-testing-playground`: JSONPlaceholder API, ReqRes API, HTTPBin, SauceDemo, BlazeDemo
   - `pentesting-playground`: Juice Shop, DVWA, Booking API, Banking API, Corporate Financial API, VulnAPI

2. **✅ Checks Availability** - Verifies which targets are online and measures initial response times

3. **📊 Runs Performance Tests**:
   - **Basic Load Test**: Python requests with concurrent users
   - **Locust Test**: Realistic user simulation with wait times
   - **k6 Test**: Docker-based load testing with stages

4. **📈 Generates Reports**:
   - Emoji-rich HTML reports with step-by-step explanations
   - Shows what success/failure looks like for each test
   - Detailed metrics and visualizations

### What Each Test Shows

**✅ Success Looks Like:**
- Basic Load Test: ≥80% success rate, avg response time < 1000ms
- Locust Test: Test completes, HTML report generated with metrics
- k6 Test: All stages complete, thresholds met (p95 < 2000ms, error rate < 10%)

**❌ Failure Looks Like:**
- Basic Load Test: <50% success rate or avg response time > 2000ms
- Locust Test: Connection errors, crashes, or execution failures
- k6 Test: Docker unavailable, k6 crashes, or thresholds exceeded

### Example Output

```
🚀 Cross-Repository Performance Testing Discovery

🔍 Discovering Automation Testing Targets...
✅ Discovered 5 automation targets

🔍 Discovering Penetration Testing Targets...
✅ Discovered 6 pentesting targets

🔍 Checking Target Availability...

📊 Step: Load Test - JSONPlaceholder API - /posts
Action: Running basic load test
📖 Explanation: This test sends multiple concurrent HTTP requests...
✅ Success Looks Like: At least 80% of requests should succeed...
❌ Failure Looks Like: If more than 20% requests fail...
   → Sending 20 requests with 5 concurrent users
✅ PASSED
   → Success Rate: 20/20 (100.0%)
   → Avg Response Time: 245.32ms
   ✓ Criteria met: 100.0% success rate and 245.32ms avg response time
```

## ⚔️  Hybrid Attack + Load Testing

⚠️ **WARNING: Only use on systems you own or have explicit written permission to test!**

The `hybrid_attack_load_tester.py` combines vulnerability exploitation attacks (SQL Injection, XSS) with performance/flood testing to identify if systems become more vulnerable under load.

### Why This Matters

When systems are under heavy load, they may:
- Fail rate limiting, allowing more attack attempts
- Expose error messages that reveal sensitive information
- Experience resource exhaustion, making vulnerabilities easier to exploit
- Fail to validate inputs properly due to performance optimizations
- Timeout or race conditions that bypass security checks

### How It Works

1. **📋 Baseline Attack** - Runs vulnerability tests without load to establish baseline
2. **🌊 Load/Flood Test** - Floods the system with concurrent requests (50+ users)
3. **⚔️  Attacks Under Load** - Runs vulnerability attacks while load is active
4. **📊 Comparison Analysis** - Compares success rates and identifies if load made attacks easier

### Test Flow

```
Step 1: Baseline Attack (No Load)
  → Tests SQL Injection and XSS without load
  → Establishes if vulnerabilities exist normally

Step 2: Load/Flood Test
  → Floods endpoint with 50+ concurrent users
  → Measures response times, error rates, throughput

Step 3: Attacks Under Load
  → Runs vulnerability attacks while load is active
  → Tracks success rate and response times

Step 4: Comparison Analysis
  → Compares baseline vs attacks under load
  → Identifies if load made attacks MORE successful
```

### What It Detects

- **Rate Limiting Failures**: System allows more attack attempts under load
- **Error Handling Breakdown**: System exposes sensitive errors when stressed
- **Resource Exhaustion**: Attacks succeed more easily when system is overloaded
- **Security Bypass**: Performance optimizations bypass security checks

### Example Output

```
🎯 Hybrid Attack + Load Test
Target: http://localhost:3000/rest/products/search?q=
Load: 50 concurrent users for 30s
Attacks: SQLI, XSS

Step 1: Baseline Attack (No Load)
✅ Baseline attack successful: SQL Injection
   Response time: 45.23ms
   Evidence: SQL error pattern detected: mysql

Step 2: Load/Flood Test
✅ Load test completed
   Total requests: 1,245
   Success rate: 87.3%
   Avg response time: 2,341.52ms
   Throughput: 41.50 req/s
   Errors: 159
⚠️  System appears stressed under load!

Step 3: Attacks Under Load
✅ Completed 20 attack attempts
   Successful exploits: 15

🚨 VULNERABILITIES FOUND UNDER LOAD!
   • SQL Injection via /rest/products/search?q=
     Payload: ' OR '1'='1 --
     Response time: 1,234.56ms

Step 4: Comparison Analysis
🚨 CRITICAL: Attacks were MORE successful under load!
   Baseline success rate: 100.0%
   Under-load success rate: 75.0%
```

### Configuration

Edit the `test_targets` list in `hybrid_attack_load_tester.py` to specify your authorized test targets:

```python
test_targets = [
    {
        "url": "http://localhost:3000",
        "endpoints": ["/rest/products/search?q=", "/api/users/"],
        "parameter": "q"
    }
]
```

## 📊 Test Types

### k6 Tests

- **Basic API Test** (`basic_api_test.js`)
  - Ramp up: 10 → 20 users
  - Duration: ~3 minutes
  - Tests: Homepage + API endpoints

- **Stress Test** (`stress_test.js`)
  - High load: 50 → 100 users
  - Duration: ~9 minutes
  - Tests system under heavy load

- **Spike Test** (`spike_test.js`)
  - Sudden spike: 10 → 100 → 10 users
  - Duration: ~1 minute
  - Tests system resilience to sudden traffic bursts

### JMeter Tests

- **API Test** (`api_test.jmx`)
  - 10 concurrent users
  - Tests homepage and API endpoints
  - Generates HTML report

### Locust Tests

- **Web App Load Test** (`locustfile.py`)
  - Multiple user scenarios:
    - `WebAppUser` - Realistic browsing behavior
    - `APIUser` - API client simulation
    - `SpikeUser` - Rapid fire requests

## 📈 Progress & Milestones

### ✅ Completed
- Docker Compose configuration for k6 and JMeter
- k6 test scripts (basic, stress, spike)
- JMeter test plan (API test)
- Locust test scenarios
- Unified test runner script
- Windows-compatible Docker commands
- Setup verification script
- **Cross-repository performance testing** 🆕
  - Automatic discovery from automation-testing-playground and pentesting-playground
  - Step-by-step explanations with success/failure criteria
  - Emoji-rich HTML reports with detailed metrics
  - Integration with k6, Locust, and basic load testing
- **Hybrid Attack + Load Testing** 🆕
  - Combines vulnerability exploitation with load/flood testing
  - Identifies if systems become more vulnerable under stress
  - Baseline vs under-load comparison analysis
  - Detailed HTML reports showing attack success rates

### 🚧 In Progress
- Advanced k6 scenarios (API authentication, custom metrics)
- JMeter GUI mode support
- Performance baseline comparisons

### 📋 Planned
- CI/CD integration for performance tests
- Automated performance regression detection
- Grafana dashboards for performance metrics
- Custom performance test scenarios for different target applications
- Performance monitoring and alerting
- Baseline performance tracking

## 📚 Resources

- [k6 Documentation](https://k6.io/docs/)
- [JMeter Documentation](https://jmeter.apache.org/usermanual/)
- [Locust Documentation](https://docs.locust.io/)

## 🔧 Troubleshooting

### Docker Issues (Windows)

1. **"host.docker.internal" not resolving**:
   - Use `localhost` instead of `host.docker.internal`
   - Or use container IP address

2. **Volume mounting issues**:
   - Use absolute paths: `C:\Users\...\performance_testing-sandbox\k6:/scripts`
   - Ensure Docker Desktop is running

3. **Permission errors**:
   - Run Docker Desktop as Administrator
   - Check file permissions on shared volumes

### Locust Issues

1. **"Module not found"**:
   ```bash
   pip install locust
   ```

2. **Port already in use**:
   - Change port: `--web-port 8081`
   - Or stop other services using the port

