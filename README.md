# Remote Monitoring & Control

Built for a Network Design (Internet Engineering) course, this lightweight code allows multiple agents to communicate with a master node and vice versa.

**What it does?**

* Auto-discover agents over UDP
* Remote restart commands
* Fetch CPU, memory, and process statistics via TCP or HTTP

**Components:**

* **agent.py**: Listens for discovery; serves stats; broadcasts alerts; handles reboots
* **master.py**: Discovers agents; requests stats; issues restarts (Socket & REST modes)

**Setup:**

Run agent on targets # Run master on controller

```bash
pip install -r requirements.txt
```
