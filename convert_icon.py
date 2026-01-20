from PIL import Image
import os

img_path = r'e:\My Projects\file_deletion_management\assets\icon.png'
ico_path = r'e:\My Projects\file_deletion_management\assets\icon.ico'

if os.path.exists(img_path):
    img = Image.open(img_path)
    # Resize and save as ico
    icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    img.save(ico_path, sizes=icon_sizes)
    print(f"Converted {img_path} to {ico_path}")
else:
    print("Source image not found.")
