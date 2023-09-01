import os
from PIL import Image
import io
import zipfile

# Function 
# Modifying the main function to include logic for handling .zip files
def main():
    folder_path = "./raw"
    temp_folder = "./temp"
    output_path = "./output"
    
    # Create temp folder if it doesn't exist
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)
    
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        
        # If the file is a .zip file, handle it
        if file_name.lower().endswith('.zip'):
            handle_zip_file(file_path, temp_folder)
            folder_to_process = temp_folder
        else:
            folder_to_process = folder_path
        
        extract_second_png_from_cmax_files(folder_to_process, output_path)
    
    # Cleanup: Remove temporary files
#    if os.path.exists(temp_folder):
#        for file_name in os.listdir(temp_folder):
#            file_path = os.path.join(temp_folder, file_name)
#            os.remove(file_path)


def handle_zip_file(zip_file_path, temp_folder):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        # Filtering out .cmax2 files from the archive
        cmax2_files = [file for file in zip_ref.namelist() if file.lower().endswith('.cmax2')]
        
        # Extracting .cmax2 files to the temporary folder
        for file in cmax2_files:
            zip_ref.extract(file, temp_folder)


def extract_image(binary_data, start_pos, image_type):
    if image_type == 'JPEG':
        end_pos = binary_data.find(b'\xFF\xD9', start_pos) + 2
    elif image_type == 'PNG':
        end_pos = binary_data.find(b'\x49\x45\x4E\x44', start_pos) + 4 + 4  # IEND + CRC
    else:
        return None
    
    image_data = binary_data[start_pos:end_pos]
    image = Image.open(io.BytesIO(image_data))
    return image, image_data

def extract_second_png_from_cmax_files(folder_path, output_path):
    image_headers = {
        'PNG': b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'
    }
    
    saved_png_paths = {}
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            if filename.endswith('.cmax2'):
                file_path = os.path.join(root, filename)
                
                with open(file_path, 'rb') as file:
                    binary_data = file.read()
                
                png_positions = []
                search_start_pos = 0
                while True:
                    pos = binary_data.find(image_headers['PNG'], search_start_pos)
                    if pos == -1:
                        break
                    png_positions.append(pos)
                    search_start_pos = pos + 1
                
                if len(png_positions) < 2:
                    saved_png_paths[filename] = 'Less than two PNG images found'
                    continue
                
                try:
                    image, _ = extract_image(binary_data, png_positions[1], 'PNG')
                    save_path = os.path.join(output_path, f'{filename}.png')
                    image.save(save_path)
                    saved_png_paths[filename] = save_path
                except Exception as e:
                    saved_png_paths[filename] = str(e)
                
    return saved_png_paths

if __name__ == "__main__":
    main()