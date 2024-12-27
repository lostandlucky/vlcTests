#Convert all .tif files in video directory to .jpg files

import os
from PIL import Image

def convert2jpg(folder):
    all_files = []
    for f in sorted(os.listdir(folder)):
        if f.lower().endswith('.tif'):
            all_files.append(os.path.join(folder, f))
    if not all_files:
        raise FileNotFoundError(f"No media found in {folder}")
    return all_files

def convert_tif_to_jpg(tif_file):
    im = Image.open(tif_file)
    jpg_file = tif_file.replace('.tif', '.jpg')
    im.save(jpg_file)
    return jpg_file

def main():
    tif_files = convert2jpg('Videos')
    for tif_file in tif_files:
        jpg_file = convert_tif_to_jpg(tif_file)
        print(f"Converted {tif_file} to {jpg_file}")
        
if __name__ == '__main__':
    main()