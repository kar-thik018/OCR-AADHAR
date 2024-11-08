from flask import Flask, request, render_template
from flask_cors import CORS
import easyocr
import numpy as np
import cv2  # Import OpenCV for image handling
from ocr_core import *

# Initialize Flask app and EasyOCR reader
app = Flask(__name__)
CORS(app)
reader = easyocr.Reader(['en'])

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Function to check file extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('upload.html', msg='No file selected')
        
        file = request.files['file']
        if file.filename == '':
            return render_template('upload.html', msg='No file selected')

        if file and allowed_file(file.filename):
            # Read the image data
            image_bytes = file.read()
            image_array = np.frombuffer(image_bytes, np.uint8)
            image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

            # Check if the image was loaded properly
            if image is None:
                return render_template('upload.html', msg='Failed to load image')
            r1= front_data(image)

            # Use EasyOCR to extract text
            results = reader.readtext(image)

            # Extract text from the results
            extracted_text = " ".join([text for _, text, _ in results])

            return render_template(
                'upload.html',
                msg='Successfully processed',
                extracted_text=extracted_text,
                r1=r1
            )
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
