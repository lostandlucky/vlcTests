#!/usr/bin/env python3
import os
import subprocess
import sys
from pathlib import Path

def convert_tiff_to_jpg(input_dir):
    # Find all .tif and .tiff files
    tiff_files = []
    for ext in ['.tif', '.tiff']:
        tiff_files.extend(Path(input_dir).glob(f'*{ext}'))
    
    if not tiff_files:
        print("No TIFF files found.")
        return

    print(f"Found {len(tiff_files)} TIFF files to convert.")
    
    for i, tiff_file in enumerate(tiff_files, 1):
        jpg_file = tiff_file.with_suffix('.jpg')
        print(f"Converting {i}/{len(tiff_files)}: {tiff_file.name}")
        
        try:
            # Run ffmpeg with high quality settings
            subprocess.run([
                'ffmpeg',
                '-i', str(tiff_file),
                '-qscale:v', '2',  # High quality (1-31, lower is better)
                '-y',  # Overwrite output files
                str(jpg_file)
            ], check=True, capture_output=True)
            
            print(f"Successfully converted: {jpg_file.name}")
            
        except subprocess.CalledProcessError as e:
            print(f"Error converting {tiff_file.name}:")
            print(e.stderr.decode())
            continue

if __name__ == "__main__":
    input_dir = sys.argv[1] if len(sys.argv) > 1 else '.'
    convert_tiff_to_jpg(input_dir)
