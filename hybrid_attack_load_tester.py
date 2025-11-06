#!/usr/bin/env python3
"""
Hybrid Attack + Load Testing Tool
Combines vulnerability exploitation with performance/flood testing to identify
if systems become more vulnerable under load.

⚠️  WARNING: Only use on systems you own or have explicit written permission to test!
"""

import sys
import os
import io
import requests
import time
import threading
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from datetime import datetime
import json

# Fix Windows encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

console = Console()

# Repository paths
SCRIPT_DIR = Path(__file__).parent.absolute()
WORKSPACE_ROOT = SCRIPT_DIR.parent
PENTESTING_REPO = WORKSPACE_ROOT / "pentesting-playground"
RESULTS_DIR = SCRIPT_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)

# Import attack modules from pentesting-playground
sys.path.insert(0, str(PENTESTING_REPO / "tools" / "attacks"))
try:
    from attack_sqli_basic import SQLInjectionTester
    from attack_xss_basic import XSSTester
except ImportError:
    console.print("[red]❌ Could not import attack modules. Ensure pentesting-playground is available.[/red]")
    sys.exit(1)


@dataclass
class AttackResult:
    """Result of a vulnerability attack"""
    attack_type: str
    endpoint: str
    parameter: Optional[str]
    payload: str
    success: bool
    response_time: float
    error_message: Optional[str] = None
    evidence: Optional[str] = None
    severity: Optional[str] = None


@dataclass
class LoadTestResult:
    """Result of load/flood testing"""
    total_requests: int
    success_count: int
    failure_count: int
    avg_response_time: float
    min_response_time: float
    max_response_time: float
    throughput: float
    error_count: int = 0


@dataclass
class HybridTestResult:
    """Combined result of attack + load testing"""
    target_url: str
    endpoint: str
    baseline_attack: Optional[AttackResult] = None
    load_test_result: Optional[LoadTestResult] = None
    attacks_under_load: List[AttackResult] = field(default_factory=list)
    comparison: Dict = field(default_factory=dict)
    vulnerabilities_found: List[Dict] = field(default_factory=list)


class HybridAttackLoadTester:
    """Combines vulnerability attacks with load/flood testing"""
    
    def __init__(self, target_url: str, endpoints: List[str], attack_types: List[str] = None):
        self.target_url = target_url.rstrip('/')
        self.endpoints = endpoints
        self.attack_types = attack_types or ['sqli', 'xss']
        self.results: List[HybridTestResult] = []
        self.is_running = False
        self.stop_event = threading.Event()
        
        # Initialize attack testers
        self.sqli_tester = SQLInjectionTester(self.target_url)
        self.xss_tester = XSSTester(self.target_url)
        
    def run_baseline_attack(self, endpoint: str, parameter: str = "id") -> Optional[AttackResult]:
        """Run vulnerability attack without load to establish baseline"""
        console.print(f"[dim]📋 Running baseline attack on {endpoint}...[/dim]")
        
        vulnerabilities = []
        start_time = time.time()
        
        # Test SQL Injection
        if 'sqli' in self.attack_types:
            try:
                sqli_vulns = self.sqli_tester.test_get_parameter(endpoint, parameter)
                vulnerabilities.extend(sqli_vulns)
            except Exception as e:
                pass
        
        # Test XSS
        if 'xss' in self.attack_types:
            try:
                xss_vulns = self.xss_tester.test_reflected_xss(endpoint, parameter)
                vulnerabilities.extend(xss_vulns)
            except Exception as e:
                pass
        
        elapsed = (time.time() - start_time) * 1000
        
        if vulnerabilities:
            vuln = vulnerabilities[0]
            return AttackResult(
                attack_type=vuln['type'],
                endpoint=endpoint,
                parameter=parameter,
                payload=vuln['payload'],
                success=True,
                response_time=elapsed,
                evidence=vuln['evidence'],
                severity=vuln['severity']
            )
        
        return None
    
    def run_load_flood(self, endpoint: str, duration: int = 30, 
                      concurrent_users: int = 50, rate_per_second: int = 10) -> LoadTestResult:
        """Run load/flood test on endpoint"""
        console.print(f"[yellow]🌊 Starting load flood: {concurrent_users} concurrent users for {duration}s[/yellow]")
        
        url = f"{self.target_url}{endpoint}"
        response_times = []
        success_count = 0
        failure_count = 0
        error_count = 0
        start_time = time.time()
        request_count = 0
        
        def make_request():
            nonlocal success_count, failure_count, error_count, request_count
            try:
                req_start = time.time()
                response = requests.get(url, timeout=5)
                elapsed = (time.time() - req_start) * 1000
                
                request_count += 1
                response_times.append(elapsed)
                
                if response.status_code < 400:
                    success_count += 1
                else:
                    failure_count += 1
                    error_count += 1
            except Exception as e:
                failure_count += 1
                error_count += 1
        
        # Create thread pool for concurrent requests
        with ThreadPoolExecutor(max_workers=concurrent_users) as executor:
            futures = []
            
            # Submit requests at specified rate
            while time.time() - start_time < duration and not self.stop_event.is_set():
                # Submit batch of requests
                for _ in range(rate_per_second):
                    if time.time() - start_time < duration:
                        futures.append(executor.submit(make_request))
                
                # Wait 1 second before next batch
                time.sleep(1)
            
            # Wait for all requests to complete
            for future in as_completed(futures):
                try:
                    future.result()
                except:
                    pass
        
        elapsed_total = time.time() - start_time
        
        if response_times:
            avg_time = sum(response_times) / len(response_times)
            min_time = min(response_times)
            max_time = max(response_times)
            throughput = len(response_times) / elapsed_total if elapsed_total > 0 else 0
        else:
            avg_time = min_time = max_time = throughput = 0
        
        return LoadTestResult(
            total_requests=request_count,
            success_count=success_count,
            failure_count=failure_count,
            avg_response_time=avg_time,
            min_response_time=min_time,
            max_response_time=max_time,
            throughput=throughput,
            error_count=error_count
        )
    
    def run_attack_under_load(self, endpoint: str, parameter: str = "id",
                              load_duration: int = 30, concurrent_users: int = 50) -> List[AttackResult]:
        """Run vulnerability attacks while load/flood is happening"""
        console.print(f"[red]⚔️  Running attacks under load...[/red]")
        
        url = f"{self.target_url}{endpoint}"
        attack_results = []
        
        # Start load flood in background
        load_thread = threading.Thread(
            target=self._run_load_in_background,
            args=(endpoint, load_duration, concurrent_users),
            daemon=True
        )
        load_thread.start()
        
        # Give load a moment to start
        time.sleep(2)
        
        # Now run attacks
        start_time = time.time()
        attack_count = 0
        
        # SQL Injection attacks under load
        if 'sqli' in self.attack_types:
            for payload in self.sqli_tester.payloads[:10]:  # Test first 10 payloads
                if time.time() - start_time > load_duration:
                    break
                    
                try:
                    attack_start = time.time()
                    test_url = f"{url}?{parameter}={payload}"
                    response = requests.get(test_url, timeout=5)
                    elapsed = (time.time() - attack_start) * 1000
                    
                    # Check for SQL errors
                    content_lower = response.text.lower()
                    found_vuln = False
                    evidence = None
                    
                    for pattern in self.sqli_tester.error_patterns:
                        if pattern in content_lower:
                            found_vuln = True
                            evidence = f"SQL error pattern: {pattern}"
                            break
                    
                    attack_results.append(AttackResult(
                        attack_type="SQL Injection",
                        endpoint=endpoint,
                        parameter=parameter,
                        payload=payload,
                        success=found_vuln,
                        response_time=elapsed,
                        evidence=evidence,
                        severity="Critical" if found_vuln else None
                    ))
                    
                    attack_count += 1
                    time.sleep(0.5)  # Small delay between attacks
                    
                except Exception as e:
                    attack_results.append(AttackResult(
                        attack_type="SQL Injection",
                        endpoint=endpoint,
                        parameter=parameter,
                        payload=payload,
                        success=False,
                        response_time=0,
                        error_message=str(e)
                    ))
        
        # XSS attacks under load
        if 'xss' in self.attack_types:
            for payload in self.xss_tester.payloads[:10]:  # Test first 10 payloads
                if time.time() - start_time > load_duration:
                    break
                    
                try:
                    attack_start = time.time()
                    test_url = f"{url}?{parameter}={payload}"
                    response = requests.get(test_url, timeout=5)
                    elapsed = (time.time() - attack_start) * 1000
                    
                    # Check if payload reflected
                    found_vuln = False
                    evidence = None
                    
                    if payload in response.text or payload.replace('<', '&lt;') not in response.text:
                        if '<script>' in response.text.lower() or 'onerror=' in response.text.lower():
                            found_vuln = True
                            evidence = "Payload reflected without proper encoding"
                    
                    attack_results.append(AttackResult(
                        attack_type="XSS",
                        endpoint=endpoint,
                        parameter=parameter,
                        payload=payload[:50] + "..." if len(payload) > 50 else payload,
                        success=found_vuln,
                        response_time=elapsed,
                        evidence=evidence,
                        severity="High" if found_vuln else None
                    ))
                    
                    attack_count += 1
                    time.sleep(0.5)  # Small delay between attacks
                    
                except Exception as e:
                    attack_results.append(AttackResult(
                        attack_type="XSS",
                        endpoint=endpoint,
                        parameter=parameter,
                        payload=payload[:50] + "..." if len(payload) > 50 else payload,
                        success=False,
                        response_time=0,
                        error_message=str(e)
                    ))
        
        return attack_results
    
    def _run_load_in_background(self, endpoint: str, duration: int, concurrent_users: int):
        """Run load flood in background thread"""
        url = f"{self.target_url}{endpoint}"
        start_time = time.time()
        
        def make_request():
            try:
                requests.get(url, timeout=5)
            except:
                pass
        
        with ThreadPoolExecutor(max_workers=concurrent_users) as executor:
            futures = []
            while time.time() - start_time < duration and not self.stop_event.is_set():
                futures.append(executor.submit(make_request))
                time.sleep(0.1)  # High rate
            
            for future in as_completed(futures):
                try:
                    future.result()
                except:
                    pass
    
    def run_hybrid_test(self, endpoint: str, parameter: str = "id",
                       load_duration: int = 30, concurrent_users: int = 50) -> HybridTestResult:
        """Run complete hybrid test: baseline attack, load test, attacks under load"""
        
        console.print(Panel.fit(
            f"[bold yellow]🎯 Hybrid Attack + Load Test[/bold yellow]\n"
            f"Target: {self.target_url}{endpoint}\n"
            f"Load: {concurrent_users} concurrent users for {load_duration}s\n"
            f"Attacks: {', '.join(self.attack_types).upper()}"
        ))
        
        result = HybridTestResult(target_url=self.target_url, endpoint=endpoint)
        
        # Step 1: Baseline attack (no load)
        console.print("\n[bold cyan]Step 1: Baseline Attack (No Load)[/bold cyan]")
        baseline = self.run_baseline_attack(endpoint, parameter)
        result.baseline_attack = baseline
        
        if baseline:
            console.print(f"[green]✅ Baseline attack successful: {baseline.attack_type}[/green]")
            console.print(f"   Response time: {baseline.response_time:.2f}ms")
            console.print(f"   Evidence: {baseline.evidence}")
        else:
            console.print("[yellow]⚠️  Baseline attack did not find vulnerabilities[/yellow]")
        
        # Step 2: Load/Flood test
        console.print("\n[bold cyan]Step 2: Load/Flood Test[/bold cyan]")
        load_result = self.run_load_flood(endpoint, load_duration, concurrent_users)
        result.load_test_result = load_result
        
        console.print(f"[green]✅ Load test completed[/green]")
        console.print(f"   Total requests: {load_result.total_requests}")
        console.print(f"   Success rate: {(load_result.success_count/load_result.total_requests*100):.1f}%" if load_result.total_requests > 0 else "   Success rate: 0%")
        console.print(f"   Avg response time: {load_result.avg_response_time:.2f}ms")
        console.print(f"   Throughput: {load_result.throughput:.2f} req/s")
        console.print(f"   Errors: {load_result.error_count}")
        
        # Check if system is stressed
        if load_result.avg_response_time > 2000 or load_result.error_count > load_result.total_requests * 0.2:
            console.print("[red]⚠️  System appears stressed under load![/red]")
        
        # Step 3: Attacks under load
        console.print("\n[bold cyan]Step 3: Attacks Under Load[/bold cyan]")
        console.print("[dim]Running vulnerability attacks while load is active...[/dim]")
        
        attack_results = self.run_attack_under_load(endpoint, parameter, load_duration, concurrent_users)
        result.attacks_under_load = attack_results
        
        successful_attacks = [a for a in attack_results if a.success]
        console.print(f"[green]✅ Completed {len(attack_results)} attack attempts[/green]")
        console.print(f"   Successful exploits: {len(successful_attacks)}")
        
        if successful_attacks:
            console.print(f"[red]🚨 VULNERABILITIES FOUND UNDER LOAD![/red]")
            for attack in successful_attacks:
                console.print(f"   • {attack.attack_type} via {attack.endpoint}")
                console.print(f"     Payload: {attack.payload[:50]}...")
                console.print(f"     Response time: {attack.response_time:.2f}ms")
        
        # Step 4: Compare results
        console.print("\n[bold cyan]Step 4: Comparison Analysis[/bold cyan]")
        comparison = self._compare_results(baseline, attack_results, load_result)
        result.comparison = comparison
        
        if comparison['load_made_attacks_easier']:
            console.print("[red]🚨 CRITICAL: Attacks were MORE successful under load![/red]")
            console.print(f"   Baseline success rate: {comparison['baseline_success_rate']:.1f}%")
            console.print(f"   Under-load success rate: {comparison['under_load_success_rate']:.1f}%")
        else:
            console.print("[yellow]ℹ️  Load did not significantly affect attack success[/yellow]")
        
        return result
    
    def _compare_results(self, baseline: Optional[AttackResult], 
                        attacks_under_load: List[AttackResult],
                        load_result: LoadTestResult) -> Dict:
        """Compare baseline vs attacks under load"""
        comparison = {
            'baseline_success': baseline.success if baseline else False,
            'baseline_response_time': baseline.response_time if baseline else 0,
            'total_attacks_under_load': len(attacks_under_load),
            'successful_attacks_under_load': len([a for a in attacks_under_load if a.success]),
            'baseline_success_rate': 100.0 if baseline and baseline.success else 0.0,
            'under_load_success_rate': (len([a for a in attacks_under_load if a.success]) / len(attacks_under_load) * 100) if attacks_under_load else 0.0,
            'avg_attack_response_time': sum([a.response_time for a in attacks_under_load]) / len(attacks_under_load) if attacks_under_load else 0,
            'load_avg_response_time': load_result.avg_response_time,
            'load_made_attacks_easier': False,
            'system_stressed': load_result.avg_response_time > 2000 or load_result.error_count > load_result.total_requests * 0.2
        }
        
        # Determine if load made attacks easier
        if baseline and baseline.success:
            # If baseline succeeded, check if more attacks succeeded under load
            if comparison['successful_attacks_under_load'] > 0:
                comparison['load_made_attacks_easier'] = True
        else:
            # If baseline failed but attacks under load succeeded, load made it easier
            if comparison['successful_attacks_under_load'] > 0:
                comparison['load_made_attacks_easier'] = True
        
        return comparison
    
    def generate_report(self, results: List[HybridTestResult]) -> str:
        """Generate HTML report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = RESULTS_DIR / f"hybrid_attack_load_report_{timestamp}.html"
        
        html_content = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Hybrid Attack + Load Test Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }}
        h1 {{ color: #d32f2f; }}
        h2 {{ color: #1976d2; margin-top: 30px; }}
        .result {{ margin: 20px 0; padding: 15px; border-left: 4px solid #1976d2; background: #f9f9f9; }}
        .success {{ border-left-color: #4caf50; }}
        .failure {{ border-left-color: #f44336; }}
        .warning {{ border-left-color: #ff9800; }}
        table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
        th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background: #1976d2; color: white; }}
        .metric {{ display: inline-block; margin: 10px 20px 10px 0; padding: 10px; background: #e3f2fd; border-radius: 4px; }}
        .critical {{ background: #ffebee; color: #c62828; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🎯 Hybrid Attack + Load Test Report</h1>
        <p><strong>Generated:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        
        <h2>📊 Summary</h2>
        <div class="metric">Total Tests: {len(results)}</div>
        <div class="metric">Successful Exploits Under Load: {sum([len([a for a in r.attacks_under_load if a.success]) for r in results])}</div>
        <div class="metric">Tests Where Load Made Attacks Easier: {sum([1 for r in results if r.comparison.get('load_made_attacks_easier', False)])}</div>
        
'''
        
        for idx, result in enumerate(results, 1):
            comparison = result.comparison
            html_content += f'''
        <h2>🎯 Test #{idx}: {result.endpoint}</h2>
        <div class="result {'success' if comparison.get('load_made_attacks_easier') else 'warning'}">
            <h3>Target: {result.target_url}{result.endpoint}</h3>
            
            <h4>📋 Baseline Attack (No Load)</h4>
            <p><strong>Status:</strong> {'✅ Success' if result.baseline_attack and result.baseline_attack.success else '❌ No vulnerabilities found'}</p>
            {f'<p><strong>Attack Type:</strong> {result.baseline_attack.attack_type}</p>' if result.baseline_attack else ''}
            {f'<p><strong>Response Time:</strong> {result.baseline_attack.response_time:.2f}ms</p>' if result.baseline_attack else ''}
            
            <h4>🌊 Load Test Results</h4>
            <div class="metric">Total Requests: {result.load_test_result.total_requests}</div>
            <div class="metric">Success Rate: {(result.load_test_result.success_count/result.load_test_result.total_requests*100):.1f}%</div>
            <div class="metric">Avg Response Time: {result.load_test_result.avg_response_time:.2f}ms</div>
            <div class="metric">Throughput: {result.load_test_result.throughput:.2f} req/s</div>
            <div class="metric">Errors: {result.load_test_result.error_count}</div>
            
            <h4>⚔️  Attacks Under Load</h4>
            <p><strong>Total Attack Attempts:</strong> {len(result.attacks_under_load)}</p>
            <p><strong>Successful Exploits:</strong> {len([a for a in result.attacks_under_load if a.success])}</p>
            
            {f'<div class="critical"><h4>🚨 CRITICAL FINDING: Load Made Attacks Easier!</h4>' if comparison.get('load_made_attacks_easier') else ''}
            {f'<p>Baseline success rate: {comparison.get("baseline_success_rate", 0):.1f}%</p>' if comparison.get('load_made_attacks_easier') else ''}
            {f'<p>Under-load success rate: {comparison.get("under_load_success_rate", 0):.1f}%</p>' if comparison.get('load_made_attacks_easier') else ''}
            {f'</div>' if comparison.get('load_made_attacks_easier') else ''}
            
            <h4>📈 Vulnerabilities Found Under Load</h4>
            <table>
                <tr>
                    <th>Attack Type</th>
                    <th>Payload</th>
                    <th>Response Time</th>
                    <th>Severity</th>
                </tr>
'''
            
            for attack in [a for a in result.attacks_under_load if a.success]:
                html_content += f'''
                <tr>
                    <td>{attack.attack_type}</td>
                    <td>{attack.payload[:50]}...</td>
                    <td>{attack.response_time:.2f}ms</td>
                    <td><strong>{attack.severity}</strong></td>
                </tr>
'''
            
            html_content += '''
            </table>
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
    """Main execution"""
    console.print(Panel.fit(
        "[bold red]⚠️  WARNING: Only use on systems you own or have explicit written permission to test![/bold red]\n\n"
        "[bold yellow]🎯 Hybrid Attack + Load Testing Tool[/bold yellow]\n"
        "Combines vulnerability exploitation with performance/flood testing"
    ))
    
    # Example targets (modify these to your authorized test targets)
    test_targets = [
        {
            "url": "http://localhost:3000",
            "endpoints": ["/rest/products/search?q=", "/api/users/"],
            "parameter": "q"
        },
        {
            "url": "http://localhost:8080",
            "endpoints": ["/vulnerabilities/sqli/", "/vulnerabilities/xss/"],
            "parameter": "id"
        }
    ]
    
    console.print("\n[bold cyan]Starting Hybrid Attack + Load Tests...[/bold cyan]\n")
    
    all_results = []
    
    for target in test_targets:
        tester = HybridAttackLoadTester(
            target_url=target["url"],
            endpoints=target["endpoints"],
            attack_types=['sqli', 'xss']
        )
        
        for endpoint in target["endpoints"]:
            try:
                result = tester.run_hybrid_test(
                    endpoint=endpoint,
                    parameter=target["parameter"],
                    load_duration=30,
                    concurrent_users=50
                )
                all_results.append(result)
            except Exception as e:
                console.print(f"[red]❌ Error testing {target['url']}{endpoint}: {str(e)}[/red]")
    
    # Generate report
    if all_results:
        report_generator = HybridAttackLoadTester("", [])
        report_path = report_generator.generate_report(all_results)
        console.print(f"\n[green]✅ Report saved to: {report_path}[/green]")


if __name__ == "__main__":
    main()




