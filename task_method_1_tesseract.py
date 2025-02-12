import cv2
import pytesseract
import json
import sqlite3
import re

# Set Tesseract path (Change if needed)
# include this line if tesseract is not added to path else ignore
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def preprocess_image(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.GaussianBlur(img, (5, 5), 0)
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
    return cv2.resize(img, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)

def extract_text_tesseract(image_path):
    img = preprocess_image(image_path)
    return pytesseract.image_to_string(img, config="--psm 6").strip()
def extract_data(text):
    data = {}
    data['patient_name'] = re.search(r"Patient's Name[:\s]+([A-Za-z\s]+)", text)
    data['dob'] = re.search(r"DOB[:\s]+(\d{2}/\d{2}/\d{4})", text)
    data['date_of_visit'] = re.search(r"Date of Visit[:\s]+(\d{2}/\d{2}/\d{4})", text)
    data['injection'] = re.search(r"Injection[:\s]+(Yes|No)", text)
    data['exercise_therapy'] = re.search(r"Exercise Therapy[:\s]+(Yes|No)", text)
    data['pain_symptoms'] = {
        'pain': re.search(r"Pain[:\s]*(\d)", text),
        'numbness': re.search(r"Numbness[:\s]*(\d)", text),
        'tingling': re.search(r"Tingling[:\s]*(\d)", text),
        'burning': re.search(r"Burning[:\s]*(\d)", text),
        'tightness': re.search(r"Tightness[:\s]*(\d)", text)
    }
    data['difficulty_ratings'] = {
        'bending': re.search(r"Bending[:\s]*(\d)", text),
        'putting_on_shoes': re.search(r"Putting on Shoes[:\s]*(\d)", text),
        'sleeping': re.search(r"Sleeping[:\s]*(\d)", text),
    }

    data['patient_changes'] = {
        'since_last_treatment': re.search(r"Since Last Treatment[:\s]+(\w+)", text),
        'since_start_of_treatment': re.search(r"Since Start of Treatment[:\s]+(\w+)", text),
        'last_3_days': re.search(r"Last 3 Days[:\s]+(\w+)", text)
    }

    data['medical_assistant_data'] = {
        'blood_pressure': re.search(r"Blood Pressure[:\s]+([\d/]+)", text),
        'hr': re.search(r"Heart Rate[:\s]*(\d+)", text),
        'weight': re.search(r"Weight[:\s]*(\d+)", text),
        'height': re.search(r"Height[:\s]*([\d\']+)", text),
        'spo2': re.search(r"SpO2[:\s]*(\d+)", text),
        'temperature': re.search(r"Temperature[:\s]*([\d.]+)", text),
        'blood_glucose': re.search(r"Blood Glucose[:\s]*(\d+)", text),
        'respirations': re.search(r"Respirations[:\s]*(\d+)", text)
    }

    for key in data:
        if isinstance(data[key], dict):
            for sub_key in data[key]:
                data[key][sub_key] = data[key][sub_key].group(1) if data[key][sub_key] else 'N/A'
        else:
            data[key] = data[key].group(1) if data[key] else 'N/A'

    return data

def save_results(data, method="Tesseract"):
    json_data = json.dumps(data, indent=4)

    with open(f"ocr_{method.lower()}_results.json", "w") as f:
        f.write(json_data)

    conn = sqlite3.connect(f"ocr_{method.lower()}_results.db")
    conn.execute(""" 
        CREATE TABLE IF NOT EXISTS ocr_data (
            id INTEGER PRIMARY KEY,
            method TEXT,
            form_json TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.execute("INSERT INTO ocr_data (method, form_json) VALUES (?, ?)", (method, json_data))

    conn.commit()
    conn.close()
image_path = "C:\\Users\\hp\\Desktop\\image1.png"  # Change to your image file
text = extract_text_tesseract(image_path)
extracted_data = extract_data(text)
save_results(extracted_data, "Tesseract")

print("\nExtracted Data:")
print(extracted_data)
