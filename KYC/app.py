from flask import Flask, render_template, request, jsonify
import base64
import cv2
import pytesseract
import re
import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
import base64
import os

app = Flask(__name__)
image_count = 0

captured_info = {}

# Function to extract information from OCR text
def extract_information(text):
    # Initialize variables to store extracted information
    name = None
    dob = None
    gender = None
    aadhaar_number = None

    
    # Extract name
    '''
    name_match = re.search(r'(?<=\nafer at\n)([A-Za-z ]+)', text)
   
    if name_match:
        name = name_match.group(1).strip()
    else:
        name_match = re.search(r'a¢\s*([A-Za-z ]+)', text)
    if name_match:
        name = name_match.group(1).strip()
        '''
    #name_match = re.search(r'[A-Z][a-zA-Z ]+(?=\D)', text)
    name_match = re.search(r'[A-Z][a-zA-Z]{3,}(?: [A-Z][a-zA-Z]{3,})?(?=\D)', text)
    if name_match:
        name = name_match.group(0).strip()
    # Extract date of birth (DOB)
    dob_match = re.search(r'\b(\d{2}/\d{2}/\d{4})\b', text)
    if dob_match:
        dob = dob_match.group(0).strip()

    # Extract gender
    gender_match = re.search(r'(Male|Female)', text, re.IGNORECASE)
    if gender_match:
        gender = gender_match.group(0).upper()

    # Extract Aadhaar number
    aadhaar_match = re.search(r'\b(\d{4} \d{4} \d{4})\b', text)
    if aadhaar_match:
        aadhaar_number = aadhaar_match.group(0)

    return name, dob, gender, aadhaar_number

# Function to process the image and perform OCR

def process_image(image_path):
    # Read the image
    global captured_info
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Perform thresholding to preprocess the image (adjust threshold values as needed)
    _, threshold_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # Perform OCR (change configuration as needed)
    config = '--psm 6'  # Assume a single uniform block of text
    text = pytesseract.image_to_string(threshold_image, config=config)

    # Extract information from the OCR text
    name, dob, gender, aadhaar_number = extract_information(text)
    print(text)
    captured_info = {
        'name': name,
        'dob': dob,
        'gender': gender,
        'aadhaar_number': aadhaar_number
    }

    return name, dob, gender, aadhaar_number

def get_captured_images():
    image_folder = 'photos'  # Update with your actual folder name
    if os.path.exists(image_folder):
        return [filename for filename in os.listdir(image_folder) if filename.endswith(('.jpg', '.png'))]
    else:
        return []

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/index')
def get_started():
    return render_template('index.html')

@app.route('/last.html')
def last():
    return render_template('last.html')


@app.route('/save_image', methods=['POST'])
def save_image():
    global image_count
    data_url = request.form['image']
    encoded_image = data_url.split(',')[1]
    decoded_image = base64.b64decode(encoded_image)

    if not os.path.exists('photos'):
        os.makedirs('photos')

    image_count += 1
    if image_count == 1:
        filename = 'dp.jpg'
    elif image_count == 2:
        filename = 'id.jpg'
    else:
        filename = f'default.jpg'

    with open(f'photos/{filename}', 'wb') as f:
        f.write(decoded_image)

    name, dob, gender, aadhaar_number = process_image(f'photos/{filename}')

    print("Name:", name)
    print("Date of Birth (DOB):", dob)
    print("Gender:", gender)
    print("Aadhaar Number:", aadhaar_number)

    return jsonify({'message': 'Image saved successfully', 'name': name, 'dob': dob, 'gender': gender, 'aadhaar_number': aadhaar_number, 'image_filename': filename})

@app.route('/display_info')
def display_info():
    global captured_info
    captured_info['images'] = get_captured_images()
    return render_template('display_info.html', captured_info=captured_info)

if __name__ == '__main__':
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    app.run(debug=True)