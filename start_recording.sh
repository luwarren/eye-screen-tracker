#!/bin/bash

# Output filenames with timestamp
timestamp=$(date +"%Y-%m-%d_%H-%M-%S")
mkdir -p "raw_videos/$timestamp"
folder_name="raw_videos/$timestamp"
screen_output="$folder_name/screen_recording_$timestamp.mp4"
camera_output="$folder_name/camera_recording_$timestamp.mp4"


# Set the display ID for screen recording (Let user choose from active displays)
display_options=$(ffmpeg -f avfoundation -list_devices true -i "" 2>&1 | grep -Eo '\[\d+\] [^[]+' | grep -viE 'audio|music|sounds|microphone')
display_full_selection=$(echo "$display_options" | zenity --list --title="Choose Display" --column="Display Options")
display_id=$(echo "$display_full_selection" | awk -F '[][]' '{print $2}')
echo "Display ID: $display_id"

# Set the video device for camera recording (Let user choose from active cameras)
camera_options=$(ffmpeg -f avfoundation -list_devices true -i "" 2>&1 | grep -Eo '\[\d+\] [^[]+' | grep -viE 'audio|music|sounds|microphone')
camera_full_selection=$(echo "$camera_options" | zenity --list --title="Choose Camera" --column="Display Options")
camera_id=$(echo "$camera_full_selection" | awk -F '[][]' '{print $2}')
echo "Camera ID: $camera_id"

# Screen resolution (adjust as necessary)
screen_resolution="1920x1080"

# Set framerate
framerate_camera="30" # adjust as necessary - higher FPS = better
framerate_screen="15"

# Start camera recording
ffmpeg -f avfoundation -framerate $framerate_camera -i "$camera_id" -an -r 30 "$camera_output" &

# Start screen recording
ffmpeg -f avfoundation -framerate $framerate_screen -video_size $screen_resolution -i "$display_id" -an -r 30 "$screen_output" &

zenity --info --title="Recording in Progress" --text="Recording in Progress..." --timeout=1 &

# Wait for both processes to finish
wait
