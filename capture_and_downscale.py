import cv2
import os
# from tqdm import tqdm

os.makedirs("HR", exist_ok=True)
os.makedirs("LR", exist_ok=True)

def generate_frames(camera_index=0, downscale_factor=5):
    cap = cv2.VideoCapture(camera_index)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        # Generate LR frame
        h, w, _ = frame.shape
        lr_frame = cv2.resize(frame, (w//downscale_factor, h//downscale_factor), interpolation=cv2.INTER_CUBIC)
        
        # Convert frames to jpg format
        _, lr_buffer = cv2.imencode('.jpg', lr_frame)
        _, hr_buffer = cv2.imencode('.jpg', frame)
        
        lr_frame_bytes = lr_buffer.tobytes()
        hr_frame_bytes = hr_buffer.tobytes()
        
        yield (lr_frame_bytes, hr_frame_bytes)

def capture_and_downscale(camera_index=0, downscale_factor=3, num_frames=300):
    cap = cv2.VideoCapture(camera_index)
    frame_count = 0
    
    print("Capturing frames... Press 'q' to stop.")
    while frame_count < num_frames:
        ret, frame = cap.read()
        if not ret:
            print("Camera disconnected or no frame captured.")
            break

        # Save HR frame
        hr_frame_path = f"HR/frame_{frame_count:04d}.png"
        cv2.imwrite(hr_frame_path, frame)
        
        h, w, _ = frame.shape
        lr_frame = cv2.resize(frame, (w//downscale_factor, h//downscale_factor), interpolation=cv2.INTER_NEAREST)
        lr_frame_path = f"LR/frame_{frame_count:04d}.png"
        cv2.imwrite(lr_frame_path, lr_frame)

        frame_count += 1
        cv2.imshow("Low Resolution", lr_frame)
        # resized_hr = cv2.resize(hr_frame, (w//2, h//2))  # Reduce window size by half
        # reading from hr folder
        hr_frame = cv2.imread(hr_frame_path)
        cv2.imshow("High Resolution",hr_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    print(f"Captured {frame_count} frames. Saved in 'HR' and 'LR' folders.")
if __name__=="__main__":
    # different_downscaling()
    capture_and_downscale()
# from flask import Flask, request, send_file
# from io import BytesIO
# # from some_esrgan_library import enhance_image_function  # Replace with actual ESRGAN library

# app = Flask(__name__)

# @app.route('/enhance-image', methods=['POST'])
# def enhance_image():
#     if 'file' not in request.files:
#         return 'No file part', 400
#     file = request.files['file']
#     if file.filename == '':
#         return 'No selected file', 400

#     enhanced_image = enhance_image_function(file)

#     img_io = BytesIO()
#     enhanced_image.save(img_io, 'PNG')
#     img_io.seek(0)
#     return send_file(img_io, mimetype='image/png')

# if __name__ == "__main__":
#     app.run(debug=True, port=5000)
