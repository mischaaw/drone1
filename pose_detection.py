import pygame
import numpy as np
import mediapipe as mp

# Initialize pygame
pygame.init()

# Initialize MediaPipe Pose module
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Initialize MediaPipe Drawing module to draw the pose landmarks
mp_drawing = mp.solutions.drawing_utils

# Initialize Pygame camera
pygame.display.set_mode((640, 480))
cap = pygame.camera.Camera(pygame.camera.list_cameras()[0], (640, 480))
cap.start()

# Set up the window for displaying the camera feed
screen = pygame.display.set_mode((640, 480))

# Main loop
while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Capture a frame from the webcam
    frame = cap.get_image()

    # Convert Pygame surface to numpy array for processing by MediaPipe
    frame_array = np.array(pygame.surfarray.pixels3d(frame))

    # Process the frame with MediaPipe pose detection
    results = pose.process(frame_array)

    # Draw landmarks if pose landmarks are found
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(frame_array, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    # Convert numpy array back to Pygame surface for displaying
    frame_surface = pygame.surfarray.make_surface(frame_array)

    # Display the frame
    screen.blit(frame_surface, (0, 0))
    pygame.display.flip()

# Close the Pygame window after quitting
cap.stop()
pygame.quit()
