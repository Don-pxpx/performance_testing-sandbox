#!/usr/bin/env python3
"""
Quick verification script for performance testing setup
Checks Docker, Python packages, and directory structure
"""

import subprocess
import sys
import os
from pathlib import Path
from rich.console import Console
from rich.panel import Panel

# Fix Windows encoding
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

console = Console()

SCRIPT_DIR = Path(__file__).parent.absolute()


def check_docker():
    """Check if Docker is available"""
    console.print("[cyan]🐳 Checking Docker...[/cyan]")
    try:
        result = subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            console.print(f"[green]✅ Docker found: {result.stdout.strip()}[/green]")
            
            # Check if Docker images are available
            console.print("[cyan]   Checking Docker images...[/cyan]")
            images = ["grafana/k6:latest", "justb4/jmeter:latest"]
            for image in images:
                result = subprocess.run(
                    ["docker", "images", "-q", image],
                    capture_output=True,
                    text=True
                )
                if result.stdout.strip():
                    console.print(f"[green]   ✅ {image} available[/green]")
                else:
                    console.print(f"[yellow]   ⚠️  {image} not found. Run: docker pull {image}[/yellow]")
            
            return True
        else:
            console.print("[red]❌ Docker not working properly[/red]")
            return False
    except FileNotFoundError:
        console.print("[red]❌ Docker not found. Please install Docker Desktop.[/red]")
        return False
    except Exception as e:
        console.print(f"[red]❌ Error checking Docker: {e}[/red]")
        return False


def check_python_packages():
    """Check if required Python packages are installed"""
    console.print("\n[cyan]🐍 Checking Python packages...[/cyan]")
    
    packages = ["locust", "rich"]
    all_installed = True
    
    for package in packages:
        try:
            __import__(package.replace("-", "_"))
            console.print(f"[green]✅ {package} installed[/green]")
        except ImportError:
            console.print(f"[red]❌ {package} not installed. Run: pip install {package}[/red]")
            all_installed = False
    
    return all_installed


def check_directory_structure():
    """Check if required directories exist"""
    console.print("\n[cyan]📁 Checking directory structure...[/cyan]")
    
    dirs = ["k6", "jmeter", "locust", "results"]
    all_exist = True
    
    for dir_name in dirs:
        dir_path = SCRIPT_DIR / dir_name
        if dir_path.exists() and dir_path.is_dir():
            console.print(f"[green]✅ {dir_name}/ directory exists[/green]")
        else:
            console.print(f"[yellow]⚠️  {dir_name}/ directory not found. Creating...[/yellow]")
            dir_path.mkdir(exist_ok=True)
            all_exist = False
    
    return all_exist


def check_test_files():
    """Check if test files exist"""
    console.print("\n[cyan]📄 Checking test files...[/cyan]")
    
    test_files = [
        ("k6/basic_api_test.js", "k6 basic test"),
        ("k6/stress_test.js", "k6 stress test"),
        ("k6/spike_test.js", "k6 spike test"),
        ("jmeter/api_test.jmx", "JMeter test plan"),
        ("locust/locustfile.py", "Locust test file"),
    ]
    
    all_exist = True
    for file_path, description in test_files:
        full_path = SCRIPT_DIR / file_path
        if full_path.exists():
            console.print(f"[green]✅ {description} found[/green]")
        else:
            console.print(f"[yellow]⚠️  {description} not found at {file_path}[/yellow]")
            all_exist = False
    
    return all_exist


def main():
    console.print(Panel.fit(
        "[bold cyan]🔍 Performance Testing Setup Verification[/bold cyan]",
        border_style="cyan"
    ))
    
    results = {
        "Docker": check_docker(),
        "Python Packages": check_python_packages(),
        "Directory Structure": check_directory_structure(),
        "Test Files": check_test_files(),
    }
    
    console.print("\n[bold]📊 Summary:[/bold]\n")
    
    all_passed = all(results.values())
    
    if all_passed:
        console.print(Panel.fit(
            "[bold green]✅ All checks passed! You're ready to run performance tests.[/bold green]",
            border_style="green"
        ))
    else:
        console.print(Panel.fit(
            "[bold yellow]⚠️  Some checks failed. Please fix the issues above.[/bold yellow]",
            border_style="yellow"
        ))
        console.print("\n[bold]Quick Fixes:[/bold]")
        console.print("  1. Install Docker Desktop: https://www.docker.com/products/docker-desktop/")
        console.print("  2. Pull Docker images: docker pull grafana/k6:latest && docker pull justb4/jmeter:latest")
        console.print("  3. Install Python packages: pip install locust rich")
        console.print("  4. Run tests: python performance/run_performance_tests.py list")


if __name__ == "__main__":
    main()




