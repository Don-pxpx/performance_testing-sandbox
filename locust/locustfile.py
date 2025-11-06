"""
Locust Performance Test Script
Load testing scenarios for web applications and APIs
"""

from locust import HttpUser, task, between
from locust.exception import StopUser


class WebAppUser(HttpUser):
    """Simulates a web application user"""
    wait_time = between(1, 3)  # Wait 1-3 seconds between requests
    
    def on_start(self):
        """Called when a user starts"""
        pass
    
    @task(3)
    def view_homepage(self):
        """View homepage - high frequency task"""
        self.client.get("/", name="Homepage")
    
    @task(2)
    def view_api_products(self):
        """View API products - medium frequency task"""
        self.client.get("/api/products", name="API Products")
    
    @task(1)
    def view_api_search(self):
        """Search API - low frequency task"""
        self.client.get("/api/products?q=test", name="API Search")


class APIUser(HttpUser):
    """Simulates an API client"""
    wait_time = between(0.5, 2)
    
    @task(5)
    def get_products(self):
        """Get products endpoint"""
        with self.client.get("/api/products", name="GET Products", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Unexpected status code: {response.status_code}")
    
    @task(2)
    def get_homepage(self):
        """Get homepage"""
        self.client.get("/", name="GET Homepage")


class SpikeUser(HttpUser):
    """Simulates spike traffic"""
    wait_time = between(0.1, 0.5)  # Very short wait times
    
    @task(10)
    def rapid_requests(self):
        """Rapid fire requests"""
        self.client.get("/", name="Spike Request")




