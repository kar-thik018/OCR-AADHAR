# try:  
from PIL import Image
# except ImportError:  
# import Image
import pytesseract

def ocr_core(filename):  
    """
    This function will handle the core OCR processing of images.
    """
    text = pytesseract.image_to_string(Image.open(filename))  # We'll use Pillow's Image class to open the image and pytesseract to detect the string in the image
    return text

import easyocr
import re
import spacy

# Initialize EasyOCR reader and spaCy NER
reader = easyocr.Reader(['en'])
NER = spacy.load("en_core_web_sm")

def front_data(img):
    regex_name = None
    regex_gender = None
    regex_dob = None
    regex_aadhaar_number = None

    # Use EasyOCR to extract text from the image
    result = reader.readtext(img, detail=0)
    res_string_name = " ".join(result)

    # Extracting name using Named Entity Recognition (NER)
    name = NER(res_string_name)
    for word in name.ents:
        if word.label_ == "PERSON":
            regex_name = re.findall("[A-Z][a-z]+", word.text)

    if not regex_name:
        regex_name = re.findall("[A-Z][a-z]+", res_string_name)

    # Extracting information other than name
    # Use EasyOCR to get all text for gender, dob, aadhaar number extraction
    result_else = reader.readtext(img, detail=0)
    res_string_else = " ".join(result_else)

    if not regex_name:
        regex_name = re.findall("[A-Z][a-z]+", res_string_else)

    # Extracting gender
    regex_gender = re.findall(r"\b(MALE|FEMALE|male|female)\b", res_string_else)
    if regex_gender:
        regex_gender = regex_gender[0]

    # Extracting date of birth (DOB)
    regex_dob = re.findall(r"\b\d{2}/\d{2}/\d{4}\b", res_string_else)
    if regex_dob:
        regex_dob = regex_dob[0]

    # Extracting Aadhaar number
    regex_aadhaar_number = re.findall(r"\b\d{4}\s\d{4}\s\d{4}\b", res_string_else)
    if regex_aadhaar_number:
        regex_aadhaar_number = regex_aadhaar_number[0]

    return (regex_name, regex_gender, regex_dob, regex_aadhaar_number)


def back_data(img):
    # Use EasyOCR to extract text from the image
    result = reader.readtext(img, detail=0)
    ocr_text = " ".join(result)

    try:
        address_start = ocr_text.find('Address')
        if address_start == -1:
            address_start = ocr_text.find('To')
        address = ocr_text[address_start + 8:] if address_start != -1 else ocr_text
        
        pinpatn = r'[0-9]{6}'
        address_end = 0
        pinloc = re.search(pinpatn, address)

        if pinloc:
            address_end = pinloc.end()
            address = address[:address_end]
        else:
            print('Pin code not found in address')
            address = re.sub('\n', ' ', address[:address_end])
    except Exception as e:
        print(f"Error extracting address: {e}")
        address = re.sub('\n', ' ', ocr_text)
        pinloc = re.search(pinpatn, address)
    
    return address.replace("\n", "")
