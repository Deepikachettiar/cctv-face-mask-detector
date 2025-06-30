from flask import Flask,render_template,Response,jsonify
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///project.db"
db=SQLAlchemy(app)

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    """Video streaming route"""
    return Response(generate_frames(),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start_detection')
def start_detection():
    """Start face mask detection"""
    global detection_active
    detection_active = True
    return jsonify({"status": "Detection started"})

@app.route('/stop_detection')
def stop_detection():
    """Stop face mask detection"""
    global detection_active
    detection_active = False
    return jsonify({"status": "Detection stopped"})

@app.route('/camera_status')
def camera_status():
    """Check camera status"""
    camera = get_camera()
    if camera and camera.isOpened():
        return jsonify({"status": "Camera connected"})
    else:
        return jsonify({"status": "Camera not available"})

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    print("Starting Face Mask Detection Web App...")
    print("Make sure you have created the HTML template in templates/index.html")
    app.run(debug=True, host='0.0.0.0', port=5000)
