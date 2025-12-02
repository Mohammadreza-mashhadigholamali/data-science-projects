# 📡 ML4IoT — Homework 1  
_Timeseries Processing & Voice Activity Detection_  

**Authors:**  
- Mohammadreza Mashhadigholamali  
- Ivan Ludvig  
- Ali Samimi Fard  

This project implements the full Homework 1 pipeline for the Machine Learning for IoT course at Politecnico di Torino (2024/2025).  
It includes timeseries memory optimization using RedisTimeSeries and a real-time VAD-based control system.

---

## 📁 Contents
```
Homework 1/
│── ex1.py
│── ex2.py
│── Group11_Homework1.pdf
│── README.md
```

---

## 🧪 Exercise 1 — Timeseries Processing (Redis)
`ex1.py` implements:
- Temperature & humidity acquisition every **2 seconds**
- Redis TimeSeries keys:
  - `<mac>:temperature`
  - `<mac>:humidity`
  - Min/Max/Avg aggregated TS (1‑hour bucket)
- Retention:
  - **30 days** for raw TS
  - **365 days** for aggregated TS
- Compression enabled
- Command-line arguments:
  - `--host` `--port` `--user` `--password`

---

## 🎙 Exercise 2 — Voice Activity Detection (VAD)
`ex2.py` implements:
- Real-time microphone capture @ **48 kHz**
- Downsampling to **16 kHz**
- VAD classifier (spectrogram → dB → duration check)
- Toggle logic:
  - Detect speech → toggle measuring state
  - 5‑second lock to prevent fast switching
- Temperature & humidity printed every 2 seconds when active

Hyperparameter tuning included in `Group11_Homework1.pdf`.

---

## 📄 Report
The report includes:
- Memory calculations for 1000 clients  
- Hyperparameter search tables  
- Accuracy vs latency discussion  
- Final selected VAD configuration  

---

## ⚠️ Academic Note
The assignment PDF is **not** included.  
Only original student work and the group’s report are published.
