# 🗣️ ML4IoT — Homework 2  
_Keyword Spotting (Up/Down) & Smart Hygrometer Integration_  

**Authors:**  
- Mohammadreza Mashhadigholamali  
- Ivan Ludvig  
- Ali Samimi Fard  

This project implements a full low-latency keyword spotting (KWS) system and smart hygrometer integration using Raspberry Pi.

---

## 📁 Contents
```
Homework 2/
│── training.ipynb
│── ex1.py
│── model11.tflite
│── Group11_Homework2.pdf
│── README.md
```

---

## 🎧 Exercise 1 — KWS Training (Deepnote)
`training.ipynb` includes:
- MFCC extraction  
- Lightweight CNN (SepResNet8)  
- PolynomialDecay LR schedule  
- Early stopping  
- Batch normalization  
- TFLite conversion  

Final results:
- **Accuracy: 99.5%**
- **TFLite Size: 41 KB**
- **Latency: 39.7 ms**

---

## 📟 Exercise 2 — Smart Hygrometer with VUI (ex1.py)
Code includes:
- Real-time microphone @ 48 kHz  
- MFCC feature extraction  
- TFLite inference (up/down KWS)  
- VAD silence detection  
- “Up” → enable monitoring  
- “Down” → disable monitoring  
- Push weather data to Redis every 2 seconds when active  

Matches all HW2 constraints.

---

## 📄 Report
The PDF contains:
- Preprocessing & training hyperparameter tables  
- Architecture description  
- Final metrics table  
- Explanation of optimizations  

---

## ⚠️ Academic Note
The assignment PDF is **NOT** published.  
Only original code, notebooks, model, and report are included.
