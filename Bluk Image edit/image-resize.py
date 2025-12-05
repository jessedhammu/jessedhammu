from PIL import Image
import os
import io 

# Input folder containing your JPG image files
input_folder = 'C:/Users/rupin/Desktop/photograph'

# Output folder where resized images will be saved
output_folder = 'C:/Users/rupin/Desktop/resized'

# Target file size in bytes (e.g., 200 KB)
target_size = 100 * 1024  # 100 KB in bytes

def resize_image(input_path, output_path, target_size):
    image = Image.open(input_path)

    # Compress the image until it's close to the target size
    quality = 70  # Initial quality value
    while True:
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG", quality=quality)
        image_size = buffer.tell()
        if image_size <= target_size or quality <= 10:
            break
        quality -= 10  # Reduce quality by 10 and try again

    # Save the compressed image
    image.save(output_path, format="JPEG", quality=quality)

def main():
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(".jpg") or filename.endswith(".JPG"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            resize_image(input_path, output_path, target_size)
            print(f"Resized: {filename}")

if __name__ == "__main__":
    main()
