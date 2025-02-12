import cv2
import easyocr
import json
import sqlite3
import re
from datetime import datetime

def preprocess_image(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.GaussianBlur(img, (3, 3), 0)
    return cv2.resize(img, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)

def extract_text(image_path):
    img = preprocess_image(image_path)
    cv2.imwrite("temp.png", img)  
    reader = easyocr.Reader(["en"])
    result = reader.readtext("temp.png")
    return "\n".join([text[1] for text in result]).strip()

def extract_data(text):
    data = {}
    name_match = re.search(r"Patient Name\s*[:\-]?\s*([A-Za-z\s]+)", text)
    if name_match:
        data["patient_name"] = name_match.group(1).strip()

    dob_match = re.search(r"DOB\s*[:\-]?\s*(\d{2}/\d{2}/\d{4})", text)
    if dob_match:
        data["dob"] = dob_match.group(1).strip()
    date_match = re.search(r"Date\s*[:\-]?\s*(\d{2}/\d{2}/\d{4})", text)
    if date_match:
        data["date"] = date_match.group(1).strip()

    injection_match = re.search(r"Injection\s*[:\-]?\s*(Yes|No)", text, re.IGNORECASE)
    if injection_match:
        data["injection"] = injection_match.group(1).strip()

    exercise_match = re.search(r"Exercise Therapy\s*[:\-]?\s*(Yes|No)", text, re.IGNORECASE)
    if exercise_match:
        data["exercise_therapy"] = exercise_match.group(1).strip()

    difficulty_ratings = {}
    difficulty_patterns = ["bending", "putting on shoes", "sleeping"]
    for rating in difficulty_patterns:
        match = re.search(rf"{rating}[\s:]*([0-5])", text, re.IGNORECASE)
        if match:
            difficulty_ratings[rating.replace(" ", "_")] = int(match.group(1))
    data["difficulty_ratings"] = difficulty_ratings

    changes = {}
    changes["since_last_treatment"] = re.search(r"Since last treatment\s*[:\-]?\s*(.*)", text)
    changes["since_start_of_treatment"] = re.search(r"Since start of treatment\s*[:\-]?\s*(.*)", text)
    changes["last_3_days"] = re.search(r"Last 3 days\s*[:\-]?\s*(.*)", text)
    data["patient_changes"] = {key: val.group(1).strip() if val else "" for key, val in changes.items()}

    pain_symptoms = {}
    pain_patterns = ["pain", "numbness", "tingling", "burning", "tightness"]
    for symptom in pain_patterns:
        match = re.search(rf"{symptom}[\s:]*([0-9])", text, re.IGNORECASE)
        if match:
            pain_symptoms[symptom] = int(match.group(1))
    data["pain_symptoms"] = pain_symptoms

    ma_data = {}
    ma_fields = {
        "blood_pressure": r"Blood Pressure\s*[:\-]?\s*([\d/]+)",
        "hr": r"HR\s*[:\-]?\s*(\d+)",
        "weight": r"Weight\s*[:\-]?\s*(\d+)",
        "height": r"Height\s*[:\-]?\s*([A-Za-z0-9'\" ]+)",
        "spo2": r"SpO2\s*[:\-]?\s*(\d+)",
        "temperature": r"Temperature\s*[:\-]?\s*(\d+\.\d+|\d+)",
        "blood_glucose": r"Blood Glucose\s*[:\-]?\s*(\d+)",
        "respirations": r"Respirations\s*[:\-]?\s*(\d+)"
    }

    for field, pattern in ma_fields.items():
        match = re.search(pattern, text)
        if match:
            ma_data[field] = match.group(1).strip()
    data["medical_assistant_data"] = ma_data

    data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return data

# Save Results to JSON and SQLite
def save_results(data, method="EasyOCR"):
    json_file = f"ocr_{method.lower()}_results.json"
    with open(json_file, "w") as f:
        json.dump(data, f, indent=4)

    conn = sqlite3.connect(f"ocr_{method.lower()}_results.db")
    conn.execute("CREATE TABLE IF NOT EXISTS patients (id INTEGER PRIMARY KEY, name TEXT, dob TEXT)")
    conn.execute("CREATE TABLE IF NOT EXISTS forms_data (id INTEGER PRIMARY KEY, patient_id INTEGER, form_json TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")

    patient_data = (data['patient_name'], data['dob'])
    conn.execute("INSERT INTO patients (name, dob) VALUES (?, ?)", patient_data)
    patient_id = conn.lastrowid

    form_data = json.dumps(data)
    conn.execute("INSERT INTO forms_data (patient_id, form_json) VALUES (?, ?)", (patient_id, form_data))
    conn.commit()
    conn.close()

image_path = "C:\\Users\\hp\\Desktop\\image1.png"  #  change  image path as per requirement
print("Extracting text using EasyOCR...")
text = extract_text(image_path)
data = extract_data(text)
save_results(data, "EasyOCR")
print("\nExtracted Data:")
print(json.dumps(data, indent=4))
