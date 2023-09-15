import os
import random
from shutil import copyfile
from PIL import Image, ImageEnhance

# Define the input and output directories
input_dir = "dataset/Data"
output_dir = "dataset/output"

# Define the target range for the number of images per folder
min_images_per_folder = 900
max_images_per_folder = 1000

# Define the augmentation operations (you can customize this)
def augment_image(input_path, output_path):
    try:
        image = Image.open(input_path)

        # Example augmentations, you can customize these
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(random.uniform(0.7, 1.3))

        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(random.uniform(0.7, 1.3))

        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(random.uniform(0.7, 1.3))

        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(random.uniform(0.7, 1.3))

        image.save(output_path)
    except Exception as e:
        print(f"Error processing image: {input_path}, Error: {str(e)}")

# Function to perform augmentations
def augment_images(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    # List image files in the input folder
    image_files = [f for f in os.listdir(input_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]

    # Calculate the number of images to generate
    num_images_to_generate = random.randint(min_images_per_folder, max_images_per_folder)

    # Check if there are images in the folder before attempting augmentation
    if len(image_files) == 0:
        print(f"No images found in folder: {input_folder}")
        return

    for i in range(num_images_to_generate):
        input_image = os.path.join(input_folder, random.choice(image_files))
        output_image = os.path.join(output_folder, f"augmented_{i}.jpg")
        augment_image(input_image, output_image)

# Iterate through subfolders in the input directory
for root, _, _ in os.walk(input_dir):
    # Skip the root directory itself
    if root == input_dir:
        continue

    # Extract the subfolder name
    subfolder_name = os.path.relpath(root, input_dir)

    # Create the corresponding output subfolder
    output_subfolder = os.path.join(output_dir, subfolder_name)

    # Augment images for this subfolder
    augment_images(root, output_subfolder)

print("Augmentation and image resizing completed.")
