# 🛡️ AI Prompt Firewall Micro-SaaS: 90-Day Sprint Challenge

<p align="center">
  <img src="https://img.shields.io/badge/built%20with-Python%20%7C%20JSON-blue?style=for-the-badge" alt="Built With Python">
  <img src="https://img.shields.io/badge/dependencies-None%20(Standard%20Lib)-green?style=for-the-badge" alt="Dependencies">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License">
</p>

---

## ⚡ Project Overview
> A self-contained, high-velocity defensive middleware proxy engine designed to intercept, sanitize, and validate incoming data payloads before they touch an LLM model, neutralizing **OWASP Top 10 LLM Vulnerabilities** in real time.

### 🌐 Core Defended Domains
**Web Apps** • **API Gateways** • **DevSecOps Pipelines** • **LLM Systems (Securing AI)**

---

## 🚀 What's Inside: The 90-Day Tracker

This live matrix displays my daily build journey, core defensive code modules, and real-time execution speeds achieved in our sandboxes.

| Sprint Day | Firewall Component / Filter Layer | Implemented Task / Security Goal | Performance Tax | Release Status |
| :---: | :--- | :--- | :---: | :---: |
| **Day 20** | 🕒 Layer 4: Sliding-Window Rate Limiter | Track rolling timestamp arrays to block brute-force traffic. | 0.0021 ms | 🟢 Passed |
| **Day 21** | 📦 Layer 5: Payload Volume Throttler | Measure raw string byte weights to kill buffer-bloat exploits. | 0.0015 ms | 🟢 Passed |
| **Day 22** | 🛠️ Layer 6: Structured Schema Guard | Match data models against strict schemas to fix type fuzzing. | 0.0166 ms | 🟢 Passed |
| **Day 23** | 🔤 Layer 7: Unstructured Input Sanitizer | Strip hidden C0/C1 control bytes and flatten look-alike symbols. | 0.0309 ms | 🟢 Passed |
| **Day 24** | 🎯 Layer 8: Signature Keyword Blocklist | Intercept explicit bypass phrases like 'system override'. | 0.0069 ms | 🟢 Passed |
| **Day 25** | 🔒 Layer 9: Upcoming Engine Module | *Awaiting active sprint initialization...* | -- | 🟡 Up Next |

---

## 📋 Features Checklist
- [x] Multi-layered perimeter proxy setup (Layers 4 to 8 active)
- [x] High-velocity substring matching filters
- [x] Automated Unicode transformation handling (NFKC normalization)
- [x] Full sandbox telemetry metrics logging (`overhead_ms`)
- [ ] Layer 9 context-aware behavioral vector mapping (*Pending*)

---

## 🏁 Quick Start Sandbox Execution

You can clone this entire sprint library and test any daily engine sandbox file instantly:

```bash
# 1. Clone the public repository
git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)

# 2. Enter the sprint directory
cd YOUR_REPO_NAME

# 3. Launch the sandbox file directly
python day24.py