import cv2
import os
import glob
from moviepy.editor import VideoFileClip

# Path to the Haar cascades for face and eye detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Function to get the most recent video
def get_most_recent_video():
    video_files = glob.glob('raw_videos/*/camera_recording_*.mp4')
    if not video_files:
        print("No videos found.")
        return None
    most_recent_file = max(video_files, key=os.path.getctime)
    return most_recent_file


import cv2
import os

# Function to detect eyes and crop the video, focusing only on the top half of the face
def crop_video_to_eyes(video_path):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Get FPS from the original video
    fps = cap.get(cv2.CAP_PROP_FPS)

    output_path = 'processed_videos/cropped_' + os.path.basename(video_path)
    out = None  # Initialize the video writer to None

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert frame to grayscale for detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect face
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            # Define the region to focus on the top left of the face
            face_top_left_half_gray = gray[y:y + h // 2, x:x + w]

            # Detect eyes within the top half of the face
            eyes = eye_cascade.detectMultiScale(face_top_left_half_gray)
            
            if not eyes:
                print("No eyes detected in the video frame.")
                return None

            if eyes is not None:
            # if len(eyes) >= 2:  # We assume we need at least two eyes
                ex, ey, ew, eh = eyes[0]  # Get the first detected eye

                # Define the cropping region around the detected eyes
                crop_x1 = max(0, x + ex - ew)
                crop_y1 = max(0, y + ey - eh)
                crop_x2 = min(frame.shape[1], x + ex + ew * 2)
                crop_y2 = min(frame.shape[0], y + ey + eh * 2)

                # Crop the frame around the detected eye region
                cropped_frame = frame[crop_y1:crop_y2, crop_x1:crop_x2]

                # Initialize VideoWriter
                if out is None:
                    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                    cropped_height, cropped_width, _ = cropped_frame.shape
                    out = cv2.VideoWriter(output_path, fourcc, fps, (cropped_width, cropped_height))

                # Write the cropped frame to the output video
                out.write(cropped_frame)

    # Release the video capture and writer objects
    cap.release()
    if out is not None:
        out.release()
    cv2.destroyAllWindows()

    return output_path

# Main function
def process_latest_camera_recording():
    video_path = get_most_recent_video()
    if video_path:
        cropped_video = crop_video_to_eyes(video_path)
        print(f"Video cropped and saved at: {cropped_video}")

# Run the script
if __name__ == '__main__':
    process_latest_camera_recording()
