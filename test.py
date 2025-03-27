import os
import os.path as osp
import glob
import cv2
import numpy as np
import torch
import RRDBNet_arch as arch
<<<<<<< HEAD

# Model paths
model_path1 = 'models/RRDB_ESRGAN_x4.pth'  # ESRGAN Model
model_path2 = 'models/RRDB_PSNR_x4.pth'  # PSNR Model

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

test_img_folder = 'LR/*'
output_folder = 'results'
os.makedirs(output_folder, exist_ok=True)  # Ensure output folder exists

# Load ESRGAN model
model_esrgan = arch.RRDBNet(3, 3, 64, 23, gc=32)
model_esrgan.load_state_dict(torch.load(model_path1, map_location=device), strict=True)
model_esrgan.eval().to(device)

# Load PSNR model
model_psnr = arch.RRDBNet(3, 3, 64, 23, gc=32)
model_psnr.load_state_dict(torch.load(model_path2, map_location=device), strict=True)
model_psnr.eval().to(device)

print(f'Loaded ESRGAN model from {model_path1}')
print(f'Loaded PSNR model from {model_path2}')

# Process all images in the test folder
for idx, path in enumerate(glob.glob(test_img_folder), 1):
    base = osp.splitext(osp.basename(path))[0]
    print(f'Processing Image {idx}: {base}')

    # Read and preprocess the image
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    img = img.astype(np.float32) / 255.0  # Normalize
    img = torch.from_numpy(np.transpose(img[:, :, [2, 1, 0]], (2, 0, 1))).float().unsqueeze(0).to(device)

    with torch.no_grad():
        # Super-resolution using ESRGAN model
        output_esrgan = model_esrgan(img).cpu().squeeze().clamp_(0, 1).numpy()
        output_esrgan = np.transpose(output_esrgan[[2, 1, 0], :, :], (1, 2, 0))  # Convert to OpenCV format
        output_esrgan = (output_esrgan * 255.0).round().astype(np.uint8)
=======
from flask import Flask, request, jsonify
import base64
from PIL import Image
import io
def image_upscaling():
    model_path = 'models/RRDB_ESRGAN_x4.pth' 
    device = torch.device('cpu')
    test_img_folder = 'LR/*'
    model = arch.RRDBNet(3, 3, 64, 23, gc=32)
    model.load_state_dict(torch.load(model_path), strict=True)
    model.eval()
    model = model.to(device)
    print('Model path {:s}. \nTesting...'.format(model_path))
    idx = 0
    for path in glob.glob(test_img_folder):
        idx += 1
        base = osp.splitext(osp.basename(path))[0]
        print(idx, base)
        # read images
        img = cv2.imread(path, cv2.IMREAD_COLOR)
        img = img * 1.0 / 255
        img = torch.from_numpy(np.transpose(img[:, :, [2, 1, 0]], (2, 0, 1))).float()
        img_LR = img.unsqueeze(0)
        img_LR = img_LR.to(device)

        with torch.no_grad():
            output = model(img_LR).data.squeeze().float().cpu().clamp_(0, 1).numpy()
        output = np.transpose(output[[2, 1, 0], :, :], (1, 2, 0))
        output = (output * 255.0).round()
        cv2.imwrite('results/{:s}_rlt.png'.format(base), output)
>>>>>>> 7c15a26 (Set server)

        # Super-resolution using PSNR model
        output_psnr = model_psnr(img).cpu().squeeze().clamp_(0, 1).numpy()
        output_psnr = np.transpose(output_psnr[[2, 1, 0], :, :], (1, 2, 0))  # Convert to OpenCV format
        output_psnr = (output_psnr * 255.0).round().astype(np.uint8)

    # Save results
    cv2.imwrite(osp.join(output_folder, f'{base}_ESRGAN.png'), output_esrgan)
    cv2.imwrite(osp.join(output_folder, f'{base}_PSNR.png'), output_psnr)

    print(f'Saved results: {base}_ESRGAN.png & {base}_PSNR.png')

print("Processing complete!")
