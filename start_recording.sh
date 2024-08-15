#!/bin/bash

# Output filenames with timestamp
timestamp=$(date +"%Y-%m-%d_%H-%M-%S")
mkdir -p "raw_videos/$timestamp"
folder_name="raw_videos/$timestamp"
screen_output="$folder_name/screen_recording_$timestamp.mp4"
camera_output="$folder_name/camera_recording_$timestamp.mp4"

# Screen resolution (adjust as necessary)
screen_resolution="1920x1080"

# Set the display ID for screen recording
# usually '1' for the main display
display_id="1"

# Set the video device for camera recording (
# ffmpeg -f avfoundation -list_devices true -i "" to list devices
camera_device="0"

# Set framerate
framerate_camera="30" # adjust as necessary - higher FPS = better
framerate_screen="15"

# Start camera recording
ffmpeg -f avfoundation -framerate $framerate_camera -i "$camera_device" -an -r 30 "$camera_output" &

# Start screen recording
ffmpeg -f avfoundation -framerate $framerate_screen -video_size $screen_resolution -i "$display_id" -an -r 30 "$screen_output" &

# Wait for both processes to finish
wait
