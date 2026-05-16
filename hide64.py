import subprocess
import sys
import os

def hide_data(input_mp4, secret_file, output_mp4):
    print(f"[*] Starting Steganography Process...")
    print(f"[*] Input: {input_mp4} | Secret: {secret_file}")

    ffmpeg_cmd = [
        "ffmpeg", 
        "-i", input_mp4, 
        "-f", "yuv4mpegpipe", 
        "-" # Output to stdout
    ]

    x264_cmd = [
        "./x264.exe", 
        "--demuxer", "y4m", 
        "-", # Read from stdin
        "-o", output_mp4, 
        "--no-8x8dct",
        "--hide", secret_file
    ]

    print("[*] Spinning up FFmpeg and x264 instances...")

    ffmpeg_process = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

    x264_process = subprocess.Popen(x264_cmd, stdin=ffmpeg_process.stdout)

    x264_process.communicate()

    if x264_process.returncode == 0:
        print(f"[+] Success! Data hidden inside {output_mp4}")
    else:
        print("[-] An error occurred during encoding.")

if __name__ == "__main__":
    hide_data("./../smallest_fractal.mp4", "./../pass.txt", "./../final_video.mp4")