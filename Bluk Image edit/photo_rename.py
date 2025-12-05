import os
import csv

# Path to the folder containing the image files
folder_path = 'c:/Users/rupin/Desktop/rename/photos'

# Path to the CSV file with old and new names
csv_file_path = 'c:/Users/rupin/Desktop/rename/photos/rename.csv'

# Read the CSV file
with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    
    # Skip the header row if it exists
    next(csv_reader, None)
    
    for row in csv_reader:
        if len(row) >= 2:
            old_name = row[0]  # Get the old name from the first column
            new_name = row[1]  # Get the new name from the second column
            
            # Construct the full paths for the old and new image files
            old_image_path = os.path.join(folder_path, old_name + '.jpg')
            new_image_path = os.path.join(folder_path, new_name + '.jpg')
            
            try:
                # Rename the image file
                os.rename(old_image_path, new_image_path)
                print(f'Renamed {old_name}.jpg to {new_name}.jpg')
            except FileNotFoundError:
                print(f'File {old_name}.jpg not found.')
            except FileExistsError:
                print(f'File {new_name}.jpg already exists.')
        else:
            print('Invalid row in CSV:', row)