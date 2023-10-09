
# FIPExtractor

## Description

`FIPExtractor` is a Python module designed to extract the second PNG image from `.cmax2` files.
It also provides functionality to handle `.zip` archives containing `.cmax2` files.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/FIPExtractor.git
   ```
   
2. Navigate to the repository folder and install the package:
   ```bash
   cd FIPExtractor
   pip install .
   ```

## Usage

```python
from FIPExtractor import FIPExtractor

# Initialize the extractor
extractor = FIPExtractor(folder_path='./raw', temp_folder='./temp', output_path='./output')

# Run the extraction
extractor.extract_second_png_from_cmax_files()
```

## Parameters

- `folder_path`: Path to the folder containing the `.cmax2` or `.zip` files (default is `./raw`).
- `temp_folder`: Path to the temporary folder used for extraction (default is `./temp`).
- `output_path`: Path where the extracted PNGs will be saved (default is `./output`).

## License

This project is not intended for public consumption or modification and is made available simply to demonstrate the capabilities of GPT4 at creating a module from minimal input