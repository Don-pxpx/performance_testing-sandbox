// k6 Stress Test - High Load Scenario
// Run with: docker run --rm -i -v ${PWD}:/scripts -e BASE_URL=http://host.docker.internal:3000 grafana/k6 run /scripts/stress_test.js

import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

const errorRate = new Rate('errors');

export const options = {
  stages: [
    { duration: '1m', target: 50 },   // Ramp up to 50 users
    { duration: '3m', target: 50 },    // Stay at 50 users
    { duration: '1m', target: 100 },   // Spike to 100 users
    { duration: '2m', target: 100 },   // Stay at 100 users
    { duration: '2m', target: 0 },    // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<2000'], // 95% of requests should be below 2s
    http_req_failed: ['rate<0.2'],    // Error rate should be less than 20%
  },
};

const BASE_URL = __ENV.BASE_URL || 'http://host.docker.internal:3000';

export default function () {
  // Multiple concurrent requests to stress the system
  const responses = http.batch([
    ['GET', `${BASE_URL}/`],
    ['GET', `${BASE_URL}/api/products`],
    ['GET', `${BASE_URL}/api/products`],
  ]);

  const success = check(responses[0], {
    'Stress test request successful': (r) => r.status === 200,
  });

  errorRate.add(!success);
  sleep(0.5); // Minimal wait time for high load
}

