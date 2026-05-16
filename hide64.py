import subprocess
import sys
import os

def hide_data(input_mp4, secret_file, output_mp4):
    print(f"[*] Starting Steganography Process...")
    print(f"[*] Input: {input_mp4} | Secret: {secret_file}")

    temp_264 = "temp_stealth.264"

    ffmpeg_decode_cmd = [
        "ffmpeg", \
        "-i", input_mp4, 
        "-f", "yuv4mpegpipe", 
        "-"
    ]

    x264_cmd = [
        "./x264.exe", 
        "--demuxer", "y4m", 
        "-", 
        "-o", temp_264, 
        "--no-8x8dct",
        "--hide", secret_file
    ]

    print("[*] Spinning up FFmpeg and x264 instances...")

    ffmpeg_process = subprocess.Popen(ffmpeg_decode_cmd, stdout=subprocess.PIPE, stderr=None)
    x264_process = subprocess.Popen(x264_cmd, stdin=ffmpeg_process.stdout)
    ffmpeg_process.stdout.close()
    x264_process.communicate()

    if x264_process.returncode != 0:
        print("[-] An error occurred during x264 encoding.")
        return

    print("[*] x264 encoding complete. Muxing back into MP4 and restoring audio...")

    # Mux the raw .264 video and the original audio back into a final MP4
    ffmpeg_mux_cmd = [
        "ffmpeg",
        "-y",
        "-i", temp_264,        # Stream 0: Our new steganography video
        "-i", input_mp4,       # Stream 1: The original video (for audio)
        "-c:v", "copy",
        "-c:a", "copy",
        "-map", "0:v:0",       # Take video from the first input
        "-map", "1:a:0?",      # Take audio from the second input (if it exists)
        output_mp4
    ]

    mux_process = subprocess.run(ffmpeg_mux_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if mux_process.returncode == 0:
        print(f"[+] Success! Data hidden inside {output_mp4}")
        # Clean up the temporary raw file
        if os.path.exists(temp_264):
            os.remove(temp_264)
    else:
        print("[-] An error occurred during FFmpeg muxing.")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    input_video = os.path.join(script_dir, "..", "smallest_fractal.mp4")
    secret = os.path.join(script_dir, "..", "pass.txt")
    output_video = os.path.join(script_dir, "..", "final_stego_video.mp4")
    
    input_video = os.path.abspath(input_video)
    secret = os.path.abspath(secret)
    output_video = os.path.abspath(output_video)
    
    hide_data(input_video, secret, output_video)