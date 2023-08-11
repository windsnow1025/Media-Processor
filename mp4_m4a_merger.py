import glob
import os
import subprocess


def merge_audio_video(
        ffmpeg_path,
        video_file,
        audio_file,
        output_file,
):
    command = f'{ffmpeg_path} -i "{video_file}" -i "{audio_file}" -c:v copy -c:a aac -strict experimental "{output_file}"'
    subprocess.call(command, shell=True)


def merge_mp4_m4a(ffmpeg_path):
    # Get all mp4 and m4a files in the input directory
    mp4_files = glob.glob("input\\*.mp4")
    m4a_files = glob.glob("input\\*.m4a")

    # Sort the lists just to make sure they are in the same order
    mp4_files.sort()
    m4a_files.sort()

    # Iterate over the mp4 files
    for mp4_file in mp4_files:
        # Get the base name of the mp4 file
        mp4_base_name = os.path.splitext(os.path.basename(mp4_file))[0]

        # Check if there is a matching m4a file
        for m4a_file in m4a_files:
            m4a_base_name = os.path.splitext(os.path.basename(m4a_file))[0]
            if mp4_base_name == m4a_base_name:
                # If there is a match, merge the files and break the loop
                output_file = f"output\\{mp4_base_name}.mp4"
                merge_audio_video(ffmpeg_path, mp4_file, m4a_file, output_file)
                break
