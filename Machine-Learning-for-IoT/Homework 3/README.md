# 🌐 ML4IoT — Homework 3  
_MQTT Communication, Redis Storage, REST API & Visualization_  

**Authors:**  
- Mohammadreza Mashhadigholamali  
- Ivan Ludvig  
- Ali Samimi Fard  

This project covers IoT sensor communication via MQTT, Redis storage, REST API development, and data visualization.

---

## 📁 Contents
```
Homework 3/
│── publisher.py
│── subscriber.ipynb
│── rest_server.ipynb
│── rest_client.ipynb
│── Group11_Homework3.pdf
│── README.md
```

---

## 📡 Exercise 1 — MQTT Publisher (publisher.py)
Implements:
- DHT11 readings  
- JSON messages:
  `{mac_address, timestamp, temperature, humidity}`
- Publish every 2 seconds to MQTT broker  
- Topic: `<student_id>`  

---

## 🗄️ Exercise 1.2 — Redis Subscriber (subscriber.ipynb)
Implements:
- MQTT subscription  
- Two Redis TS:
  - `<mac>:temperature`
  - `<mac>:humidity`

---

## 🌍 Exercise 2 — REST API Server (rest_server.ipynb)
Implements:
- `/status`  
- `/sensors` (POST)  
- `/data/{mac_address}?start_date=&end_date=`  
- Proper 200 / 400 / 404 responses  
- JSON schema for HistoricalData  

---

## 📈 Exercise 2.2 — REST Client (rest_client.ipynb)
Performs:
1. GET `/status`  
2. POST `/sensors`  
3. GET `/data` with date range  
4. Plots temperature & humidity  

---

## 📄 Report
Includes:
- MQTT vs REST comparison  
- API design justification  
- Response codes  
- Example visualizations  

---

## ⚠️ Academic Note
Assignment PDF is excluded.  
Only original implementation and report are shared.
