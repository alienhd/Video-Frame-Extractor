import cv2
import os
import random
from tqdm import tqdm

# Prompt the user to enter the values for the variables
frame_extraction_mode = input("Enter 'random' to extract random frames or 'interval' to extract frames at a specified interval: ")
directory = input("Enter the directory containing the videos: ")
output_directory = input("Enter the directory to save the captured frames: ")
min_frames = int(input("Enter the minimum number of frames to capture from each video: "))
max_frames = int(input("Enter the maximum number of frames to capture from each video: "))
frame_rate = float(input("Enter the rate of frames to capture (e.g., 0.1 = 1 frame per 10 seconds of video): "))

# Get a list of all video files in the directory and its subdirectories
video_files = []
for dirpath, dirnames, filenames in os.walk(directory):
    for filename in filenames:
        if filename.endswith((".mp4", ".mkv", ".avi", ".flv", ".MPG", ".mov", ".3gp", ".wmv", ".m4v")):
            filepath = os.path.join(dirpath, filename)
            video_files.append(filepath)

# Process each video file and display a progress bar
for filepath in tqdm(video_files, desc="Processing videos", unit="file"):
    vidcap = cv2.VideoCapture(filepath)
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    if fps > 0:
        duration = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT) / fps)
        num_frames = int(duration * frame_rate)
        num_frames = max(min(num_frames, max_frames), min_frames)
        if duration > 0 and num_frames > 0:
            # Display a progress bar for extracting frames from the current video
            with tqdm(total=num_frames, desc="Extracting frames", unit="frame", leave=False) as pbar:
                for i in range(num_frames):
                    if frame_extraction_mode == 'random':
                        frame_number = random.randint(0, int(duration * fps) - 1)
                    else:
                        frame_number = int(i * (duration * fps) / num_frames)
                    vidcap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
                    success, image = vidcap.read()
                    if success:
                        filename = os.path.basename(filepath)
                        output_filename = f"{os.path.splitext(filename)[0]}_frame{i}.jpg"
                        output_filepath = os.path.join(output_directory, output_filename)
                        cv2.imwrite(output_filepath, image)
                    pbar.update(1)
