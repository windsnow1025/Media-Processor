import os

from dotenv import load_dotenv

from mp4_m4a_merger import merge_mp4_m4a
from mp4_trimmer import trim_mp4_end


def main():
    load_dotenv()
    ffmpeg_path = os.getenv("FFMPEG_PATH")
    ffprobe_path = ffmpeg_path.replace("ffmpeg.exe", "ffprobe.exe")
    merge_mp4_m4a(ffmpeg_path)
    trim_mp4_end(ffmpeg_path, ffprobe_path, seconds_to_remove=10)


if __name__ == "__main__":
    main()
