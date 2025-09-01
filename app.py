import os
import subprocess
from flask import Flask, request, send_file
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = '/app/uploads'
OUTPUT_FOLDER = '/app/outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def home():
    return "hello world!"


    


@app.route('/convert', methods=['POST'])
def convert_pdf():
    # Handle file upload
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    if file and file.filename.endswith('.pdf'):
        filename = secure_filename(file.filename)
        input_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(input_path)

        # Run Audiveris command-line tool
        try:
            output_filename = os.path.splitext(filename)[0] + '.mxl'
            output_path = os.path.join(OUTPUT_FOLDER, output_filename)
            subprocess.run([
                '/audiveris/Audiveris-5.3-alpha/bin/Audiveris',
                '-batch',
                '-export',
                '-output', OUTPUT_FOLDER,
                input_path
            ], check=True)

            return send_file(output_path, as_attachment=True)
        except subprocess.CalledProcessError as e:
            return f"Audiveris conversion failed: {e}", 500
    return "Invalid file format. Please upload a PDF.", 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
