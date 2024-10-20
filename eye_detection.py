import cv2
import os
import glob

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

# Function to detect eyes and crop the video, focusing only on the top half of the face
def crop_video_to_eye_region(video_path):
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    
    # Get FPS from the original video
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Output path for the cropped video
    output_path = 'processed_videos/cropped_' + os.path.basename(video_path)
    out = None  # Initialize the video writer to None
    crop_region = None  # To store the cropping region based on the first detected eye

    # Process each frame of the video
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert frame to grayscale for detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if crop_region is None:
            # Detect face
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            # If face is detected
            for (x, y, w, h) in faces:
                # Define the region for the top half of the face
                face_top_half = gray[y:y + h // 2, x:x + w]

                # Detect eyes within the top half of the face
                eyes = eye_cascade.detectMultiScale(face_top_half, scaleFactor=1.1, minNeighbors=5)

                if len(eyes) == 0:
                    print("No eyes detected in this frame.")
                    continue

                # Get the first detected eye (if multiple are found)
                ex, ey, ew, eh = eyes[0]

                # Calculate the cropping region around the eye (square region)
                eye_center_x = x + ex + ew // 2
                eye_center_y = y + ey + eh // 2
                side_length = max(ew, eh) * 2  # Create a square around the eye
                half_side_length = side_length // 2

                crop_x1 = max(0, eye_center_x - half_side_length)
                crop_y1 = max(0, eye_center_y - half_side_length)
                crop_x2 = min(frame.shape[1], eye_center_x + half_side_length)
                crop_y2 = min(frame.shape[0], eye_center_y + half_side_length)

                crop_region = (crop_x1, crop_y1, crop_x2, crop_y2)
                break

        if crop_region:
            # Apply the cropping region from the first detected eye to all frames
            crop_x1, crop_y1, crop_x2, crop_y2 = crop_region
            cropped_frame = frame[crop_y1:crop_y2, crop_x1:crop_x2]

            # Initialize the VideoWriter if not already done
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
        cropped_video = crop_video_to_eye_region(video_path)
        if cropped_video:
            print(f"Video cropped and saved at: {cropped_video}")
        else:
            print("Error: No eyes were detected in the video.")
    else:
        print("No video to process.")

# Run the script
if __name__ == '__main__':
    process_latest_camera_recording()
