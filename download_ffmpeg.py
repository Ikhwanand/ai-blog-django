import requests
import zipfile
import os
import shutil
from pathlib import Path

def download_ffmpeg():
    # Create ffmpeg directory
    ffmpeg_dir = Path('ffmpeg')
    ffmpeg_dir.mkdir(exist_ok=True)
    
    # Download FFmpeg
    url = 'https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip'
    print('Downloading FFmpeg...')
    response = requests.get(url, stream=True)
    zip_path = Path('ffmpeg.zip')
    
    with open(zip_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    
    # Extract FFmpeg
    print('Extracting FFmpeg...')
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(ffmpeg_dir)
    
    # Move ffmpeg.exe to the root of ffmpeg directory
    ffmpeg_exe = next(ffmpeg_dir.rglob('ffmpeg.exe'))
    shutil.move(str(ffmpeg_exe), str(ffmpeg_dir / 'ffmpeg.exe'))
    
    # Clean up
    zip_path.unlink()
    print('FFmpeg installation complete!')

if __name__ == '__main__':
    download_ffmpeg()
