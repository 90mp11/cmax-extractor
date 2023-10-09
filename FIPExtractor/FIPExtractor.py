import os
from PIL import Image
import io
import zipfile

class FileHandler:
    @staticmethod
    def read_binary_file(file_path):
        try:
            with open(file_path, 'rb') as file:
                return file.read()
        except Exception as e:
            return None, str(e)
        
    @staticmethod
    def write_image(image, save_path):
        try:
            image.save(save_path)
            return save_path
        except Exception as e:
            return None, str(e)

    @staticmethod
    def unzip_files(zip_file_path, temp_folder):
        try:
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                cmax2_files = [file for file in zip_ref.namelist() if file.lower().endswith('.cmax2')]
                for file in cmax2_files:
                    zip_ref.extract(file, temp_folder)
            return True, None
        except Exception as e:
            return False, str(e)


# ImageExtractor Class for image extraction logic
class ImageExtractor:
    @staticmethod
    def extract_image(binary_data, start_pos, image_type):
        if image_type == 'PNG':
            end_pos = binary_data.find(b'\x49\x45\x4E\x44', start_pos) + 4 + 4  # IEND + CRC
        else:
            return None, 'Unsupported image type'
        
        image_data = binary_data[start_pos:end_pos]
        image = Image.open(io.BytesIO(image_data))
        return image, None


# DirectoryWalker Class for directory traversal
class DirectoryWalker:
    @staticmethod
    def find_eligible_files(folder_path, file_extension):
        eligible_files = []
        for root, _, files in os.walk(folder_path):
            for filename in files:
                if filename.lower().endswith(file_extension):
                    eligible_files.append(os.path.join(root, filename))
        return eligible_files


# Main Coordinator Class (Refactored FIPExtractor)
class FIPExtractor:
    def __init__(self, folder_path='./raw', temp_folder='./temp', output_path='./output'):
        self.folder_path = folder_path
        self.temp_folder = temp_folder
        self.output_path = output_path

    def extract_second_png_from_single_file(self, file_path):
        binary_data, err = FileHandler.read_binary_file(file_path)
        if err:
            return None, err

        # Search for PNG headers
        image_headers = {'PNG': b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'}
        png_positions = []
        search_start_pos = 0
        while True:
            pos = binary_data.find(image_headers['PNG'], search_start_pos)
            if pos == -1:
                break
            png_positions.append(pos)
            search_start_pos = pos + 1

        if len(png_positions) < 2:
            return None, 'Less than two PNG images found'

        image, err = ImageExtractor.extract_image(binary_data, png_positions[1], 'PNG')
        if err:
            return None, err

        filename = os.path.basename(file_path)
        save_path = os.path.join(self.output_path, f'{filename}.png')
        return FileHandler.write_image(image, save_path)

    def extract_second_png_from_cmax_files(self):
        cmax2_files = DirectoryWalker.find_eligible_files(self.folder_path, '.cmax2')
        zip_files = DirectoryWalker.find_eligible_files(self.folder_path, '.zip')

        # Handle zip files
        for zip_file in zip_files:
            FileHandler.unzip_files(zip_file, self.temp_folder)

        saved_png_paths = {}
        for file_path in cmax2_files:
            save_path, err = self.extract_second_png_from_single_file(file_path)
            if err:
                saved_png_paths[file_path] = err
            else:
                saved_png_paths[file_path] = save_path

        return saved_png_paths

# Test the improved class (Not executable here but for demonstration)
if __name__ == '__main__':
    extractor = FIPExtractor()
    print(extractor.extract_second_png_from_single_file("./some_file.cmax2"))
    print(extractor.extract_second_png_from_cmax_files(folder_path="./raw/"))
