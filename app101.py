"""
ANPR System — minimal consumer-facing UI.
Clean, modern, fully animated Dark Mode UI.
"""
 
import streamlit as st
import cv2
import numpy as np
import easyocr
import os
import re
from ultralytics import YOLO
 
# ── Page config ──────────────────────────────
st.set_page_config(
    page_title="AutoSense UI",
    page_icon="⚡",
    layout="centered", 
)
 
# ── CSS ──────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500;700&display=swap');
 
/* ── ANIMATIONS ── */
@keyframes fadeUp {
    0% { opacity: 0; transform: translateY(15px); }
    100% { opacity: 1; transform: translateY(0); }
}
@keyframes pulseGlow {
    0% { box-shadow: 0 0 0 0 rgba(0, 240, 255, 0.4); }
    70% { box-shadow: 0 0 15px 10px rgba(0, 240, 255, 0); }
    100% { box-shadow: 0 0 0 0 rgba(0, 240, 255, 0); }
}
@keyframes scanline {
    0% { top: -100px; }
    100% { top: 100%; }
}
 
html, body, [class*="css"], .stApp {
    background: #0a0a0b !important;
    color: #e0e0e0;
    font-family: 'Inter', sans-serif;
}
.block-container { padding: 3rem 1.5rem 4rem !important; max-width: 760px !important; }
#MainMenu, footer, header { visibility: hidden; }
 
h1,h2,h3 { font-family: 'Syne', sans-serif !important; color: #ffffff; }
 
/* ── TOP BAR ── */
.topbar {
    text-align: center;
    padding-bottom: 2rem;
    margin-bottom: 2rem;
    animation: fadeUp 0.8s ease-out;
}
.topbar-logo {
    font-family: 'Syne', sans-serif;
    font-size: 2.6rem;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: -1px;
}
.topbar-logo span { 
    color: #00f0ff; 
    text-shadow: 0 0 15px rgba(0, 240, 255, 0.4); 
}
.topbar-sub {
    font-size: 0.95rem;
    color: #888;
    margin-top: 0.5rem;
}
 
/* ── PLATE RESULT ── */
.plate-wrap {
    background: #111115;
    border-radius: 20px;
    padding: 3.5rem 2rem;
    text-align: center;
    margin: 2.5rem 0;
    box-shadow: 0 10px 40px rgba(0,0,0,0.5);
    border: 1px solid #1f1f26;
    animation: fadeUp 0.6s ease-out;
    position: relative;
    overflow: hidden;
}
/* Cyberpunk scan line effect */
.plate-wrap::before {
    content: '';
    position: absolute;
    left: 0; right: 0; height: 100px;
    background: linear-gradient(to bottom, transparent, rgba(0, 240, 255, 0.1), transparent);
    animation: scanline 3s linear infinite;
    pointer-events: none;
}
.plate-hint {
    font-family: 'Inter', sans-serif;
    font-size: 0.8rem;
    letter-spacing: 2.5px;
    color: #777;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
    font-weight: 600;
}
.plate-val {
    font-family: 'JetBrains Mono', monospace;
    font-size: 4rem;
    font-weight: 700;
    color: #00f0ff;
    letter-spacing: 14px;
    line-height: 1;
    margin-left: 14px; 
    text-shadow: 0 0 20px rgba(0, 240, 255, 0.3);
}
 
/* ── CHIPS ── */
.chip {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-family: 'Inter', sans-serif;
    font-size: 0.85rem;
    padding: 6px 16px;
    border-radius: 100px;
    font-weight: 500;
    margin-top: 1.5rem;
}
.chip-green { 
    background: rgba(16, 185, 129, 0.1); 
    color: #34d399; 
    border: 1px solid rgba(16, 185, 129, 0.3); 
}
 
/* ── UPLOAD ── */
[data-testid="stFileUploader"] {
    background: #15151a !important;
    border: 2px dashed #2a2a35 !important;
    border-radius: 16px !important;
    padding: 2.5rem !important;
    transition: all 0.3s ease;
    animation: fadeUp 0.6s ease-out 0.1s both;
}
[data-testid="stFileUploader"]:hover {
    border-color: #00f0ff !important;
    background: #1a1a24 !important;
    box-shadow: 0 0 20px rgba(0, 240, 255, 0.1) !important;
}
 
/* ── BUTTON ── */
.stButton > button {
    font-family: 'Inter', sans-serif !important;
    font-size: 1.05rem !important;
    font-weight: 600 !important;
    background: #00f0ff !important;
    color: #000 !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 1rem 2rem !important;
    width: 100% !important;
    transition: all 0.3s ease !important;
    animation: pulseGlow 2.5s infinite;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(0, 240, 255, 0.4) !important;
    background: #33f3ff !important;
}
 
/* ── IMAGES ── */
div[data-testid="stImage"] img { 
    border-radius: 16px; 
    box-shadow: 0 10px 40px rgba(0,0,0,0.5); 
    border: 1px solid #1f1f26;
    animation: fadeUp 0.6s ease-out;
}
div[data-testid="stImage"] {
    text-align: center;
    margin-bottom: 1rem;
}
div[data-testid="stImage"] p {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.8rem !important;
    color: #666 !important;
    margin-top: 0.8rem !important;
    font-weight: 500;
}
 
/* ── CUSTOM ALERTS ── */
.custom-alert {
    background: rgba(220, 38, 38, 0.1);
    color: #fca5a5;
    border: 1px solid rgba(220, 38, 38, 0.2);
    padding: 1rem 1.5rem;
    border-radius: 12px;
    font-size: 0.95rem;
    text-align: center;
    margin: 1.5rem 0;
    animation: fadeUp 0.4s ease-out;
}
.custom-warning {
    background: rgba(245, 158, 11, 0.05);
    color: #fcd34d;
    border: 1px solid rgba(245, 158, 11, 0.2);
    padding: 1rem 1.5rem;
    border-radius: 12px;
    font-size: 0.95rem;
    text-align: center;
    margin: 1.5rem 0;
    animation: fadeUp 0.4s ease-out;
}
</style>
""", unsafe_allow_html=True)
 
# ── Cached loaders ────────────────────────────
@st.cache_resource
def load_model():
    return YOLO("anpr_best.pt")
 
@st.cache_resource
def load_ocr():
    return easyocr.Reader(['en'])
 
# ── Preprocessing ─────────────────────────────
def preprocess_variants(plate_bgr):
    h, w  = plate_bgr.shape[:2]
    scale = min(max(2, 120 // max(h, 1)), 6)
    big   = cv2.resize(plate_bgr, (w * scale, h * scale), interpolation=cv2.INTER_CUBIC)
    gray  = cv2.cvtColor(big, cv2.COLOR_BGR2GRAY)
 
    clahe   = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    blur3   = cv2.GaussianBlur(gray, (3, 3), 0)
    blur5   = cv2.GaussianBlur(gray, (5, 5), 0)
    _, otsu = cv2.threshold(blur5, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
 
    return {
        'Grayscale':  gray,
        'CLAHE':      clahe.apply(gray),
        'Adaptive':   cv2.adaptiveThreshold(blur3, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2),
        'Otsu':       otsu,
        'Inverted':   cv2.bitwise_not(otsu),
        'Sharpened':  cv2.filter2D(gray, -1, np.array([[0,-1,0],[-1,5,-1],[0,-1,0]])),
    }
 
def clean_text(t):
    t = t.upper().strip()
    return re.sub(r'[^A-Z0-9]', '', t)
 
def run_ocr(reader, variants):
    results = []
    for name, img in variants.items():
        try:
            for (_, text, conf) in reader.readtext(
                img, detail=1, paragraph=False,
                allowlist='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
                mag_ratio=2.0,
                beamWidth=5,
                text_threshold=0.6,
                low_text=0.4
            ):
                c = clean_text(text)
                if c and len(c) >= 4:
                    results.append({'Text': c, 'Confidence': round(conf * 100, 1)})
        except Exception:
            continue
 
    if not results:
        return None
 
    results.sort(key=lambda x: x['Confidence'], reverse=True)
    plate_like = [r for r in results if 8 <= len(r['Text']) <= 10]
    best = plate_like[0] if plate_like else results[0]
    return best
 
# ── STATE MANAGEMENT ─────────────────────────
if "scan_clicked" not in st.session_state:
    st.session_state.scan_clicked = False
if "last_uploader_id" not in st.session_state:
    st.session_state.last_uploader_id = None
 
def handle_scan():
    st.session_state.scan_clicked = True
 
# ── UI LAYOUT ────────────────────────────────
st.markdown("""
<div class="topbar">
    <div class="topbar-logo">Auto<span>Sense</span></div>
    <div class="topbar-sub">Instantly extract license plates using Neural Networks.</div>
</div>
""", unsafe_allow_html=True)
 
uploaded = st.file_uploader(
    "Upload a car photo",
    type=["jpg","jpeg","png","webp"],
    label_visibility="collapsed"
)
 
if uploaded:
    # Reset state on new upload
    if st.session_state.last_uploader_id != uploaded.file_id:
        st.session_state.scan_clicked = False
        st.session_state.last_uploader_id = uploaded.file_id
        
    raw      = np.asarray(bytearray(uploaded.read()), dtype=np.uint8)
    img_bgr  = cv2.imdecode(raw, cv2.IMREAD_COLOR)
    img_rgb  = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    
    if not st.session_state.scan_clicked:
        st.image(img_rgb, use_column_width=True)
        st.button("Scan License Plate", type="primary", use_container_width=True, on_click=handle_scan)
    else:
        if not os.path.exists("anpr_best.pt"):
            st.markdown('<div class="custom-alert">Model missing: `anpr_best.pt` not found. Please place weights in folder.</div>', unsafe_allow_html=True)
            st.stop()
            
        with st.spinner("Analyzing image array..."):
            model = load_model()
            reader = load_ocr()
            
            res = model.predict(img_bgr, conf=0.30, iou=0.45, verbose=False)
            boxes = res[0].boxes
            
            if len(boxes) == 0:
                st.image(img_rgb, use_column_width=True)
                st.markdown('<div class="custom-warning">We couldn\'t detect a clear license plate. Please try a different angle.</div>', unsafe_allow_html=True)
                if st.button("Try Again", use_container_width=True):
                    st.session_state.scan_clicked = False
                    st.rerun()
                st.stop()
                
            best_box = sorted(boxes, key=lambda b: float(b.conf[0]), reverse=True)[0]
            x1, y1, x2, y2 = map(int, best_box.xyxy[0].tolist())
            H, W = img_bgr.shape[:2]
            pad = 2
            crop = img_bgr[max(0,y1-pad):min(H,y2+pad), max(0,x1-pad):min(W,x2+pad)]
            
            # Draw an electric cyan box around the plate 
            annotated_img = img_rgb.copy()
            cv2.rectangle(annotated_img, (max(0,x1-pad), max(0,y1-pad)), (min(W,x2+pad), min(H,y2+pad)), (0, 240, 255), 4)
            
            st.image(annotated_img, use_column_width=True, caption="Target Lock Established.")
            
            variants = preprocess_variants(crop)
            best_text = run_ocr(reader, variants)
            
            if best_text:
                st.markdown(f"""
                <div class="plate-wrap">
                    <div class="plate-hint">Extracted Plate Number</div>
                    <div class="plate-val">{best_text['Text']}</div>
                    <div class="chip chip-green">
                        <svg width="14" height="14" fill="none" stroke="currentColor" viewBox="0 0 24 24" style="margin-right:6px"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                        High Confidence Match
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown('<div class="custom-warning">A plate structure was found, but it is too blurry or obscured to confidently read the characters.</div>', unsafe_allow_html=True)
        
        st.button("Scan Another Image", use_container_width=True, on_click=lambda: st.session_state.update(scan_clicked=False))