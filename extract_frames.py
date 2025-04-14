import cv2
import os
import shutil



def extract_frames(video_path, output_folder):


    # Check if the output folder exists. If it does, remove all its contents.
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Open the video
    cap = cv2.VideoCapture(video_path)

    # Check if the video was opened successfully
    if not cap.isOpened():
        print("Error: Couldn't open video.")
        exit()

    frame_count = 0
    frame_number = 0

    #while True # this was commented out and changed for testing purposes
    while frame_count < 100:
        # Read the next frame from the video
        ret, frame = cap.read()

        # If the frame was not read correctly, exit the loop
        if not ret:
            break

        # Check if the frame number is a multiple of 6
        if frame_number % 6 == 0:
            # Save the frame as an image
            frame_filename = os.path.join(output_folder, f'frame_{frame_count:04d}.png')
            cv2.imwrite(frame_filename, frame)
            print(f'Saved {frame_filename}')

            frame_count += 1

        frame_number += 1

    # Release the video capture object and close any OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

    print(f"Extracted {frame_count} frames.")
