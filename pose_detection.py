import cv2
import mediapipe as mp
from codrone_edu.drone import Drone
import time
import numpy as np


# Initialize the drone
drone = Drone()
drone.pair()  # Connect to the drone


# Initialize MediaPipe for Face Mesh (to detect smiles/frowns) and Hand Detection
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils


# Open the webcam
cap = cv2.VideoCapture(0)


# Track drone state
drone_is_flying = False  # Variable to track whether the drone is flying
drone_is_flipping = False  # Variable to track whether the drone is flipping




# Function to calculate the distance between two points
def calculate_distance(p1, p2):
   return np.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)




print("Waiting for hand or smile/frown to be detected...")


try:
   while True:
       # Read a frame from the camera
       ret, frame = cap.read()


       if not ret:
           print("Failed to grab frame")
           break


       # Flip the frame horizontally for a later mirror view
       frame = cv2.flip(frame, 1)


       # Convert the frame to RGB for MediaPipe
       rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


       # Process face mesh for smile/frown detection
       face_results = face_mesh.process(rgb_frame)


       # Process hands for hand detection
       hand_results = hands.process(rgb_frame)


       # Initialize hand_detected to False before checking
       hand_detected = False
       smile_detected = False
       frown_detected = False


       # If a hand is detected, perform the flip action
       if hand_results.multi_hand_landmarks:
           hand_detected = True
           for hand_landmarks in hand_results.multi_hand_landmarks:
               mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
          
           # Perform flip if hand detected and drone is in the air
           if not drone_is_flipping and drone_is_flying:
               print("Hand detected, flipping...")
               drone.flip()  # Flip the drone
               drone_is_flipping = True  # Update drone state
               cv2.putText(frame, "Hand Detected - Drone Flipping", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)


       # Face landmarks for smile/frown detection
       if face_results.multi_face_landmarks:
           for face_landmarks in face_results.multi_face_landmarks:
               # Draw face landmarks
               mp_drawing.draw_landmarks(frame, face_landmarks, mp_face_mesh.FACEMESH_CONTOURS)


               # Get the corners of the mouth
               mouth_left = face_landmarks.landmark[61]
               mouth_right = face_landmarks.landmark[291]


               # Calculate the distance between the corners of the mouth
               mouth_distance = calculate_distance((mouth_left.x, mouth_left.y), (mouth_right.x, mouth_right.y))


               # Print the mouth distance for debugging
               print(f"Mouth distance: {mouth_distance:.4f}")


               # Control drone movement based on smile or frown
               if mouth_distance > 0.075:  # Smile detected (greater mouth distance)
                   smile_detected = True
                   if not drone_is_flying:
                       print("Smile detected, taking off...")
                       drone.takeoff()  # Take off the drone
                       drone_is_flying = True  # Update drone state
                       cv2.putText(frame, "Smile Detected - Drone Taking Off", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
               elif mouth_distance < 0.060:  # Frown detected (smaller mouth distance)
                   frown_detected = True
                   if drone_is_flying:
                       print("Frown detected, landing...")
                       drone.land()  # Land the drone
                       drone_is_flying = False  # Update drone state
                       cv2.putText(frame, "Frown Detected - Drone Landing", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)


       # If no hand is detected and the drone is flipping, reset the flipping state
       if not hand_detected and drone_is_flipping:
           drone_is_flipping = False


       # Show the webcam feed with the hand landmarks drawn
       cv2.imshow("Face and Hand Detection", frame)


       # Exit on pressing 'q'
       if cv2.waitKey(1) & 0xFF == ord('q'):
           break


except KeyboardInterrupt:
   print("Program stopped by user. Attempting to land safely...")
   drone.land()  # Safely land the drone


# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()


# Disconnect the drone after the program ends
drone.close()