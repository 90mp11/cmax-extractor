import os
import FIPExtractor.DirectoryWalker as DirectoryWalker
import FIPExtractor.FileHandler as FileHandler
import FIPExtractor.ImageExtractor as ImageExtractor

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
