import http from 'k6/http';
import { check, sleep } from 'k6';

// 1. Cấu hình kịch bản test (Options)
export const options = {
  stages: [
    { duration: '10s', target: 20 }, // Tăng dần từ 0 lên 20 user trong 10 giây (Ramp-up)
    { duration: '20s', target: 20 }, // Giữ mức 20 user trong 20 giây (Plateau)
    { duration: '10s', target: 0 },  // Giảm dần về 0 user trong 10 giây (Ramp-down)
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% số request phải nhanh hơn 500ms
    http_req_failed: ['rate<0.01'],   // Tỉ lệ lỗi phải thấp hơn 1%
  },
};

// 2. Nội dung giả lập hành vi người dùng (Default function)
export default function () {
  // Test endpoint Health
  let res1 = http.get('http://127.0.0.1:5000/api/health');
  check(res1, { 'Status Health là 200': (r) => r.status === 200 });

  sleep(1); // Nghỉ 1 giây giữa các lần request để giống người dùng thật

  // Test endpoint tính toán nặng
  let res2 = http.get('http://127.0.0.1:5000/api/heavy-calculation?n=5000');
  check(res2, { 'Status Heavy là 200': (r) => r.status === 200 });
}