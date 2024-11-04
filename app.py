from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from PIL import Image
import pytesseract
from flask_cors import CORS
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Make sure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Configure Tesseract path (Update this with your Tesseract installation path)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_details(image_path):
    text = pytesseract.image_to_string(Image.open(image_path))
    name, age, other_details = None, None, {}

    lines = text.splitlines()
    for line in lines:
        if "Name" in line:
            name = line.split(":")[-1].strip()
        if "Age" in line or "DOB" in line:
            age = line.split(":")[-1].strip()

    other_details = {'Name': name, 'Age/DOB': age}
    return other_details

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        details = extract_details(file_path)
        return f"Extracted Details: {details}"

if __name__ == '__main__':
    app.run()
    