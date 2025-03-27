from flask import Flask, render_template, Response
from capture_and_downscale import generate_frames
import cv2

app = Flask(__name__)
stream_active = False
camera = None

def init_camera():
    global camera
    if camera is None:
        camera = cv2.VideoCapture(0)
    return camera

def generate_lr():
    camera = init_camera()
    while True:
        ret, frame = camera.read()
        if not ret:
            break
        
        # Generate LR frame
        h, w, _ = frame.shape
        lr_frame = cv2.resize(frame, (w//2, h//2), interpolation=cv2.INTER_CUBIC)
        
        # Convert to jpg format
        _, buffer = cv2.imencode('.jpg', lr_frame)
        frame_bytes = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

def generate_hr():
    camera = init_camera()
    while True:
        ret, frame = camera.read()
        if not ret:
            break
        
        # Convert to jpg format
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.get("/")
def home_page():
    return render_template("live section with start stop.html")

@app.route('/video_feed_lr')
def video_feed_lr():
    return Response(generate_lr(),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed_hr')
def video_feed_hr():
    return Response(generate_hr(),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start_stream', methods=['POST'])
def start_stream():
    global stream_active
    stream_active = True
    return '', 204

@app.route('/stop_stream', methods=['POST'])
def stop_stream():
    global stream_active
    stream_active = False
    return '', 204

if __name__=='__main__':
    app.run(debug=True)