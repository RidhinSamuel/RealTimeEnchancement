from flask import Flask, render_template, Response, request, send_file
from capture_and_downscale import capture_and_downscale, generate_frames
from werkzeug.utils import secure_filename
from test import image_upscaling
import os
app=Flask(__name__)
app.config['UPLOAD_FOLDER']='LR'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def generate_lr():
    for lr_frame, _ in generate_frames():
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + lr_frame + b'\r\n')

def generate_hr():
    for _, hr_frame in generate_frames():
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + hr_frame + b'\r\n')
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#takes image and upscaled and return it
@app.route('/photo', methods=['POST'])
def upload_photo():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    
    if file.filename == '':
        return 'No selected file', 400
        
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        # return filename
    image_upscaling()
    hr_files = [f for f in os.listdir('HR') if os.path.isfile(os.path.join('HR', f))]
    if hr_files:
        latest_file = max(hr_files, key=lambda x: os.path.getctime(os.path.join('HR', x)))
        hr_filepath = os.path.join('HR', latest_file)
        if os.path.exists(hr_filepath):
            return send_file(
                hr_filepath,
                mimetype='image/png',
                as_attachment=True,
                download_name=f'enhanced_{filename}'
            )
        return 'Enhancement failed', 500
    return 'Invalid file type', 400
@app.get("/")
def home_page():
    return render_template("index.html")
@app.post("/live")
def live():
    capture_and_downscale()

# @app.route('/video_feed_lr')
# def video_feed_lr():
#     return Response(generate_lr(),
#                    mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/video_feed_hr')
# def video_feed_hr():
#     return Response(generate_hr(),
#                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__=='__main__':
    app.run(debug=True)