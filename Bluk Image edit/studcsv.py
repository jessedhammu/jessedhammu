import os
import csv
import requests

def download_images(csv_filename, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with open(csv_filename, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip the header row if present

        for row in csv_reader:
            image_url = row[0]
            image_name = os.path.basename(image_url)
            image_path = os.path.join(output_folder, image_name)

            try:
                response = requests.get(image_url, stream=True)
                response.raise_for_status()
                
                with open(image_path, 'wb') as image_file:
                    for chunk in response.iter_content(chunk_size=8192):
                        image_file.write(chunk)
                
                print(f"Downloaded: {image_url}")
            except Exception as e:
                print(f"Failed to download {image_url}: {e}")

if __name__ == "__main__":
    csv_filename = "C:/Users/rupin/Desktop/stud.csv"  # Replace with your CSV filename
    output_folder = "C:/Users/rupin/Desktop/stud"  # Replace with the folder where you want to save images
    download_images(csv_filename, output_folder)