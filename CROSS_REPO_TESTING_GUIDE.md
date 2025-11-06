# 🔗 Cross-Repository Performance Testing Guide

## Overview

The `cross_repo_performance_tester.py` script automatically discovers and tests performance of applications and APIs from both `automation-testing-playground` and `pentesting-playground` repositories.

## How It Works

### Step 1: Discovery Phase 🔍

The script scans both repositories and identifies testable targets:

**From `automation-testing-playground`:**
- JSONPlaceholder API (public REST API)
- ReqRes API (public test API)
- HTTPBin API (HTTP testing service)
- SauceDemo (e-commerce demo)
- BlazeDemo (travel booking demo)

**From `pentesting-playground`:**
- OWASP Juice Shop (port 3000)
- DVWA (port 8080)
- Booking API (port 5000)
- Banking API (port 5001)
- Corporate Financial API (port 7000)
- VulnAPI (port 5002)

### Step 2: Availability Check ✅

For each discovered target:
- **Action**: Sends a HEAD/GET request to check if the service is online
- **Success Looks Like**: HTTP status code < 500, response received
- **Failure Looks Like**: Connection timeout, connection refused, or 5xx errors
- **Output**: Shows status (✅ online / ❌ offline) and initial response time

### Step 3: Performance Testing 📊

For each **online** target, the script runs three types of tests:

#### Test 1: Basic Load Test (Python requests)

**What It Does:**
- Sends 20 concurrent HTTP requests using Python's `ThreadPoolExecutor`
- Measures response times and success rates
- Calculates throughput (requests per second)

**Explanation:**
"This test sends multiple concurrent HTTP requests to measure response times and success rates. It simulates multiple users hitting the endpoint simultaneously."

**✅ Success Looks Like:**
- At least 80% of requests succeed
- Average response time < 1000ms
- Throughput > 5 req/s

**❌ Failure Looks Like:**
- Less than 50% of requests succeed
- Average response time > 2000ms
- Connection errors or timeouts

**⚠️ Warning Looks Like:**
- 50-80% success rate
- Average response time 1000-2000ms
- Acceptable but not optimal performance

#### Test 2: Locust Test

**What It Does:**
- Creates a temporary Locust test file
- Runs Locust with 10 users, spawning at 2 users/second
- Runs for 30 seconds
- Generates HTML report with detailed metrics

**Explanation:**
"Locust simulates real user behavior with realistic wait times between requests. It's more realistic than basic load testing because it includes user think time."

**✅ Success Looks Like:**
- Locust completes all 30 seconds
- HTML report generated successfully
- No connection errors in output
- Report shows reasonable response times

**❌ Failure Looks Like:**
- Locust crashes or exits early
- Connection errors during execution
- No HTML report generated
- Error messages in stderr

**Skipped If:**
- Locust not installed (`pip install locust`)

#### Test 3: k6 Test (via Docker)

**What It Does:**
- Creates a k6 JavaScript test script
- Runs k6 in Docker container with stages:
  - Ramp up: 0 → 5 users over 10 seconds
  - Sustain: 5 users for 20 seconds
  - Ramp down: 5 → 0 users over 10 seconds
- Checks thresholds: p95 < 2000ms, error rate < 10%

**Explanation:**
"k6 runs in Docker container and performs load testing with configurable stages (ramp-up, sustain, ramp-down). It provides detailed metrics and can handle high loads."

**✅ Success Looks Like:**
- All k6 stages complete successfully
- p95 response time < 2000ms
- Error rate < 10%
- No threshold violations

**❌ Failure Looks Like:**
- Docker unavailable
- k6 crashes during execution
- Thresholds exceeded (p95 > 2000ms or error rate > 10%)
- Container errors

**Skipped If:**
- Docker Desktop not running
- Docker not installed

### Step 4: Report Generation 📈

**What It Generates:**
- **HTML Report**: Emoji-rich, detailed report with:
  - Discovery summary table
  - Step-by-step test execution with explanations
  - Success/failure criteria for each test
  - Detailed metrics and results
  - Visual status indicators (✅ ❌ ⚠️)

**Report Location:**
`results/cross_repo_performance_report_YYYYMMDD_HHMMSS.html`

## Example Output

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
   → Min/Max: 180.45ms / 320.10ms
   → Throughput: 18.25 req/s
   ✓ Criteria met: 100.0% success rate and 245.32ms avg response time
```

## Usage

```bash
# Run cross-repository performance tests
python cross_repo_performance_tester.py
```

The script will:
1. Automatically discover targets from both repos
2. Check which ones are online
3. Run performance tests on online targets
4. Generate detailed HTML report

## Understanding Results

### Status Indicators

- **✅ PASSED**: Test met all success criteria
- **⚠️  WARNING**: Test met some criteria but performance is borderline
- **❌ FAILED**: Test failed or criteria not met
- **⚠️  SKIPPED**: Test skipped (dependency unavailable)

### Key Metrics

- **Success Rate**: Percentage of successful requests
- **Response Time**: How long requests take (avg/min/max)
- **Throughput**: Requests per second the system can handle
- **P95**: 95th percentile response time (95% of requests faster than this)

## Troubleshooting

### Target Shows as Offline
- **Check**: Is the application running?
- **For Pentesting Targets**: Start Docker containers first
- **For Public APIs**: Check internet connection

### Locust Tests Fail
- **Install Locust**: `pip install locust`
- **Check**: Python version (3.10+)

### k6 Tests Skipped
- **Install Docker Desktop**: https://www.docker.com/products/docker-desktop/
- **Check**: Docker is running
- **Verify**: Docker images pulled (`docker pull grafana/k6:latest`)

## Next Steps

1. **Review HTML Report**: Open the generated report in your browser
2. **Analyze Metrics**: Look for response times, throughput, and error rates
3. **Compare Targets**: See which targets perform best/worst
4. **Identify Issues**: Slow response times or high error rates indicate problems
5. **Re-run Tests**: Run tests multiple times to establish baselines




