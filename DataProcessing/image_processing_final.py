from PIL import Image, ImageOps
import os

# Define the directory and target size
image_folder_small = 'image_folder'
target_size = (224, 224)

# Iterate over all subfolders and images in image_folder_small
for root, _, files in os.walk(image_folder_small):
    for file in files:
        if file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff')):
            image_path = os.path.join(root, file)
            with Image.open(image_path) as img:
                # Convert to RGB if the image is in a different mode
                if img.mode != 'RGB':
                    img = img.convert('RGB')

                # Ensure pixel values are in the 0-255 range
                extrema = img.getextrema()
                if any(ext[1] <= 1 for ext in extrema) and all(ext[1] <= 1 for ext in extrema):  # If all values are in 0-1 range
                    img = img.point(lambda x: x * 255)  # Scale up to 0-255 range

                # Use ImageOps.fit to resize and center-crop the image
                img_resized = ImageOps.fit(img, target_size, Image.LANCZOS)

                # Save the resized image back to the same location
                img_resized.save(image_path)