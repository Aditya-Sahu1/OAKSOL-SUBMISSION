OCR Text Extraction 

Overview
This guide outlines the steps to set up and execute Optical Character Recognition (OCR) workflows using two different OCR tools: Tesseract OCR and EasyOCR. The goal is to extract text from an image, process it, and save the output in both JSON and SQLite formats.

The scripts provided in this document will help automate the text extraction process and ensure smooth execution, especially on a Windows system.

Prerequisites
1.Python Installation: Ensure that Python is installed on your system. You can check the installed version with the following command:
python --version

If Python is not installed, download it from python.org.
During installation, make sure to check the box to "Add Python to PATH".

2.Required Python Libraries: Install the necessary libraries by running the following command:
pip install opencv-python pytesseract easyocr numpy pillow sqlite3

3.Tesseract Installation: Tesseract is required for extracting text using the Tesseract OCR script. To install Tesseract:

Download Tesseract from https://github.com/UB-Mannheim/tesseract/wiki.
During installation, note the directory where Tesseract is installed, as you'll need to specify this directory in the Python script.
Add Tesseract to PATH (if not already done during installation):

Navigate to System Properties > Environment Variables.
Under System variables, find the Path variable and click Edit.
Add the path to the Tesseract directory (e.g., C:\Program Files\Tesseract-OCR).
If you do not want to modify the system PATH, specify the Tesseract path directly in the Python code.

Image Path Configuration
In both scripts, you need to specify the path to your image file (the image from which text will be extracted).

For example:

image_path = "C:\\Users\\hp\\Desktop\\image1.png" 
Replace "C:\\Users\\hp\\Desktop\\image1.png" with the actual path to your image.

Ensure that the image file is in a readable format (e.g., PNG, JPG) and is placed in an accessible folder.

Method 1: EasyOCR-based Text Extraction
Key Steps:
Image Path: Set image_path to the location of your image.
Preprocessing: The image is preprocessed (grayscale and blurred) before OCR.
OCR Execution: EasyOCR is used to extract text from the processed image.
Result Saving: The extracted text is saved in both JSON and SQLite formats.

Method 2: Tesseract OCR-based Text Extraction

Key Steps:
Image Path: Set image_path to the location of your image.
Preprocessing: The image is preprocessed (grayscale, blurred, and thresholded) before OCR.
OCR Execution: Tesseract OCR is used to extract text from the preprocessed image.
Result Saving: The extracted text is saved in both JSON and SQLite formats.
Tesseract Path Configuration:
If Tesseract is installed but not added to PATH, specify its path directly in the code by uncommenting the following line and modifying the path as required:

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
Conclusion
By following the steps outlined above, you can efficiently extract text from images using either Tesseract OCR or EasyOCR on a Windows system. Ensure that the image path is correctly set and that all necessary dependencies, including Tesseract, are properly installed. The extracted text is saved in both JSON and SQLite formats for easy access and storage.







