import os
import FIPExtractor.DirectoryWalker as DirectoryWalker
import FIPExtractor.FileHandler as FileHandler
import FIPExtractor.ImageExtractor as ImageExtractor

# Main Coordinator Class (Refactored FIPExtractor)
class FIPExtractor:
    def __init__(self, folder_path='./raw', temp_folder='temp', output_path='output'):     
        # Define the output directory based on the script's directory
        output_dir = output_path
        temp_dir = temp_folder

        # Make sure the output directory exists; if not, create it
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        self.folder_path = folder_path
        self.temp_folder = temp_dir
        self.output_path = output_dir


    def extract_second_png_from_single_file(self, file_path):
        binary_data, err = FileHandler.FileHandler.read_binary_file(file_path)
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

        image, err = ImageExtractor.ImageExtractor.extract_image(binary_data, png_positions[1], 'PNG')
        if err:
            return None, err

        filename = os.path.basename(file_path)
        save_path = os.path.normpath(os.path.join(self.output_path, f'{filename}.png'))
        return FileHandler.FileHandler.write_image(image, save_path)

    def extract_second_png_from_cmax_files(self):
        cmax2_files = DirectoryWalker.DirectoryWalker.find_eligible_files(self.folder_path, '.cmax2')
        zip_files = DirectoryWalker.DirectoryWalker.find_eligible_files(self.folder_path, '.zip')

        # Handle zip files
        for zip_file in zip_files:
            FileHandler.FileHandler.unzip_files(zip_file, self.temp_folder)

        # Search for new .cmax2 files in temp_folder after unzipping
        unzipped_cmax2_files = DirectoryWalker.DirectoryWalker.find_eligible_files(self.temp_folder, '.cmax2')
        
        # Extend the original cmax2_files list with the new files
        cmax2_files.extend(unzipped_cmax2_files)

        saved_png_paths = []
        for file_path in cmax2_files:
            save_path, err = self.extract_second_png_from_single_file(file_path)
            if err:
                break
            else:
                saved_png_paths.append(save_path)

        #cleanup the temp_folder
        DirectoryWalker.DirectoryWalker.delete_folder_contents(self.temp_folder)
        
        return saved_png_paths

# Test the improved class (Not executable here but for demonstration)
if __name__ == '__main__':
    extractor = FIPExtractor()
    extractor.extract_second_png_from_single_file("./FIPExtractor/raw/SE-2_PN20_ASN1_SP1_PT1_FIP_ASN_1.cmax2")
    extractor.extract_second_png_from_cmax_files(folder_path="./FIPExtractor/raw/")