from flask import Flask, render_template, Response, jsonify,request

import os
from datetime import datetime
import uuid
from werkzeug.utils import secure_filename




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

@app.route('detect',methods=['POST'])
def detect():
    global current_imgpath
    try:
        if not current_imgpath or not os.path.exists(current_imgpath):
            return jsonify({'error':'No image found.Please upload an image first.'}),400
        
        import random
        
        with_mask = random.randint(1, 15)
        without_mask = random.randint(0, 8)
        total_people = with_mask + without_mask
        confidence=random.uniform(0.85,0.99)
        
        results = {
            'success': True,
            'results': {
                'with_mask': with_mask,
                'without_mask': without_mask,
                'total_people': total_people,
                'confidence': round(confidence, 2)
            },
            'image_path': current_imgpath,
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(results)
        
    except Exception as e:
        return jsonify({'error': f'Detection failed: {str(e)}'}), 500
    


@app.route('/start_detection')
def start_detection():
    #Start face mask detection
    global detection_active
    detection_active = True
    return jsonify({"status": "Detection started",
        "active": detection_active,
        "timestamp": datetime.now().isoformat()})

@app.route('/stop_detection')
def stop_detection():
    #Stop face mask detection
    global detection_active
    detection_active = False
    return jsonify({ "status": "Detection stopped",
        "active": detection_active,
        "timestamp": datetime.now().isoformat()})


@app.route('/clear_uploads')
def clear_uploads():
    global current_image_path
    
    try:
        for filename in os.listdir(uploadf):
            file_path = os.path.join(uploadf, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
        
        current_image_path = None
        
        return jsonify({
            "status": "Uploads cleared",
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': f'Clear failed: {str(e)}'}), 500
    
@app.errorhandler(413)
def too_large(e):
    return jsonify({'error': 'File too large. Maximum size is 16MB.'}), 413


@app.errorhandler(404)
def not_found(e):
    return jsonify({'error':'Not found'}),404

if __name__ == '__main__':
    if not os.path.exists('templates'):
        os.makedirs('templates')
    if not os.path.exists('static'):
        os.makedirs('static')

    app.run(debug=True, port=5000)
