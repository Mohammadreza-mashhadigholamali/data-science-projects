# 🤖 Machine Learning for IoT  
### Politecnico di Torino — Course Projects (2024/2025)

**Authors:**  
- Mohammadreza Mashhadigholamali  
- Ivan Ludvig  
- Ali Samimi Fard  

This repository contains all three graded homeworks completed for the  
**Machine Learning for Internet of Things (ML4IoT)** course at Politecnico di Torino.

Each homework focuses on a different ML/IoT integration theme, ranging from  
timeseries processing to keyword spotting, MQTT communication, and REST APIs.

Assignment PDFs are **not included** to respect university policy.  
Only original student work (code, notebooks, models, reports) is published.

---

# 📁 Repository Structure

```
Machine-Learning-for-IoT/
│
├── Homework 1/   # Redis timeseries + real-time VAD system
├── Homework 2/   # Keyword spotting model + smart hygrometer
└── Homework 3/   # MQTT → Redis → REST API IoT pipeline
```

---

# 📝 Homework Summaries

## 🔹 Homework 1 — Timeseries Processing & VAD
Focus:
- RedisTimeSeries (30-day raw retention, 365-day aggregated retention)
- Real-time DHT11 readings
- Aggregation (min/max/avg)
- Voice Activity Detection system (speech → toggle sensing)
- Accuracy/latency tuning

Deliverables:
- ex1.py, ex2.py
- Group11_Homework1.pdf

➡️ Detailed README inside *Homework 1/*

---

## 🔹 Homework 2 — Keyword Spotting (Up/Down) & Smart Hygrometer
Focus:
- MFCC preprocessing
- SepResNet8 KWS model
- TFLite conversion + latency optimization
- Voice interface for enabling/disabling sensing
- Push data to Redis in real-time

Deliverables:
- training.ipynb, ex1.py, model11.tflite
- Group11_Homework2.pdf

➡️ Detailed README inside *Homework 2/*

---

## 🔹 Homework 3 — MQTT, Redis Storage, REST API & Visualization
Focus:
- MQTT publisher (DHT11 → JSON → topic)
- MQTT subscriber (Deepnote → Redis TS)
- REST server with:
  - /status
  - /sensors
  - /data/{mac_address}
- REST client with data visualization

Deliverables:
- publisher.py, subscriber.ipynb
- rest_server.ipynb, rest_client.ipynb
- Group11_Homework3.pdf

➡️ Detailed README inside *Homework 3/*

---

# 🧠 Skills Demonstrated

Across the three projects, this repository demonstrates:

- TimeSeries processing & memory optimization  
- Real-time audio processing (VAD, MFCC, KWS)  
- Lightweight ML deployment on IoT devices (TFLite)  
- MQTT communication protocols  
- RESTful API design  
- Redis integration (streaming + storage)  
- End-to-end IoT data pipelines  
- Model latency / footprint optimization  
- Data visualization  

---

# ⚠️ Academic Note

This repository contains only:
- Original code  
- Trained models  
- Notebooks  
- Reports  
- Visualizations  

The ML4IoT assignment PDFs and datasets are **not included**.

---

# 📬 Contact

If you have questions regarding the implementation, feel free to reach out.
