import cv2
import os
# from tqdm import tqdm

os.makedirs("HR", exist_ok=True)
os.makedirs("LR", exist_ok=True)

def capture_and_downscale(camera_index=0, downscale_factor=4, num_frames=300):
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
        lr_frame = cv2.resize(frame, (w // downscale_factor, h // downscale_factor), interpolation=cv2.INTER_CUBIC)
        lr_frame_path = f"LR/frame_{frame_count:04d}.png"
        cv2.imwrite(lr_frame_path, lr_frame)

        frame_count += 1

        cv2.imshow("Low Resolution", lr_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"Captured {frame_count} frames. Saved in 'HR' and 'LR' folders.")

capture_and_downscale()

from flask import Flask, request, send_file
from io import BytesIO
# from some_esrgan_library import enhance_image_function  # Replace with actual ESRGAN library

app = Flask(__name__)

@app.route('/enhance-image', methods=['POST'])
def enhance_image():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400

    enhanced_image = enhance_image_function(file)

    img_io = BytesIO()
    enhanced_image.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')
import cv2
import os

# Ensure "results" folder exists
os.makedirs("results", exist_ok=True)

# Define output video file name and FPS
output_video_path = "results/combined_video.mp4"
fps = 30  # Adjust as needed

# Get list of HR and LR frames and sort them
hr_frames = sorted([f for f in os.listdir("HR") if f.endswith(".png")])
lr_frames = sorted([f for f in os.listdir("LR") if f.endswith(".png")])

if not hr_frames or not lr_frames:
    print("Error: HR or LR frames not found!")
    exit()

# Read the first frame to determine dimensions
first_hr = cv2.imread(os.path.join("HR", hr_frames[0]))
first_lr = cv2.imread(os.path.join("LR", lr_frames[0]))

hr_height, hr_width, _ = first_hr.shape
lr_height, lr_width, _ = first_lr.shape

# Resize LR to match HR height (keep aspect ratio)
scale_factor = hr_height / lr_height
new_lr_width = int(lr_width * scale_factor)
lr_resized = cv2.resize(first_lr, (new_lr_width, hr_height), interpolation=cv2.INTER_CUBIC)

# Define video writer
combined_width = new_lr_width + hr_width
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Or 'XVID' for AVI format
out = cv2.VideoWriter(output_video_path, fourcc, fps, (combined_width, hr_height))

print("Generating combined video...")

# Iterate over frames
for lr_name, hr_name in zip(lr_frames, hr_frames):
    lr_frame = cv2.imread(os.path.join("LR", lr_name))
    hr_frame = cv2.imread(os.path.join("HR", hr_name))

    # Resize LR to match HR height
    lr_resized = cv2.resize(lr_frame, (new_lr_width, hr_height), interpolation=cv2.INTER_CUBIC)

    # Concatenate images side by side
    combined_frame = cv2.hconcat([lr_resized, hr_frame])

    # Write to video
    out.write(combined_frame)

    # Display the combined frame
    cv2.imshow("LR vs HR Video", combined_frame)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

out.release()
cv2.destroyAllWindows()
print(f"Combined video saved in {output_video_path}")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
