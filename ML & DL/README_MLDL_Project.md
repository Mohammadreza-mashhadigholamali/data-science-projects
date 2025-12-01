# 🧠 Real-Time Domain Adaptation in Semantic Segmentation

*A Machine Learning & Deep Learning Project (Politecnico di Torino,
2024)*

This project explores **domain adaptation** techniques for **real-time
semantic segmentation**.\
The goal is to understand how models trained on **synthetic data
(GTA5)** perform on **real-world images (Cityscapes)**,\
and how to reduce the **domain shift** using:

-   Data augmentation\
-   FDA (Fourier Domain Adaptation)\
-   DACS (Domain Adaptation via Cross-domain Sampling -- optional)

This project follows the official MLDL 2024 assignment steps.

------------------------------------------------------------------------

## 📁 Project Structure

    ML & DL/
    │── Real_time_Domain_Adaptation_in_Semantic_Segmentation.pdf   # Full project report
    │── Appendix.pdf                                                # Detailed tables & results
    │── source/                                                     # All Jupyter notebooks
    │     ├── 1-MLDL_Step_2a.ipynb
    │     ├── 2-Metrics_2a.ipynb
    │     ├── 3-MLDL_Step_2b.ipynb
    │     ├── 4-Metrics_2b.ipynb
    │     ├── 5-MLDL_Step_3a.ipynb
    │     ├── 6-MLDL_Step_3b.ipynb
    │     ├── 7-MLDL_Step_4b_FDA.ipynb

------------------------------------------------------------------------

## 🎯 Objectives of the Project

### **✔ Step 2 --- Baselines on Cityscapes**

-   Train **DeepLabV2** (classic segmentation)
-   Train **BiSeNet** (real‑time segmentation)
-   Measure:
    -   mIoU\
    -   FLOPs\
    -   Params\
    -   Latency

### **✔ Step 3 --- Domain Shift (GTA5 → Cityscapes)**

-   Train BiSeNet on GTA5 synthetic dataset
-   Test on Cityscapes real images
-   Observe drop in mIoU (domain shift problem)

### **✔ Step 3b --- Data Augmentation**

Experiments with: - Gaussian Blur\
- Horizontal Flip\
- Combined augmentations

### **✔ Step 4 --- Domain Adaptation**

Image‑to‑image approach: - **FDA (Fourier Domain Adaptation)**\
- (Optional: DACS)

------------------------------------------------------------------------

## 📊 Summary of Key Results

### **💡 Baseline on Cityscapes**

  Model       mIoU
  ----------- --------
  DeepLabV2   53.57%
  BiSeNet     34.62%

### **💡 Domain Shift (GTA5 → Cityscapes)**

-   BiSeNet: **21.79% mIoU**

### **💡 Augmentations**

-   Gaussian Blur: **23.60%**
-   Horizontal Flip: **21.89%**
-   Blur + Flip: **23.56%**

### **💡 FDA Domain Adaptation**

-   FDA: **29.21% mIoU**

Detailed class-wise performance is available in **Appendix.pdf**.

------------------------------------------------------------------------

## ▶️ How to Use the Notebooks

1.  Download the **Cityscapes** and **GTA5** datasets\
2.  Follow the expected folder structure inside the notebooks\
3.  Open each notebook in the `source/` directory in order\
4.  Run the training and evaluation steps sequentially

> ⚠️ **Datasets are NOT included** due to academic restrictions.

------------------------------------------------------------------------

## 👥 Authors

-   **Mohammadreza Mashhadigholamali**\
-   **Ali Samimi Fard**\
-   **Mahsa Mohammadi**

This work was completed collaboratively as part of the **Machine
Learning & Deep Learning** course at Politecnico di Torino.

------------------------------------------------------------------------

## 📄 License & Academic Note

This repository contains **only original student work** (code,
notebooks, report, appendix).\
The course assignment instructions and datasets are **not included**,
respecting university policy.
