import os

def rename_images_to_uppercase(directory):
    for filename in os.listdir(directory):
        if filename.lower().endswith(".jpeg") or filename.lower().endswith(".jpg"):
            new_filename = filename.upper()
            old_path = os.path.join(directory, filename)
            new_path = os.path.join(directory, new_filename)
            
            try:
                os.rename(old_path, new_path)
                print(f"Renamed: {filename} -> {new_filename}")
            except Exception as e:
                print(f"Failed to rename {filename}: {e}")

if __name__ == "__main__":
    image_directory = "C:/Users/rupin/Desktop/stud"  # Replace with the actual path to your image directory
    rename_images_to_uppercase(image_directory)