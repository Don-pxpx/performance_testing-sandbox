// k6 Basic API Performance Test
// Run with: docker run --rm -i -v ${PWD}:/scripts grafana/k6 run /scripts/basic_api_test.js

import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend } from 'k6/metrics';

// Custom metrics
const errorRate = new Rate('errors');
const apiResponseTime = new Trend('api_response_time');

// Test configuration
export const options = {
  stages: [
    { duration: '30s', target: 10 },   // Ramp up to 10 users
    { duration: '1m', target: 10 },     // Stay at 10 users
    { duration: '30s', target: 20 },    // Ramp up to 20 users
    { duration: '1m', target: 20 },      // Stay at 20 users
    { duration: '30s', target: 0 },     // Ramp down to 0 users
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],  // 95% of requests should be below 500ms
    http_req_failed: ['rate<0.1'],     // Error rate should be less than 10%
    errors: ['rate<0.1'],
  },
};

// Base URL - will be passed via environment variable or default
const BASE_URL = __ENV.BASE_URL || 'http://host.docker.internal:3000';

export default function () {
  // Test 1: Homepage
  let response = http.get(`${BASE_URL}/`);
  let success = check(response, {
    'Homepage status is 200': (r) => r.status === 200,
    'Homepage response time < 500ms': (r) => r.timings.duration < 500,
  });
  
  errorRate.add(!success);
  apiResponseTime.add(response.timings.duration);
  sleep(1);

  // Test 2: API endpoint (if available)
  response = http.get(`${BASE_URL}/api/products`);
  success = check(response, {
    'API status is 200': (r) => r.status === 200,
    'API response time < 1000ms': (r) => r.timings.duration < 1000,
  });
  
  errorRate.add(!success);
  apiResponseTime.add(response.timings.duration);
  sleep(1);
}

export function handleSummary(data) {
  return {
    '/results/k6_summary.json': JSON.stringify(data),
    stdout: textSummary(data, { indent: ' ', enableColors: true }),
  };
}

function textSummary(data, options) {
  // Simple text summary for console output
  return `
  =========================================
  k6 Test Summary
  =========================================
  Total Requests: ${data.metrics.http_reqs.values.count}
  Failed Requests: ${data.metrics.http_req_failed.values.count}
  Average Response Time: ${data.metrics.http_req_duration.values.avg.toFixed(2)}ms
  P95 Response Time: ${data.metrics.http_req_duration.values['p(95)'].toFixed(2)}ms
  Error Rate: ${(data.metrics.http_req_failed.values.rate * 100).toFixed(2)}%
  =========================================
  `;
}

