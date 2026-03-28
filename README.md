# 🚗 AutoSense-ANPR System (License Plate Recognition)
The AutoSense-ANPR system employs Automatic Number Plate Recognition technology which utilizes YOLOv8 EasyOCR and Streamlit software for its operation.
The system identifies license plates from pictures and successfully retrieves the plate number with advanced accuracy.

---

## ✨ Features

- 🔍 **Plate Detection** using YOLOv8
- 🔤 **Text Recognition (OCR)** using EasyOCR
- 🎨 **Modern Dark UI** (Cyberpunk-style Streamlit interface)
- ⚡ The system processes data quickly because of its efficient initial stage evaluation
- 📷 The system accepts image uploads in JPG PNG and WEBP formats
- 🧠 The system uses various initial data analysis methods to enhance optical character recognition performance


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
│── app101.py                 # Main Streamlit app
│── anpr_best.pt           # Trained YOLO model weights
│── requirements.txt       # Dependencies
│── README.md              # Documentation
│── ANPR_Training_Colab.ipynb         # Model Training
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
streamlit run app101.py
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
