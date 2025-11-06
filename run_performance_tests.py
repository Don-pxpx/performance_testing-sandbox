#!/usr/bin/env python3
"""
Unified Performance Testing Runner
Supports k6, JMeter, and Locust via Docker (Windows compatible)
"""

import subprocess
import sys
import os
from pathlib import Path
from rich.console import Console
from rich.table import Table

console = Console()

# Fix Windows encoding
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

SCRIPT_DIR = Path(__file__).parent.absolute()
K6_DIR = SCRIPT_DIR / "k6"
JMETER_DIR = SCRIPT_DIR / "jmeter"
LOCUST_DIR = SCRIPT_DIR / "locust"
RESULTS_DIR = SCRIPT_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)


def run_k6_test(test_script: str, base_url: str, output_file: str = None):
    """Run k6 performance test via Docker"""
    console.print(
        f"[bold cyan]🚀 Running k6 Test[/bold cyan]\n"
        f"[dim]Script: {test_script}[/dim]\n"
        f"[dim]Target: {base_url}[/dim]\n"
    )
    
    try:
        # Convert Windows path to Docker-compatible path
        volume_mount = f"{K6_DIR.absolute()}:/scripts"
        
        cmd = [
            "docker", "run", "--rm", "-i",
            "-v", volume_mount,
            "-e", f"BASE_URL={base_url}",
            "grafana/k6:latest",
            "run", f"/scripts/{test_script}"
        ]
        
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        console.print("[bold green]✅ k6 test completed successfully[/bold green]")
        console.print(result.stdout)
        
        return True
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]❌ k6 test failed: {e}[/bold red]")
        console.print(e.stderr)
        return False
    except FileNotFoundError:
        console.print("[bold red]❌ Docker not found. Please install Docker Desktop.[/bold red]")
        return False


def run_jmeter_test(test_plan: str, base_url: str):
    """Run JMeter performance test via Docker"""
    console.print(
        f"[bold yellow]🔧 Running JMeter Test[/bold yellow]\n"
        f"[dim]Test Plan: {test_plan}[/dim]\n"
        f"[dim]Target: {base_url}[/dim]\n"
    )
    
    try:
        volume_mount = f"{JMETER_DIR.absolute()}:/scripts"
        results_mount = f"{RESULTS_DIR.absolute()}:/results"
        
        cmd = [
            "docker", "run", "--rm", "-i",
            "-v", volume_mount,
            "-v", results_mount,
            "-e", f"BASE_URL={base_url}",
            "justb4/jmeter:latest",
            "-n", "-t", f"/scripts/{test_plan}",
            "-l", "/results/jmeter_results.jtl",
            "-e", "-o", "/results/jmeter_html_report"
        ]
        
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        console.print("[bold green]✅ JMeter test completed successfully[/bold green]")
        console.print(f"[cyan]📊 HTML report available at: {RESULTS_DIR / 'jmeter_html_report' / 'index.html'}[/cyan]")
        
        return True
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]❌ JMeter test failed: {e}[/bold red]")
        console.print(e.stderr)
        return False
    except FileNotFoundError:
        console.print("[bold red]❌ Docker not found. Please install Docker Desktop.[/bold red]")
        return False


def run_locust_test(base_url: str, users: int = 10, spawn_rate: float = 2, run_time: str = "60s"):
    """Run Locust performance test (native Python, no Docker needed)"""
    console.print(
        f"[bold green]🦗 Running Locust Test[/bold green]\n"
        f"[dim]Target: {base_url}[/dim]\n"
        f"[dim]Users: {users}, Spawn Rate: {spawn_rate}/s, Duration: {run_time}[/dim]\n"
    )
    
    try:
        locustfile = LOCUST_DIR / "locustfile.py"
        
        if not locustfile.exists():
            console.print(f"[bold red]❌ Locustfile not found at {locustfile}[/bold red]")
            return False
        
        cmd = [
            sys.executable, "-m", "locust",
            "-f", str(locustfile),
            "--host", base_url,
            "--users", str(users),
            "--spawn-rate", str(spawn_rate),
            "--run-time", run_time,
            "--headless",
            "--html", str(RESULTS_DIR / "locust_report.html"),
            "--csv", str(RESULTS_DIR / "locust_results")
        ]
        
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        console.print("[bold green]✅ Locust test completed successfully[/bold green]")
        console.print(f"[cyan]📊 HTML report available at: {RESULTS_DIR / 'locust_report.html'}[/cyan]")
        
        return True
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]❌ Locust test failed: {e}[/bold red]")
        console.print(e.stderr)
        return False
    except FileNotFoundError:
        console.print("[bold red]❌ Locust not installed. Run: pip install locust[/bold red]")
        return False


def list_available_tests():
    """List all available performance tests"""
    console.print("\n[bold]📋 Available Performance Tests[/bold]\n")
    
    table = Table(title="Performance Tests")
    table.add_column("Tool", style="cyan")
    table.add_column("Test Name", style="green")
    table.add_column("Script File", style="yellow")
    
    # k6 tests
    k6_tests = [
        ("Basic API Test", "basic_api_test.js"),
        ("Stress Test", "stress_test.js"),
        ("Spike Test", "spike_test.js"),
    ]
    for name, script in k6_tests:
        table.add_row("k6", name, script)
    
    # JMeter tests
    jmeter_tests = [
        ("API Test", "api_test.jmx"),
    ]
    for name, script in jmeter_tests:
        table.add_row("JMeter", name, script)
    
    # Locust tests
    table.add_row("Locust", "Web App Load Test", "locustfile.py")
    
    console.print(table)
    console.print("\n[bold]Usage Examples:[/bold]\n")
    console.print("  # Run k6 basic test")
    console.print("  python run_performance_tests.py k6 basic http://localhost:3000\n")
    console.print("  # Run JMeter test")
    console.print("  python run_performance_tests.py jmeter api http://localhost:3000\n")
    console.print("  # Run Locust test")
    console.print("  python run_performance_tests.py locust http://localhost:3000 --users 50\n")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Performance Testing Runner - k6, JMeter, and Locust",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run k6 basic test
  python run_performance_tests.py k6 basic http://localhost:3000
  
  # Run JMeter test
  python run_performance_tests.py jmeter api http://localhost:3000
  
  # Run Locust test
  python run_performance_tests.py locust http://localhost:3000 --users 50
  
  # List all available tests
  python run_performance_tests.py list
        """
    )
    
    subparsers = parser.add_subparsers(dest="tool", help="Performance testing tool")
    
    # k6 subcommand
    k6_parser = subparsers.add_parser("k6", help="Run k6 test")
    k6_parser.add_argument("test", choices=["basic", "stress", "spike"], help="Test type")
    k6_parser.add_argument("url", help="Target URL")
    
    # JMeter subcommand
    jmeter_parser = subparsers.add_parser("jmeter", help="Run JMeter test")
    jmeter_parser.add_argument("test", choices=["api"], help="Test type")
    jmeter_parser.add_argument("url", help="Target URL")
    
    # Locust subcommand
    locust_parser = subparsers.add_parser("locust", help="Run Locust test")
    locust_parser.add_argument("url", help="Target URL")
    locust_parser.add_argument("--users", type=int, default=10, help="Number of users")
    locust_parser.add_argument("--spawn-rate", type=float, default=2, help="Users per second")
    locust_parser.add_argument("--run-time", default="60s", help="Test duration")
    
    # List subcommand
    list_parser = subparsers.add_parser("list", help="List all available tests")
    
    args = parser.parse_args()
    
    if args.tool == "k6":
        test_map = {
            "basic": "basic_api_test.js",
            "stress": "stress_test.js",
            "spike": "spike_test.js",
        }
        script = K6_DIR / test_map[args.test]
        run_k6_test(script.name, args.url)
    
    elif args.tool == "jmeter":
        test_map = {
            "api": "api_test.jmx",
        }
        script = JMETER_DIR / test_map[args.test]
        run_jmeter_test(script.name, args.url)
    
    elif args.tool == "locust":
        run_locust_test(args.url, args.users, args.spawn_rate, args.run_time)
    
    elif args.tool == "list" or not args.tool:
        list_available_tests()


if __name__ == "__main__":
    main()




