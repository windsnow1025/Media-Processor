import glob
import os
import subprocess
import json


def get_video_duration(ffprobe_path, video_file):
    """Get the duration of a video file in seconds"""
    command = f'{ffprobe_path} -v quiet -print_format json -show_format "{video_file}"'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode == 0:
        data = json.loads(result.stdout)
        duration = float(data['format']['duration'])
        return duration
    else:
        raise Exception(f"Failed to get video duration: {result.stderr}")


def trim_video_end(ffmpeg_path, ffprobe_path, video_file, output_file, seconds_to_remove=10):
    """Remove specified seconds from the end of a video file"""
    # Get the original duration
    original_duration = get_video_duration(ffprobe_path, video_file)

    # Calculate new duration (original - seconds to remove)
    new_duration = original_duration - seconds_to_remove

    if new_duration <= 0:
        raise Exception(f"Cannot remove {seconds_to_remove} seconds from a {original_duration:.2f} second video")

    # Trim the video
    command = f'{ffmpeg_path} -i "{video_file}" -t {new_duration} -c copy "{output_file}"'
    subprocess.call(command, shell=True)
    print(f"Trimmed {seconds_to_remove} seconds from the end. New duration: {new_duration:.2f} seconds")


def trim_mp4_end(ffmpeg_path, ffprobe_path, seconds_to_remove=10):
    """Find the single mp4 file in input directory and trim its end"""
    # Get all mp4 files in the input directory
    mp4_files = glob.glob("input\\*.mp4")

    if len(mp4_files) == 0:
        print("No mp4 files found in input directory")
        return
    elif len(mp4_files) > 1:
        print(f"Found {len(mp4_files)} mp4 files. This program expects only one mp4 file.")
        return

    # Process the single mp4 file
    mp4_file = mp4_files[0]
    base_name = os.path.splitext(os.path.basename(mp4_file))[0]
    output_file = f"output\\{base_name}_trimmed.mp4"

    # Create output directory if it doesn't exist
    os.makedirs("output", exist_ok=True)

    print(f"Processing: {mp4_file}")
    trim_video_end(ffmpeg_path, ffprobe_path, mp4_file, output_file, seconds_to_remove)
    print(f"Output saved to: {output_file}")