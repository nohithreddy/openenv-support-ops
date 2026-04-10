---
title: SupportOps Environment
emoji: 📊
colorFrom: blue
colorTo: purple
sdk: streamlit
app_file: app.py
pinned: false
---
# 🚀 SupportOpsEnv — Multi-Ticket Customer Support Simulation

## 📌 Overview

SupportOpsEnv is a **realistic, multi-ticket customer support environment** designed to evaluate and train AI agents in operational decision-making scenarios.

Unlike simple single-turn benchmarks, this environment simulates:

* 📊 Multiple concurrent tickets
* ⏱️ SLA (deadline) constraints
* ⚡ Priority-based decision making
* 😊 Customer satisfaction dynamics

---

## 🎯 Why This Matters

Modern AI agents must operate in **complex, multi-step environments** — not just answer isolated prompts.

SupportOpsEnv provides a **structured, reproducible environment** for:

* Agent benchmarking
* Reinforcement learning research
* Real-world workflow simulation

---

## 🧠 Environment Design

### Observation Space

* List of tickets (id, text, priority, SLA, resolved)
* Step count
* Customer satisfaction score

### Action Space

* `close` → Resolve ticket
* `escalate` → Send to higher support
* `reply` → Respond to user

---

## 🧪 Tasks

| Task   | Description                                 | Difficulty |
| ------ | ------------------------------------------- | ---------- |
| Easy   | Single ticket resolution                    | 🟢         |
| Medium | Multi-ticket + SLA handling                 | 🟡         |
| Hard   | Multi-ticket optimization under constraints | 🔴         |

---

## 🧮 Reward Function

* ✅ +0.4 → Successful resolution
* ⚠️ -0.3 → SLA missed
* ❌ -0.2 → Unnecessary escalation
* ⭐ Bonus → Efficiency & satisfaction

👉 Provides **dense feedback across the episode**

---

## 📊 Evaluation

Final score combines:

* Resolution rate (50%)
* SLA compliance (30%)
* Customer satisfaction (20%)

---

## 🖥️ Interactive Dashboard

This project includes a **live UI dashboard** built with Streamlit:

* View active tickets
* Take actions interactively
* Track rewards and metrics

---

## 🚀 Setup

```bash
git clone https://github.com/nohithreddy/openenv-support-ops.git
cd openenv-support-ops
pip install -r requirements.txt
```

---

## ▶️ Run Environment

```bash
python baseline/run_baseline.py
```

---

## 📊 Run Dashboard

```bash
streamlit run ui/dashboard.py
```

---

## 🐳 Docker

```bash
docker build -t support-env .
docker run support-env
```

---

## 🧪 OpenEnv Validation

```bash
openenv validate .
```

---

## 📈 Baseline Results

| Task   | Score |
| ------ | ----- |
| Easy   | 1.0   |
| Medium | ~0.75 |
| Hard   | ~0.5  |

---

## 🔥 Key Features

* Real-world task simulation
* Multi-objective reward system
* Deterministic grading
* Interactive visualization
* Fully reproducible

---

## 🏁 Conclusion

SupportOpsEnv bridges the gap between **static benchmarks and real-world agent systems**, providing a robust testbed for evaluating AI in operational environments.
=======
---
title: Support Ops Env
emoji: 🚀
colorFrom: red
colorTo: red
sdk: docker
app_port: 8501
tags:
- streamlit
pinned: false
short_description: Multi-ticket customer support simulation with SLA and reward
license: mit
---

# Welcome to Streamlit!

Edit `/src/streamlit_app.py` to customize this app to your heart's desire. :heart:

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).
