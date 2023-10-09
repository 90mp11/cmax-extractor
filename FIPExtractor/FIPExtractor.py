import os
from PIL import Image
import io
import zipfile
import logging

class FIPExtractor:
    def __init__(self, folder_path='./raw', temp_folder='./temp', output_path='./output'):
        self.folder_path = folder_path
        self.temp_folder = temp_folder
        self.output_path = output_path
        logging.basicConfig(level=logging.INFO)

    def handle_zip_file(self, zip_file_path):
        logging.info(f"Handling zip file: {zip_file_path}")
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            cmax2_files = [file for file in zip_ref.namelist() if file.lower().endswith('.cmax2')]
            for file in cmax2_files:
                zip_ref.extract(file, self.temp_folder)

    def extract_image(self, binary_data, start_pos, image_type):
        if image_type == 'JPEG':
            end_pos = binary_data.find(b'\xFF\xD9', start_pos) + 2
        elif image_type == 'PNG':
            end_pos = binary_data.find(b'\x49\x45\x4E\x44', start_pos) + 4 + 4  # IEND + CRC
        else:
            return None

        image_data = binary_data[start_pos:end_pos]
        image = Image.open(io.BytesIO(image_data))
        return image, image_data

    def extract_second_png_from_single_file(self, file_path):
        logging.info(f"Extracting from single file: {file_path}")
        image_headers = {
            'PNG': b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'
        }
        try:
            with open(file_path, 'rb') as file:
                binary_data = file.read()
        except Exception as e:
            logging.error(f"Could not read the file {file_path}. Error: {str(e)}")
            return str(e)

        png_positions = []
        search_start_pos = 0
        while True:
            pos = binary_data.find(image_headers['PNG'], search_start_pos)
            if pos == -1:
                break
            png_positions.append(pos)
            search_start_pos = pos + 1

        if len(png_positions) < 2:
            logging.warning(f"Less than two PNG images found in {file_path}")
            return 'Less than two PNG images found'

        try:
            image, _ = self.extract_image(binary_data, png_positions[1], 'PNG')
            filename = os.path.basename(file_path)
            save_path = os.path.join(self.output_path, f'{filename}.png')
            image.save(save_path)
            logging.info(f"Saved image to {save_path}")
            return save_path
        except Exception as e:
            logging.error(f"Error in extracting image from {file_path}. Error: {str(e)}")
            return str(e)

    def extract_second_png_from_cmax_files(self, folder_path=None):
        folder_path = folder_path if folder_path is not None else self.folder_path

        saved_png_paths = {}
        for root, _, files in os.walk(folder_path):
            for filename in files:
                if filename.endswith('.cmax2'):
                    file_path = os.path.join(root, filename)
                    result = self.extract_second_png_from_single_file(file_path)
                    saved_png_paths[filename] = result
                elif filename.lower().endswith('.zip'):
                    zip_file_path = os.path.join(root, filename)
                    self.handle_zip_file(zip_file_path)

        return saved_png_paths

# Test the improved class (Not executable here but for demonstration)
if __name__ == '__main__':
    extractor = FIPExtractor()
    print(extractor.extract_second_png_from_single_file("./some_file.cmax2"))
    print(extractor.extract_second_png_from_cmax_files(folder_path="./raw/"))
