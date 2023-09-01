import os
from PIL import Image
import io

def main():
    folder_path = "./raw"
    output_path = "./output"
    print(extract_second_png_from_cmax_files(folder_path, output_path))

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
    for filename in os.listdir(folder_path):
        if filename.endswith('.cmax2'):
            file_path = os.path.join(folder_path, filename)
            
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