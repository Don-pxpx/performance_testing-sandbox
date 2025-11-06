// k6 Spike Test - Sudden Traffic Burst
// Run with: docker run --rm -i -v ${PWD}:/scripts -e BASE_URL=http://host.docker.internal:3000 grafana/k6 run /scripts/spike_test.js

import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '10s', target: 10 },   // Normal load
    { duration: '5s', target: 100 },     // Sudden spike
    { duration: '30s', target: 100 },   // Maintain spike
    { duration: '5s', target: 10 },     // Return to normal
    { duration: '10s', target: 0 },     // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<3000'], // Allow higher response times during spike
    http_req_failed: ['rate<0.3'],    // Higher error tolerance during spike
  },
};

const BASE_URL = __ENV.BASE_URL || 'http://host.docker.internal:3000';

export default function () {
  const response = http.get(`${BASE_URL}/`);
  
  check(response, {
    'Spike test request successful': (r) => r.status === 200 || r.status === 503,
  });
  
  sleep(0.1); // Very short wait for spike scenario
}

