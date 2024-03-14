import cv2
import pytesseract
import re

def extract_information(text):
    # Initialize variables to store extracted information
    name = None
    dob = None
    gender = None
    aadhaar_number = None

    # Extract name
    name_match = re.search(r'(?<=\nafer at\n)([A-Za-z ]+)', text)
    if name_match:
        name = name_match.group(1).strip()
    else:
        name_match = re.search(r'a¢\s*([A-Za-z ]+)', text)
    if name_match:
        name = name_match.group(1).strip()

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






# Path to Tesseract executable (change this to your path if necessary)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Read the image
image = cv2.imread('./photos/id.jpg')

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

# Print extracted information
print("Name:", name)
print("Date of Birth (DOB):", dob)
print("Gender:", gender)
print("Aadhaar Number:", aadhaar_number)
