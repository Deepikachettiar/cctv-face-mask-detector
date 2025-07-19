from flask import Flask, render_template, Response, jsonify,request

import os
from datetime import datetime

app = Flask(__name__)
uploadf='static/uploads/'
app.config['uploadf'] = uploadf
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

os.makedirs(uploadf, exist_ok=True)
detection_active = False
current_imgpath = None

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    #main page
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    global current_imgpath
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400


    if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Please upload PNG, JPG, JPEG, GIF, or WebP files.'}), 400
        
        
    if file:
        filename = secure_filename(file.filename)
        uname = f"{uuid.uuid4().hex}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], uname)
        file.save(filepath)
        return jsonify({
                'success': True,
                'message': 'File uploaded successfully',
                'filepath': filepath,
                'filename': uname
            })
    
    return jsonify({'error':f'upload failed:{str(e)}'}),500


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
