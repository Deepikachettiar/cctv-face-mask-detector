from flask import Flask, render_template, Response, jsonify,request
import os
from datetime import datetime

app = Flask(__name__)
uploadf='static/uploads/'
app.config['uploadf'] = uploadf

os.makedirs(uploadf, exist_ok=True)

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']

    if file.filename == '':
        return 'No selected file'

    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        return f'File uploaded! <br> <img src="/{filepath}" width="300">'
    
    return 'Something went wrong'


@app.route('/start_detection')
def start_detection():
    #Start face mask detection
    global detection_active
    detection_active = True
    return jsonify({"status": "Detection started"})

@app.route('/stop_detection')
def stop_detection():
    #Stop face mask detection
    global detection_active
    detection_active = False
    return jsonify({"status": "Detection stopped"})


if __name__ == '__main__':
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    app.run(debug=True, port=5000)
