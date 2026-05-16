# Anticipatory Congestion Control Framework (ACCF) for 6G IoT Backhaul Networks

> **An MLP-Based Proactive Throttle Prediction System in a Software-Defined Environment**
>
> *Published by — Vinayak Khandelwal & Anmol Virmani, Department of Information Technology, Netaji Subhas University of Technology (NSUT), Delhi, India*

---

## Abstract

The ACCF replaces reactive congestion signaling with a proactive, intelligence-driven approach for 6G IoT backhaul networks. A **Multi-Layer Perceptron (MLP)** classifier—trained on live SDN telemetry—predicts queue saturation and issues preemptive `THROTTLE_SOURCE` commands before bufferbloat-induced latency spikes occur, achieving **97% classification accuracy** and a **55.3% reduction in average latency** with zero packet loss.

---

## Table of Contents

- [System Architecture](#system-architecture)
- [Results & Visualizations](#results--visualizations)
- [Repository Structure](#repository-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Dataset](#dataset)
- [Model Performance](#model-performance)
- [Key Findings](#key-findings)
- [Future Work](#future-work)
- [References](#references)


---

## System Architecture

The ACCF is split across **three logical planes**:

| Plane | Components | Role |
|---|---|---|
| **Data Plane** | `iot1`, `iot2`, `bs1`, OVS Switch, MEC Server `edge` | 6G IoT topology & traffic forwarding |
| **Control Plane** | OpenFlow Controller (Ryu), `ai_telemetry.py` | Stats polling & throttle enforcement |
| **Intelligence Plane** | `train_ann.py` (MLP Classifier) | Congestion prediction & action dispatch |

### Architecture Diagram

> *Three-plane ACCF architecture: Data Plane (topology), Control Plane (SDN/stats), and Intelligence Plane (ML logic)*

<img width="425" height="296" alt="nn2" src="https://github.com/user-attachments/assets/aaa17d74-220d-4cae-87b7-5891fd0873f3" />


---

### Operational Flowchart

> *The continuous loop from telemetry collection → MLP inference → throttle action*

<img width="437" height="492" alt="nnd1" src="https://github.com/user-attachments/assets/7b33ce5e-5806-4546-870c-ac8ddf4d9847" />


---

## Results & Visualizations

### 6G Backhaul Congestion Metrics — Queue Depth vs. Latency

> *Queue Depth (KB, red) and ICMP Latency (ms, blue dashed) plotted over 110 seconds. The dotted line marks the hard 32 KB TBF limit. The synchronized spikes confirm classic bufferbloat behavior.*

<img width="3000" height="1800" alt="nnd3" src="https://github.com/user-attachments/assets/a507e49d-e978-4b18-a99c-a85ab98c5e89" />


---

## Repository Structure

```text
6G-ACCF/
│
├── 6G_Backhaul.py          # Mininet-WiFi topology: IoT nodes, gNodeB, OVS, MEC server
├── ai_telemetry.py         # Live telemetry dashboard: queue size & latency polling
├── train_ann.py            # MLP training module + test-set verification
│
├── congestion_dataset.csv  # 110-sample telemetry corpus (generated from live emulation)
│
└── README.md
```

---

## Prerequisites

### System Requirements

- **OS:** Ubuntu 22.04 LTS (headless recommended)
- **RAM:** 8 GB minimum
- **CPU:** Quad-core (for Mininet virtualization)
- **Kernel:** Linux with `mac80211_hwsim` support

### Software Dependencies

```bash
# Core networking stack
sudo apt-get install -y mininet openvswitch-switch

# Mininet-WiFi (wireless emulation extension)
git clone https://github.com/intrig-unicamp/mininet-wifi
cd mininet-wifi && sudo util/install.sh -Wlnfv

# Python dependencies
pip install scikit-learn pandas plotext
```

| Package | Version | Purpose |
|---|---|---|
| `mininet-wifi` | ≥ 2.6 | 6G network emulation |
| `openvswitch` | 2.17 | OpenFlow 1.3 switching |
| `scikit-learn` | 1.2 | MLP classifier |
| `pandas` | ≥ 1.5 | Dataset handling |
| `plotext` | ≥ 5.0 | Terminal telemetry dashboard |

---

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/6G-ACCF.git
cd 6G-ACCF

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Verify Open vSwitch is running
sudo systemctl start openvswitch-switch
sudo ovs-vsctl show
```

---

## Usage

### Step 1 — Launch the 6G Network Topology

> **Requires root privileges** (Mininet-WiFi uses kernel namespaces)

```bash
sudo python3 6G_Backhaul.py
```

This spins up the emulated topology:

- Two IoT sensor stations (`iot1`, `iot2`) connected wirelessly to gNodeB `bs1`
- A wired backhaul link to the MEC server `edge` with a **2 Mbps / 32 KB Token Bucket Filter** bottleneck

### Step 2 — Generate Traffic & Collect Telemetry

Inside the Mininet CLI, saturate the backhaul:

```bash
# In Mininet CLI
iot1 iperf -c 10.0.0.3 -t 120 &
iot2 iperf -c 10.0.0.3 -t 120 &
```

Run the live telemetry dashboard in a separate terminal:

```bash
python3 ai_telemetry.py
```

The dashboard plots **live queue depth (KB)** and **latency (ms)** every second and activates `THROTTLE_SOURCE` logic when thresholds are breached.

### Step 3 — Train the MLP Classifier

Once `congestion_dataset.csv` has been collected from the live run:

```bash
python3 train_ann.py
```

**Expected output:**

```text
==================================================
  6G Deep-Predictive ANN Training Module v1.0
==================================================
[*] Loading congestion_dataset.csv...
[*] Initializing Artificial Neural Network (Hidden Layers: 2x16)...
[*] Training the ANN on 6G backhaul telemetry...
==================================================
[SUCCESS] ANN Training Complete!
[RESULTS] Predictive Accuracy: 97.00%
==================================================
```

---

## Dataset

The training corpus `congestion_dataset.csv` was captured **live** from the Mininet-WiFi emulation — not from a public dataset — to ensure the model fits the exact environment it monitors.

### Dataset Summary

| Property | Value |
|---|---|
| Total Snapshots | 110 |
| Sampling Rate | 1 per second |
| `MAINTAIN_FLOW` samples | 105 (95.5%) |
| `THROTTLE_SOURCE` samples | 5 (4.5%) |
| Training Set (80%) | 88 samples |
| Test Set (20%) | 22 samples |
| Feature Dimensions | 3 (Queue, Latency, Bandwidth) |
| Max Queue Depth | 31.73 KB |
| Max Latency Spike | 44.87 ms |
| Minimum Bandwidth (congested) | 0.93 Mbps |

### Feature Vector

Each telemetry snapshot is a 3-dimensional feature vector:

```text
xₜ = [ Qₜ (KB),  Lₜ (ms),  Bₜ (Mbps) ]
```

### Labeling Rule

```text
yₜ = THROTTLE_SOURCE   if Bₜ < 1.0 Mbps
     MAINTAIN_FLOW      otherwise
```

### Descriptive Statistics

| Feature | Min | Max | Mean | Std Dev |
|---|---|---|---|---|
| Queue Size (KB) | 10.26 | 31.73 | 21.50 | 6.11 |
| Latency (ms) | 20.09 | 44.87 | 33.28 | 7.20 |
| Bandwidth (Mbps) | 0.93 | 2.00 | 1.86 | 0.21 |

### Feature Correlation Matrix

| | Queue (KB) | Latency (ms) | Bandwidth (Mbps) |
|---|---|---|---|
| **Queue (KB)** | 1.0000 | −0.0552 | −0.2820 |
| **Latency (ms)** | −0.0552 | 1.0000 | −0.1926 |
| **Bandwidth (Mbps)** | −0.2820 | −0.1926 | 1.0000 |

> All pairwise correlations are weak (|r| < 0.3), confirming that each feature contributes independent information to the classifier.

---

## Model Performance

### MLP Architecture

```python
MLPClassifier(
    hidden_layer_sizes = (16, 16),   # 2 hidden layers, 16 neurons each
    activation         = 'relu',
    solver             = 'adam',
    max_iter           = 500
)
```

### Classification Results

| Metric | Value |
|---|---|
| Test Set Accuracy | **97%** |
| False Negatives (missed congestion) | **0** |
| False Positive Rate | Low |
| Baseline (always-MAINTAIN) | 95.5% |

### Throttle Event Analysis

| Log Time | Queue (KB) | Bandwidth (Mbps) | Pre-Throttle Latency | Post-Throttle Latency |
|---|---|---|---|---|
| 1773585581 | 30.07 | 0.93 | 40.42 ms | 23.06 ms |
| 1773585583 | 28.29 | 0.96 | 44.34 ms | 17.40 ms |
| 1773585596 | 29.69 | 0.99 | 42.61 ms | 14.34 ms |
| 1773585639 | 29.64 | 0.96 | 40.02 ms | 24.07 ms |
| 1773585655 | 30.71 | 0.95 | 40.66 ms | 16.21 ms |
| **Average** | **29.68** | **0.96** | **41.61 ms** | **18.61 ms** |

---

## Key Findings

### 1. Bufferbloat is Real and Measurable

Without intervention, the 32 KB TBF queue reached **31.73 KB** and latency spiked to **44.87 ms** — a **124% increase** over the 20 ms baseline. The queue never drained below 10.26 KB during the 110-second test, confirming a "standing queue" condition.

### 2. Bandwidth is the Perfect Congestion Indicator

A clean **0.81 Mbps gap** with zero class overlap separates congested from healthy states:

- `THROTTLE_SOURCE` events: **0.93 – 0.99 Mbps**
- `MAINTAIN_FLOW` samples: **1.80 – 2.00 Mbps**

### 3. Proactive vs. Reactive — ACCF Wins

| Metric | Drop-Tail (Reactive) | ACCF (Proactive) |
|---|---|---|
| Max Queue Depth | 31.73 KB (99.2%) | ≤ 30.81 KB |
| Max Latency | 44.87 ms | 23.06 ms |
| Avg Latency | 33.28 ms | ≈ 18.61 ms |
| Latency Recovery | N/A | **−22.99 ms (55.3%)** |
| Packet Loss | Yes (at overflow) | **Zero** |
| Response Type | Reactive (loss-based) | Proactive (ML) |
| Overhead | None | ~1 ms processing |

---

## Future Work

| Enhancement | Approach |
|---|---|
| **Temporal Prediction** | Replace MLP with **LSTM** to model queue fill-rate trends and throttle 5 seconds ahead |
| **Privacy-Preserving Training** | **Federated Learning** — model weights aggregated, raw telemetry stays local (HIPAA/GDPR compliant) |
| **Graded Throttling** | **Reinforcement Learning** (actor-critic) to learn continuous rate adjustments (12%, 28%, 45%) instead of binary on/off |
| **Anomaly Detection** | **Autoencoder** as a sanity layer to catch novel congestion signatures not in the training set |
| **Explainability** | **SHAP values** for human-readable throttle justification ("Throttled: latency +20%, bandwidth < 1 Mbps") |
| **Digital Twin Testing** | Pre-commit throttle actions to a virtual network clone before applying to live traffic |
| **Hardware Validation** | Port the emulation to real 6G testbed hardware |

---

## References

1. C. De Alwis et al., "Survey on 6G frontiers: Trends, applications, requirements, technologies and future research," *IEEE Open J. Commun. Soc.*, vol. 2, pp. 836–886, 2021.
2. F. Guo et al., "Enabling massive IoT toward 6G: A comprehensive survey," *IEEE Internet of Things J.*, vol. 8, no. 15, pp. 11891–11915, 2021.
3. K. Nichols and V. Jacobson, "Controlling queue delay," *ACM Queue*, vol. 10, no. 5, 2012.
4. S. Floyd and V. Jacobson, "Random early detection gateways for congestion avoidance," *IEEE/ACM Trans. Netw.*, vol. 1, no. 4, pp. 397–413, 1993.
5. D. Kreutz et al., "Software-defined networking: A comprehensive survey," *Proc. IEEE*, vol. 103, no. 1, pp. 14–76, 2015.
6. R. R. Fontes et al., "Mininet-WiFi: Emulating software-defined wireless networks," *Proc. CNSM*, Barcelona, 2015.
7. B. Lantz, B. Heller, and N. McKeown, "A network in a laptop," *Proc. HotNets-IX*, ACM, 2010.
8. F. Pedregosa et al., "Scikit-learn: Machine learning in Python," *JMLR*, vol. 12, pp. 2825–2830, 2011.
9. M. Reza et al., "Network traffic classification using machine learning techniques over SDN," *IJACSA*, vol. 8, no. 7, 2017.
10. R. H. Serag et al., "Machine-learning-based traffic classification in SDN," *Electronics*, vol. 13, no. 6, p. 1108, 2024.

---



<div align="center">
  <sub>Built with Mininet-WiFi · Open vSwitch · Scikit-learn · Python</sub><br>
  <sub>Netaji Subhas University of Technology (NSUT) · Delhi, India</sub>
</div>
