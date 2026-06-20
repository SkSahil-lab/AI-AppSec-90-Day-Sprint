# 🗺️ Master 90-Day AppSec Engineering Roadmap

This tracker details the overarching chronological development phases, target attack vectors, and deployment milestones across the full scope of our AI Prompt Firewall lifecycle.

---

## 📈 Milestone Phase Breakdown

### 🎯 Phase 1: Gateway Perimeter Security (Days 1 - 25)
*Focus: Low-overhead networking controls, data structure validations, and high-velocity string sanitization.*
- [x] **Days 1–10:** Core network socket proxy initialization & raw packet handling logic.
- [x] **Days 11–19:** Initial proof-of-concept testing for regex signatures and basic character mapping filters.
- [x] **Day 20:** Layer 4: Sliding-Window Rate Limiter Engine (`O(1)` state tracking to block Model DoS).
- [x] **Day 21:** Layer 5: Payload Volume Throttler (Enforcing strict byte-weight caps against resource starvation).
- [x] **Day 22:** Layer 6: Structured Schema Guard (Rigorous JSON template compliance to defuse type fuzzing).
- [x] **Day 23:** Layer 7: Unstructured Input Sanitizer (Stripping C0/C1 control bytes & handling NFKC Unicode look-alikes).
- [x] **Day 24:** Layer 8: Signature Keyword Blocklist (High-velocity early-exit filtering for known jailbreak strings).
- [ ] **Day 25:** Layer 9: Multi-Layer Diagnostic Integration Engine.

---

### 🧠 Phase 2: Vector Search & Semantic Guardrails (Days 26 - 50)
*Focus: Protecting contextual retrieval systems, vector database integrations, and handling advanced prompt transformations.*
- [ ] **Days 26–35:** Building dynamic local tokenizers to handle structural prompt chunking before context evaluation.
- [ ] **Days 36–42:** Building Vector Database Proxies (Scanning semantic lookups to detect nested or hidden jailbreak intent).
- [ ] **Days 43–50:** Engineering RAG Contextual Sanity Checks (Preventing indirect prompt injection via poisoned data stores).

---

### 🛡️ Phase 3: Adaptive Behavioral Defense (Days 51 - 75)
*Focus: Machine learning classifiers, anomaly tracking models, and real-time behavioral assessment.*
- [ ] **Days 51–60:** Implementing lightweight local embedding classifiers to score incoming prompt risk scores dynamically.
- [ ] **Days 61–68:** Building stateful conversation tracking nodes to catch distributed adversarial attacks over multiple turns.
- [ ] **Days 69–75:** Engineering automated pattern updates via hot-swappable configuration banks (Redis syncing).

---

### 🚀 Phase 4: Enterprise SaaS Scale & Containerization (Days 76 - 90)
*Focus: Cloud-native performance tuning, high-throughput optimization, and deployment pipelines.*
- [ ] **Days 76–82:** Refactoring the Layer 8 string matching logic into a compiled **Aho-Corasick automaton** tree.
- [ ] **Days 83–87:** Packing the entire proxy application suite into hyper-lightweight, multi-stage production Docker images.
- [ ] **Days 88–90:** Setting up automated CI/CD security validation workflows and shipping the live Micro-SaaS endpoint.