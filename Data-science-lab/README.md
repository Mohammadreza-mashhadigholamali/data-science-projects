# 🎧 Intent Detection from Audio Commands

*Audio Classification using MFCC, PCA, and Artificial Neural Networks*

This project was developed as part of the **Data Science Lab: Process
and Methods** course at **Politecnico di Torino** (A.Y. 2022/2023).\
The goal is to classify the **intent** behind short spoken commands by
identifying both:

-   the **action** (e.g., increase, decrease, activate)\
-   the **object/device** (e.g., volume, lights, music)

This produces a **7-class audio classification** task.

------------------------------------------------------------------------

## 📌 Project Summary

The pipeline includes:

### ✔ Preprocessing

-   Load WAV audio at 16 kHz\
-   Remove silence (`librosa.effects.trim`)\
-   Noise reduction using **spectral gating**\
-   Zero-padding to fixed length for model input consistency

### ✔ Feature Extraction

-   **MFCC** (Mel-Frequency Cepstral Coefficients)

### ✔ Dimensionality Reduction

-   **PCA** keeping 95% variance

### ✔ Class Balancing

-   **Random Oversampling** to fix label imbalance

### ✔ Models Implemented

-   Random Forest\
-   Support Vector Machine (RBF)\
-   **Artificial Neural Network (MLP)** --- *Best result: **88.9%
    accuracy***

All results, plots, and comparisons are detailed in the report.

------------------------------------------------------------------------

## 📁 Folder Contents

    Data-science-lab/
    │── Project code.py        # Full training + inference pipeline
    │── Project report.pdf     # Full academic report with methodology & results
    │── README.md              # (this file)

------------------------------------------------------------------------

## ▶️ How to Run the Code

### 1. Prepare the dataset

The dataset is **not included** due to course policy.\
To run the script, create this structure locally:

    data/
    │── development.csv
    │── evaluation.csv
    │── audio/...   # full audio folder from the exam dataset

### 2. Install dependencies

``` bash
pip install numpy pandas librosa noisereduce tensorflow seaborn matplotlib scikit-learn imbalanced-learn tqdm
```

### 3. Run the project

``` bash
python "Project code.py"
```

The script will:

-   Extract MFCC features\
-   Apply PCA\
-   Balance the dataset\
-   Train the ANN\
-   Generate accuracy & loss plots\
-   Produce a confusion matrix\
-   Export predictions to **ANN.csv**

------------------------------------------------------------------------

## ⚠️ Dataset & Exam Policy

The dataset used in this project was provided exclusively for the **Data
Science Lab** exam.\
To respect academic rules:

-   The dataset is **not included**\
-   The assignment PDF is **not included**\
-   Only original student work (code + report) is published

------------------------------------------------------------------------

## 👥 Authors

**Mohammadreza Mashhadigholamali**  
**Ali Samimi Fard**

This project was developed as a 50/50 collaboration for the Data Science Lab exam at Politecnico di Torino.


For inquiries, feel free to reach out.
