import cv2
import numpy as np
import os

def modcrop(img, modulo):
    """Crop the image so that each dimension is divisible by `modulo`."""
    h, w = img.shape[:2]
    h = h - (h % modulo)
    w = w - (w % modulo)
    return img[:h, :w]

def process_camera_frame(frame, up_scale=4, mod_scale=4):
    """
    Process a single frame: crop and downscale.

    Parameters:
    - frame: Input image frame from the camera.
    - up_scale: Downscaling factor.
    - mod_scale: Modulo value for cropping.
    """
    # Normalize and crop
    frame = frame / 255.0  # Normalize to [0, 1]
    frame = modcrop(frame, mod_scale)

    # Downscale using bicubic interpolation
    h, w = frame.shape[:2]
    new_h, new_w = h // up_scale, w // up_scale
    frame_LR = cv2.resize(frame, (new_w, new_h), interpolation=cv2.INTER_CUBIC)

    # Convert back to [0, 255]
    frame_LR = (frame_LR * 255.0).astype(np.uint8)
    return frame_LR

def capture_and_process(output_dir, up_scale=4, mod_scale=4):
    """
    Capture images from the camera, downscale, and display them in separate windows.

    Parameters:
    - output_dir: Path to save downscaled images.
    - up_scale: Downscaling factor.
    - mod_scale: Modulo value for cropping.
    """
    cap = cv2.VideoCapture(0)  # Open the default camera
    if not cap.isOpened():
        print("Error: Unable to access the camera.")
        return

    idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame. Exiting...")
            break

        # Process the frame
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB
        frame_LR = process_camera_frame(frame, up_scale, mod_scale)

        # Show the original and downscaled frame in separate windows
        cv2.imshow("Original Frame", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))  # Original frame
        cv2.imshow("Downscaled Frame", cv2.cvtColor(frame_LR, cv2.COLOR_RGB2BGR))  # Downscaled frame

        # Save the downscaled frame
        save_path = os.path.join(output_dir, f"frame_{idx:04d}.png")
        os.makedirs(output_dir, exist_ok=True)
        cv2.imwrite(save_path, cv2.cvtColor(frame_LR, cv2.COLOR_RGB2BGR))
        print(f"Saved downscaled frame: {save_path}")

        idx += 1

        # Exit loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Example usage
output_directory = "./LR"
capture_and_process(output_directory)
