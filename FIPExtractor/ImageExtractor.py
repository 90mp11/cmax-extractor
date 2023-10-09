from PIL import Image
import io

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