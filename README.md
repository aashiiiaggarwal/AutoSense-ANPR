# 🚗 AutoSense — ANPR System (License Plate Recognition)

AutoSense is a modern **Automatic Number Plate Recognition (ANPR)** system built using **YOLOv8 + EasyOCR + Streamlit**.  
It detects vehicle license plates from images and extracts the plate number with high confidence.

---

## ✨ Features

- 🔍 **Plate Detection** using YOLOv8
- 🔤 **Text Recognition (OCR)** using EasyOCR
- 🎨 **Modern Dark UI** (Cyberpunk-style Streamlit interface)
- ⚡ Fast inference with optimized preprocessing
- 📷 Supports JPG, PNG, WEBP uploads
- 🧠 Multiple preprocessing techniques for better OCR accuracy

---

## 🧠 Tech Stack

- **Frontend/UI:** Streamlit  
- **Model:** YOLOv8 (Ultralytics)  
- **OCR:** EasyOCR  
- **Image Processing:** OpenCV, NumPy  
- **Language:** Python  

---

## 📁 Project Structure

```
AutoSense-ANPR/
│── app.py                 # Main Streamlit app
│── anpr_best.pt           # Trained YOLO model weights
│── requirements.txt       # Dependencies
│── README.md              # Documentation
│── sample_images/         # Test images (optional)
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/AutoSense-ANPR.git
cd AutoSense-ANPR
```

### 2. Create virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the App

```bash
streamlit run app.py
```

---

## 📦 Model Setup

Make sure your trained YOLO model file is present:

```
anpr_best.pt
```

Place it in the root directory.

---

## 📸 How It Works

1. Upload a vehicle image  
2. YOLO detects license plate region  
3. Image is cropped and enhanced  
4. EasyOCR extracts text  
5. Best result is displayed with confidence  

---

## 🧪 Preprocessing Techniques Used

- Grayscale conversion  
- CLAHE (Contrast enhancement)  
- Adaptive Thresholding  
- Otsu Thresholding  
- Image sharpening  

---

## 🚀 Future Improvements

- 🎥 Video-based detection  
- 🚦 Traffic violation integration  
- 🌐 Deploy on web (Streamlit Cloud / AWS)  
- 📊 Database logging of detected plates  
- 📱 Mobile app integration  

---

## 👨‍💻 Author

- Aashi 
---

## ⭐ Show Some Love

If you found this useful, give this repo a ⭐ on GitHub!
