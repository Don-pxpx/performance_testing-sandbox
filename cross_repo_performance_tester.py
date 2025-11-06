#!/usr/bin/env python3
"""
Cross-Repository Performance Testing Discovery & Execution
Discovers testable targets from automation-testing-playground and pentesting-playground,
then runs performance tests with detailed, emoji-rich reporting.
"""

import subprocess
import sys
import os
import io
import requests
import time
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.live import Live
from rich.layout import Layout
from rich.text import Text
from datetime import datetime

# Fix Windows encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

console = Console()

# Repository paths (relative to current directory)
SCRIPT_DIR = Path(__file__).parent.absolute()
WORKSPACE_ROOT = SCRIPT_DIR.parent
AUTOMATION_REPO = WORKSPACE_ROOT / "automation-testing-playground"
PENTESTING_REPO = WORKSPACE_ROOT / "pentesting-playground"
RESULTS_DIR = SCRIPT_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)


@dataclass
class TestTarget:
    """Represents a testable target"""
    name: str
    url: str
    type: str  # 'api', 'web_app', 'endpoint'
    repo: str  # 'automation' or 'pentesting'
    description: str
    endpoints: List[str]
    status: str = "unknown"  # 'online', 'offline', 'unknown'
    response_time: Optional[float] = None


class TargetDiscovery:
    """Discovers testable targets from both repositories"""
    
    def __init__(self):
        self.targets: List[TestTarget] = []
        self.discovered_count = 0
        
    def discover_automation_targets(self) -> List[TestTarget]:
        """Discover targets from automation-testing-playground"""
        console.print("[cyan]🔍 Discovering Automation Testing Targets...[/cyan]")
        
        targets = []
        
        # JSONPlaceholder API
        targets.append(TestTarget(
            name="JSONPlaceholder API",
            url="https://jsonplaceholder.typicode.com",
            type="api",
            repo="automation",
            description="Public REST API for testing - posts, users, comments",
            endpoints=[
                "/posts",
                "/users",
                "/comments",
                "/albums",
                "/photos"
            ]
        ))
        
        # ReqRes API
        targets.append(TestTarget(
            name="ReqRes API",
            url="https://reqres.in/api",
            type="api",
            repo="automation",
            description="Public API for testing REST endpoints",
            endpoints=[
                "/users",
                "/users/2",
                "/login",
                "/register"
            ]
        ))
        
        # HTTPBin API
        targets.append(TestTarget(
            name="HTTPBin API",
            url="https://httpbin.org",
            type="api",
            repo="automation",
            description="HTTP Request & Response Service",
            endpoints=[
                "/get",
                "/post",
                "/status/200",
                "/delay/1"
            ]
        ))
        
        # SauceDemo (if running locally)
        targets.append(TestTarget(
            name="SauceDemo Web App",
            url="https://www.saucedemo.com",
            type="web_app",
            repo="automation",
            description="E-commerce demo application for testing",
            endpoints=["/"]
        ))
        
        # BlazeDemo (if running locally)
        targets.append(TestTarget(
            name="BlazeDemo",
            url="https://blazedemo.com",
            type="web_app",
            repo="automation",
            description="Travel booking demo application",
            endpoints=["/"]
        ))
        
        console.print(f"[green]✅ Discovered {len(targets)} automation targets[/green]")
        return targets
    
    def discover_pentesting_targets(self) -> List[TestTarget]:
        """Discover targets from pentesting-playground"""
        console.print("[cyan]🔍 Discovering Penetration Testing Targets...[/cyan]")
        
        targets = []
        
        # Juice Shop
        targets.append(TestTarget(
            name="OWASP Juice Shop",
            url="http://localhost:3000",
            type="web_app",
            repo="pentesting",
            description="Modern vulnerable web application",
            endpoints=[
                "/",
                "/api/products",
                "/rest/products/search"
            ]
        ))
        
        # DVWA
        targets.append(TestTarget(
            name="DVWA",
            url="http://localhost:8080",
            type="web_app",
            repo="pentesting",
            description="Damn Vulnerable Web Application",
            endpoints=["/"]
        ))
        
        # Booking API
        targets.append(TestTarget(
            name="Booking API",
            url="http://localhost:5000",
            type="api",
            repo="pentesting",
            description="Vulnerable booking API",
            endpoints=[
                "/api/health",
                "/api/login",
                "/api/bookings",
                "/api/flights"
            ]
        ))
        
        # Banking API
        targets.append(TestTarget(
            name="Banking API",
            url="http://localhost:5001",
            type="api",
            repo="pentesting",
            description="Vulnerable banking API",
            endpoints=[
                "/api/health",
                "/api/login",
                "/api/accounts",
                "/api/transactions"
            ]
        ))
        
        # Corporate Financial API
        targets.append(TestTarget(
            name="Corporate Financial API",
            url="http://localhost:7000",
            type="api",
            repo="pentesting",
            description="JSE-listed company financial API",
            endpoints=[
                "/api/auth/login",
                "/api/financial/statements",
                "/api/financial/documents"
            ]
        ))
        
        # VulnAPI
        targets.append(TestTarget(
            name="VulnAPI",
            url="http://localhost:5002",
            type="api",
            repo="pentesting",
            description="Vulnerable REST API for security testing",
            endpoints=["/"]
        ))
        
        console.print(f"[green]✅ Discovered {len(targets)} pentesting targets[/green]")
        return targets
    
    def check_target_availability(self, target: TestTarget) -> Tuple[bool, Optional[float]]:
        """Check if target is online and measure response time"""
        try:
            start_time = time.time()
            response = requests.get(target.url, timeout=5, allow_redirects=True)
            response_time = (time.time() - start_time) * 1000  # Convert to ms
            
            if response.status_code < 500:
                return True, response_time
            else:
                return False, None
        except Exception:
            return False, None
    
    def discover_all(self) -> List[TestTarget]:
        """Discover all targets from both repositories"""
        console.print(Panel.fit(
            "[bold cyan]🚀 Cross-Repository Performance Testing Discovery[/bold cyan]",
            border_style="cyan"
        ))
        
        all_targets = []
        
        # Discover from automation repo
        automation_targets = self.discover_automation_targets()
        all_targets.extend(automation_targets)
        
        # Discover from pentesting repo
        pentesting_targets = self.discover_pentesting_targets()
        all_targets.extend(pentesting_targets)
        
        # Check availability
        console.print("\n[cyan]🔍 Checking Target Availability...[/cyan]")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Checking targets...", total=len(all_targets))
            
            for target in all_targets:
                progress.update(task, description=f"Checking {target.name}...")
                is_online, response_time = self.check_target_availability(target)
                
                if is_online:
                    target.status = "online"
                    target.response_time = response_time
                else:
                    target.status = "offline"
                
                time.sleep(0.2)  # Small delay to avoid overwhelming servers
                progress.advance(task)
        
        self.targets = all_targets
        self.discovered_count = len(all_targets)
        
        return all_targets


class PerformanceTestRunner:
    """Runs performance tests on discovered targets"""
    
    def __init__(self, discovery: TargetDiscovery):
        self.discovery = discovery
        self.results: List[Dict] = []
        self.steps: List[Dict] = []
        
    def run_basic_load_test(self, target: TestTarget, endpoint: str) -> Dict:
        """Run a basic load test using requests"""
        step_info = {
            "step": f"Load Test - {target.name} - {endpoint}",
            "action": "Running basic load test",
            "tool": "Python requests",
            "status": "running",
            "explanation": "This test sends multiple concurrent HTTP requests to measure response times and success rates.",
            "success_criteria": "At least 80% of requests should succeed with average response time < 1000ms",
            "failure_criteria": "If more than 20% requests fail or average response time exceeds 2000ms, the test fails"
        }
        self.steps.append(step_info)
        
        console.print(f"\n[yellow]📊 Step: {step_info['step']}[/yellow]")
        console.print(f"[dim]Action: {step_info['action']}[/dim]")
        console.print(f"[dim]📖 Explanation: {step_info['explanation']}[/dim]")
        console.print(f"[dim]✅ Success Looks Like: {step_info['success_criteria']}[/dim]")
        console.print(f"[dim]❌ Failure Looks Like: {step_info['failure_criteria']}[/dim]")
        
        try:
            num_requests = 20
            concurrent = 5
            response_times = []
            success_count = 0
            failure_count = 0
            
            console.print(f"[dim]   → Sending {num_requests} requests with {concurrent} concurrent users[/dim]")
            
            from concurrent.futures import ThreadPoolExecutor, as_completed
            
            def make_request():
                try:
                    start = time.time()
                    url = f"{target.url}{endpoint}"
                    response = requests.get(url, timeout=10)
                    elapsed = (time.time() - start) * 1000
                    
                    if response.status_code < 400:
                        return {"success": True, "time": elapsed, "status": response.status_code}
                    else:
                        return {"success": False, "time": elapsed, "status": response.status_code}
                except Exception as e:
                    return {"success": False, "time": 0, "error": str(e)}
            
            with ThreadPoolExecutor(max_workers=concurrent) as executor:
                futures = [executor.submit(make_request) for _ in range(num_requests)]
                
                for future in as_completed(futures):
                    result = future.result()
                    if result["success"]:
                        success_count += 1
                        response_times.append(result["time"])
                    else:
                        failure_count += 1
            
            if response_times:
                avg_time = sum(response_times) / len(response_times)
                min_time = min(response_times)
                max_time = max(response_times)
                throughput = len(response_times) / (max(response_times) / 1000) if response_times else 0
            else:
                avg_time = min_time = max_time = throughput = 0
            
            # Determine pass/fail based on criteria
            success_rate = (success_count / num_requests) * 100
            if success_rate >= 80 and avg_time < 1000:
                step_info["status"] = "passed"
                verdict = "✅ PASSED"
                verdict_color = "green"
            elif success_rate >= 50 and avg_time < 2000:
                step_info["status"] = "warning"
                verdict = "⚠️  WARNING"
                verdict_color = "yellow"
            else:
                step_info["status"] = "failed"
                verdict = "❌ FAILED"
                verdict_color = "red"
            
            step_info["result"] = {
                "success_count": success_count,
                "failure_count": failure_count,
                "success_rate": f"{success_rate:.1f}%",
                "avg_response_time": f"{avg_time:.2f}ms",
                "min_response_time": f"{min_time:.2f}ms",
                "max_response_time": f"{max_time:.2f}ms",
                "throughput": f"{throughput:.2f} req/s",
                "verdict": verdict
            }
            
            console.print(f"[{verdict_color}]{verdict}[/{verdict_color}]")
            console.print(f"[dim]   → Success Rate: {success_count}/{num_requests} ({success_rate:.1f}%)[/dim]")
            console.print(f"[dim]   → Avg Response Time: {avg_time:.2f}ms[/dim]")
            console.print(f"[dim]   → Min/Max: {min_time:.2f}ms / {max_time:.2f}ms[/dim]")
            console.print(f"[dim]   → Throughput: {throughput:.2f} req/s[/dim]")
            
            if step_info["status"] == "passed":
                console.print(f"[green]   ✓ Criteria met: {success_rate:.1f}% success rate and {avg_time:.2f}ms avg response time[/green]")
            elif step_info["status"] == "warning":
                console.print(f"[yellow]   ⚠ Some criteria not met but acceptable performance[/yellow]")
            else:
                console.print(f"[red]   ✗ Criteria not met: Success rate too low or response time too high[/red]")
            
            return step_info["result"]
            
        except Exception as e:
            step_info["status"] = "failed"
            step_info["error"] = str(e)
            console.print(f"[red]❌ FAILED[/red]")
            console.print(f"[dim]   → Error: {str(e)}[/dim]")
            console.print(f"[red]   ✗ Test execution failed due to exception[/red]")
            return {"error": str(e)}
    
    def run_locust_test(self, target: TestTarget, endpoint: str) -> Dict:
        """Run Locust performance test"""
        step_info = {
            "step": f"Locust Test - {target.name} - {endpoint}",
            "action": "Running Locust load test",
            "tool": "Locust",
            "status": "running",
            "explanation": "Locust simulates real user behavior with realistic wait times between requests.",
            "success_criteria": "Test completes successfully with HTML report generated showing response times and success rates",
            "failure_criteria": "Test fails if Locust can't connect, crashes, or generates errors during execution"
        }
        self.steps.append(step_info)
        
        console.print(f"\n[yellow]📊 Step: {step_info['step']}[/yellow]")
        console.print(f"[dim]Action: {step_info['action']}[/dim]")
        console.print(f"[dim]📖 Explanation: {step_info['explanation']}[/dim]")
        console.print(f"[dim]✅ Success Looks Like: {step_info['success_criteria']}[/dim]")
        console.print(f"[dim]❌ Failure Looks Like: {step_info['failure_criteria']}[/dim]")
        
        try:
            # Create temporary locustfile
            locustfile_content = f'''
from locust import HttpUser, task, between

class QuickTestUser(HttpUser):
    wait_time = between(1, 2)
    
    @task
    def test_endpoint(self):
        self.client.get("{endpoint}", name="{endpoint}")
'''
            
            locustfile_path = RESULTS_DIR / f"locustfile_{target.name.replace(' ', '_')}.py"
            locustfile_path.write_text(locustfile_content)
            
            console.print(f"[dim]   → Creating Locust test file[/dim]")
            console.print(f"[dim]   → Target: {target.url}{endpoint}[/dim]")
            console.print(f"[dim]   → Running with 10 users for 30 seconds...[/dim]")
            
            # Run Locust
            cmd = [
                sys.executable, "-m", "locust",
                "-f", str(locustfile_path),
                "--host", target.url,
                "--users", "10",
                "--spawn-rate", "2",
                "--run-time", "30s",
                "--headless",
                "--html", str(RESULTS_DIR / f"locust_report_{target.name.replace(' ', '_')}.html"),
                "--csv", str(RESULTS_DIR / f"locust_results_{target.name.replace(' ', '_')}")
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                step_info["status"] = "passed"
                step_info["result"] = {
                    "locust_output": result.stdout,
                    "report_path": str(RESULTS_DIR / f"locust_report_{target.name.replace(' ', '_')}.html")
                }
                console.print(f"[green]✅ PASSED[/green]")
                console.print(f"[dim]   → Report saved to: {step_info['result']['report_path']}[/dim]")
                console.print(f"[green]   ✓ Locust test completed successfully and generated HTML report[/green]")
            else:
                step_info["status"] = "failed"
                step_info["error"] = result.stderr
                console.print(f"[red]❌ FAILED[/red]")
                console.print(f"[dim]   → Error: {result.stderr[:200]}[/dim]")
                console.print(f"[red]   ✗ Locust test failed - check errors above[/red]")
            
            return step_info.get("result", {})
            
        except Exception as e:
            step_info["status"] = "failed"
            step_info["error"] = str(e)
            console.print(f"[red]❌ FAILED[/red]")
            console.print(f"[dim]   → Error: {str(e)}[/dim]")
            return {"error": str(e)}
    
    def run_k6_test(self, target: TestTarget, endpoint: str) -> Dict:
        """Run k6 performance test via Docker"""
        step_info = {
            "step": f"k6 Test - {target.name} - {endpoint}",
            "action": "Running k6 load test via Docker",
            "tool": "k6",
            "status": "running",
            "explanation": "k6 runs in Docker container and performs load testing with configurable stages (ramp-up, sustain, ramp-down).",
            "success_criteria": "k6 completes all stages successfully and shows metrics within thresholds (p95 < 2000ms, error rate < 10%)",
            "failure_criteria": "Test fails if Docker unavailable, k6 crashes, or thresholds are exceeded"
        }
        self.steps.append(step_info)
        
        console.print(f"\n[yellow]📊 Step: {step_info['step']}[/yellow]")
        console.print(f"[dim]Action: {step_info['action']}[/dim]")
        console.print(f"[dim]📖 Explanation: {step_info['explanation']}[/dim]")
        console.print(f"[dim]✅ Success Looks Like: {step_info['success_criteria']}[/dim]")
        console.print(f"[dim]❌ Failure Looks Like: {step_info['failure_criteria']}[/dim]")
        
        try:
            # Create k6 test script
            k6_script = f'''
import http from 'k6/http';
import {{ check, sleep }} from 'k6';

export const options = {{
  stages: [
    {{ duration: '10s', target: 5 }},
    {{ duration: '20s', target: 5 }},
    {{ duration: '10s', target: 0 }},
  ],
  thresholds: {{
    http_req_duration: ['p(95)<2000'],
    http_req_failed: ['rate<0.1'],
  }},
}};

const BASE_URL = __ENV.BASE_URL || '{target.url}';

export default function () {{
  const response = http.get(`${{BASE_URL}}{endpoint}`);
  check(response, {{
    'status is 200': (r) => r.status === 200,
    'response time < 2000ms': (r) => r.timings.duration < 2000,
  }});
  sleep(1);
}}
'''
            
            k6_file = RESULTS_DIR / f"k6_test_{target.name.replace(' ', '_')}.js"
            k6_file.write_text(k6_script)
            
            console.print(f"[dim]   → Creating k6 test script[/dim]")
            console.print(f"[dim]   → Target: {target.url}{endpoint}[/dim]")
            console.print(f"[dim]   → Running via Docker...[/dim]")
            
            # Run k6 via Docker
            volume_mount = f"{RESULTS_DIR.absolute()}:/scripts"
            cmd = [
                "docker", "run", "--rm", "-i",
                "-v", volume_mount,
                "-e", f"BASE_URL={target.url}",
                "grafana/k6:latest",
                "run", f"/scripts/{k6_file.name}"
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                step_info["status"] = "passed"
                step_info["result"] = {
                    "k6_output": result.stdout,
                    "test_script": str(k6_file)
                }
                console.print(f"[green]✅ PASSED[/green]")
                console.print(f"[dim]   → k6 test completed successfully[/dim]")
                console.print(f"[green]   ✓ All k6 stages completed within thresholds[/green]")
            else:
                step_info["status"] = "failed"
                step_info["error"] = result.stderr
                console.print(f"[red]❌ FAILED[/red]")
                console.print(f"[dim]   → Error: {result.stderr[:200]}[/dim]")
                console.print(f"[red]   ✗ k6 test failed - check Docker or thresholds[/red]")
            
            return step_info.get("result", {})
            
        except FileNotFoundError:
            step_info["status"] = "skipped"
            step_info["reason"] = "Docker not available"
            console.print(f"[yellow]⚠️  SKIPPED[/yellow]")
            console.print(f"[dim]   → Docker not found - skipping k6 test[/dim]")
            console.print(f"[yellow]   ⚠ Docker unavailable - install Docker Desktop to run k6 tests[/yellow]")
            return {"skipped": True, "reason": "Docker not available"}
        except Exception as e:
            step_info["status"] = "failed"
            step_info["error"] = str(e)
            console.print(f"[red]❌ FAILED[/red]")
            console.print(f"[dim]   → Error: {str(e)}[/dim]")
            return {"error": str(e)}
    
    def run_tests_on_target(self, target: TestTarget):
        """Run performance tests on a single target"""
        console.print(f"\n[bold cyan]🎯 Testing Target: {target.name}[/bold cyan]")
        console.print(f"[dim]URL: {target.url}[/dim]")
        console.print(f"[dim]Status: {target.status}[/dim]")
        
        if target.status != "online":
            console.print(f"[yellow]⚠️  Skipping offline target[/yellow]")
            return
        
        # Test main endpoint
        main_endpoint = target.endpoints[0] if target.endpoints else "/"
        
        # Run basic load test
        basic_result = self.run_basic_load_test(target, main_endpoint)
        
        # Try Locust if available
        try:
            import locust
            locust_result = self.run_locust_test(target, main_endpoint)
        except ImportError:
            console.print(f"[yellow]⚠️  Locust not available - skipping[/yellow]")
            locust_result = {"skipped": True}
        
        # Try k6 if Docker available
        k6_result = self.run_k6_test(target, main_endpoint)
        
        self.results.append({
            "target": target.name,
            "url": target.url,
            "endpoint": main_endpoint,
            "basic_test": basic_result,
            "locust_test": locust_result,
            "k6_test": k6_result
        })


class ReportGenerator:
    """Generates detailed, emoji-rich performance test reports"""
    
    def __init__(self, discovery: TargetDiscovery, runner: PerformanceTestRunner):
        self.discovery = discovery
        self.runner = runner
        
    def generate_report(self) -> str:
        """Generate comprehensive HTML report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = RESULTS_DIR / f"cross_repo_performance_report_{timestamp}.html"
        
        html_content = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cross-Repository Performance Test Report</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            margin-top: 30px;
            border-left: 4px solid #3498db;
            padding-left: 10px;
        }}
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .summary-card {{
            background: #ecf0f1;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }}
        .summary-card h3 {{
            margin: 0 0 10px 0;
            color: #2c3e50;
        }}
        .summary-card .number {{
            font-size: 2em;
            font-weight: bold;
            color: #3498db;
        }}
        .target-card {{
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
        }}
        .target-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }}
        .status-badge {{
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 0.9em;
        }}
        .status-online {{
            background: #d4edda;
            color: #155724;
        }}
        .status-offline {{
            background: #f8d7da;
            color: #721c24;
        }}
        .step {{
            background: white;
            border-left: 4px solid #3498db;
            padding: 15px;
            margin: 10px 0;
            border-radius: 4px;
        }}
        .step-header {{
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 10px;
        }}
        .step-result {{
            margin-top: 10px;
            padding: 10px;
            border-radius: 4px;
        }}
        .result-passed {{
            background: #d4edda;
            color: #155724;
        }}
        .result-failed {{
            background: #f8d7da;
            color: #721c24;
        }}
        .result-skipped {{
            background: #fff3cd;
            color: #856404;
        }}
        .result-warning {{
            background: #fff3cd;
            color: #856404;
            border-left: 4px solid #ffc107;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #dee2e6;
        }}
        th {{
            background: #3498db;
            color: white;
        }}
        tr:hover {{
            background: #f8f9fa;
        }}
        .emoji {{
            font-size: 1.2em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Cross-Repository Performance Test Report</h1>
        <p><strong>Generated:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        
        <div class="summary">
            <div class="summary-card">
                <h3>🎯 Total Targets</h3>
                <div class="number">{len(self.discovery.targets)}</div>
            </div>
            <div class="summary-card">
                <h3>✅ Online Targets</h3>
                <div class="number">{len([t for t in self.discovery.targets if t.status == 'online'])}</div>
            </div>
            <div class="summary-card">
                <h3>❌ Offline Targets</h3>
                <div class="number">{len([t for t in self.discovery.targets if t.status == 'offline'])}</div>
            </div>
            <div class="summary-card">
                <h3>📊 Tests Run</h3>
                <div class="number">{len(self.runner.results)}</div>
            </div>
        </div>
        
        <h2>📋 Discovery Summary</h2>
        <table>
            <thead>
                <tr>
                    <th>Name</th>
                    <th>URL</th>
                    <th>Repository</th>
                    <th>Type</th>
                    <th>Status</th>
                    <th>Response Time</th>
                </tr>
            </thead>
            <tbody>
'''
        
        for target in self.discovery.targets:
            status_class = "status-online" if target.status == "online" else "status-offline"
            status_emoji = "✅" if target.status == "online" else "❌"
            response_time_str = f"{target.response_time:.2f}ms" if target.response_time else "N/A"
            
            html_content += f'''
                <tr>
                    <td><strong>{target.name}</strong></td>
                    <td>{target.url}</td>
                    <td>{target.repo}</td>
                    <td>{target.type}</td>
                    <td><span class="status-badge {status_class}">{status_emoji} {target.status.upper()}</span></td>
                    <td>{response_time_str}</td>
                </tr>
'''
        
        html_content += '''
            </tbody>
        </table>
        
        <h2>📊 Test Execution Steps</h2>
'''
        
        for step in self.runner.steps:
            status_class = "result-passed" if step["status"] == "passed" else ("result-failed" if step["status"] == "failed" else ("result-warning" if step["status"] == "warning" else "result-skipped"))
            status_emoji = "✅" if step["status"] == "passed" else ("❌" if step["status"] == "failed" else ("⚠️" if step["status"] == "warning" else "⚠️"))
            
            html_content += f'''
        <div class="step">
            <div class="step-header">{status_emoji} {step["step"]}</div>
            <p><strong>Action:</strong> {step["action"]}</p>
            <p><strong>Tool:</strong> {step["tool"]}</p>
            <p><strong>📖 Explanation:</strong> {step.get("explanation", "N/A")}</p>
            <p><strong>✅ Success Looks Like:</strong> <span style="color: #155724;">{step.get("success_criteria", "N/A")}</span></p>
            <p><strong>❌ Failure Looks Like:</strong> <span style="color: #721c24;">{step.get("failure_criteria", "N/A")}</span></p>
            <div class="step-result {status_class}">
                <strong>Status:</strong> {step["status"].upper()}
'''
            
            if "result" in step:
                html_content += f'<pre>{json.dumps(step["result"], indent=2)}</pre>'
            if "error" in step:
                html_content += f'<p><strong>Error:</strong> {step["error"]}</p>'
            
            html_content += '''
            </div>
        </div>
'''
        
        html_content += '''
        <h2>📈 Detailed Results</h2>
'''
        
        for result in self.runner.results:
            html_content += f'''
        <div class="target-card">
            <div class="target-header">
                <h3>{result["target"]}</h3>
                <span>{result["url"]}{result["endpoint"]}</span>
            </div>
            <h4>Basic Load Test</h4>
            <pre>{json.dumps(result["basic_test"], indent=2)}</pre>
            <h4>Locust Test</h4>
            <pre>{json.dumps(result.get("locust_test", {}), indent=2)}</pre>
            <h4>k6 Test</h4>
            <pre>{json.dumps(result.get("k6_test", {}), indent=2)}</pre>
        </div>
'''
        
        html_content += '''
    </div>
</body>
</html>
'''
        
        report_path.write_text(html_content, encoding='utf-8')
        return str(report_path)


def main():
    """Main execution function"""
    console.print(Panel.fit(
        "[bold cyan]🚀 Cross-Repository Performance Testing[/bold cyan]\n"
        "[dim]Discovers and tests targets from automation-testing-playground and pentesting-playground[/dim]",
        border_style="cyan"
    ))
    
    # Step 1: Discovery
    console.print("\n[bold]Step 1: Discovery Phase[/bold]")
    discovery = TargetDiscovery()
    targets = discovery.discover_all()
    
    # Display discovered targets
    table = Table(title="Discovered Targets")
    table.add_column("Name", style="cyan")
    table.add_column("URL", style="green")
    table.add_column("Repo", style="yellow")
    table.add_column("Status", style="magenta")
    table.add_column("Response Time", style="blue")
    
    for target in targets:
        status_emoji = "✅" if target.status == "online" else "❌"
        response_time_str = f"{target.response_time:.2f}ms" if target.response_time else "N/A"
        table.add_row(
            target.name,
            target.url,
            target.repo,
            f"{status_emoji} {target.status}",
            response_time_str
        )
    
    console.print(table)
    
    # Step 2: Testing
    console.print("\n[bold]Step 2: Performance Testing Phase[/bold]")
    runner = PerformanceTestRunner(discovery)
    
    online_targets = [t for t in targets if t.status == "online"]
    console.print(f"[cyan]Found {len(online_targets)} online targets to test[/cyan]")
    
    for target in online_targets[:5]:  # Limit to 5 for demo
        runner.run_tests_on_target(target)
    
    # Step 3: Reporting
    console.print("\n[bold]Step 3: Report Generation[/bold]")
    report_generator = ReportGenerator(discovery, runner)
    report_path = report_generator.generate_report()
    
    console.print(f"\n[bold green]✅ Performance Testing Complete![/bold green]")
    console.print(f"[cyan]📊 Report saved to: {report_path}[/cyan]")
    
    # Summary
    passed_steps = len([s for s in runner.steps if s["status"] == "passed"])
    failed_steps = len([s for s in runner.steps if s["status"] == "failed"])
    skipped_steps = len([s for s in runner.steps if s["status"] == "skipped"])
    
    console.print(f"\n[bold]Summary:[/bold]")
    console.print(f"  ✅ Passed: {passed_steps}")
    console.print(f"  ❌ Failed: {failed_steps}")
    console.print(f"  ⚠️  Skipped: {skipped_steps}")


if __name__ == "__main__":
    main()

