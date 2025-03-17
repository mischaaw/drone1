import cv2
import mediapipe as mp
from codrone_edu.drone import Drone


# Initialize the drone
drone = Drone()
drone.pair()  # Connect to the drone


# Initialize MediaPipe hand detection
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils


# Initialize MediaPipe face detection and face landmarks
mp_face = mp.solutions.face_mesh
face_mesh = mp_face.FaceMesh(min_detection_confidence=0.7, min_tracking_confidence=0.7)


# Open the webcam
cap = cv2.VideoCapture(0)


print("Waiting for hand to be detected...")


# Track drone state
drone_is_flying = False  # Variable to track whether the drone is flying


# Define the scaling factor for translating pixel distance into inches (Adjust as needed)
INCHES_TO_PIXELS = 100  # You may need to adjust this based on your camera setup


# Main loop for hand detection, face detection, and drone control
try:
   while True:
       # Read a frame from the camera
       ret, frame = cap.read()
       if not ret:
           print("Failed to grab frame")
           break


       # Flip the frame horizontally for a mirror view
       frame = cv2.flip(frame, 1)


       # Convert the frame to RGB for MediaPipe
       rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
       hand_results = hands.process(rgb_frame)
       face_results = face_mesh.process(rgb_frame)


       # Initialize hand_detected to False before checking
       hand_detected = False


       # Draw hand landmarks if a hand is detected
       if hand_results.multi_hand_landmarks:
           hand_detected = True
           for hand_landmarks in hand_results.multi_hand_landmarks:
               mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)


       # If a hand is detected, take off the drone, else land
       if hand_detected and not drone_is_flying:
           print("Hand detected, taking off...")
           drone.takeoff()  # Take off the drone
           drone_is_flying = True  # Update the drone state
           cv2.putText(frame, "Hand Detected - Drone Taking Off", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
       elif not hand_detected and drone_is_flying:
           print("No hand detected, landing...")
           drone.land()  # Land the drone
           drone_is_flying = False  # Update the drone state
           cv2.putText(frame, "No Hand Detected - Drone Landing", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)


       # Face detection for smile/frown control (use landmarks for mouth region)
       if face_results.multi_face_landmarks:
           for face_landmarks in face_results.multi_face_landmarks:
               # Detect smile/frown based on mouth landmarks
               upper_lip = face_landmarks.landmark[13]  # Upper lip center
               lower_lip = face_landmarks.landmark[14]  # Lower lip center


               # Calculate the distance between the lips (in normalized coordinates)
               lip_distance = lower_lip.y - upper_lip.y


               # If the lip distance indicates a smile (small change, lips closer together), move up
               if lip_distance < 0.02:  # Smile
                   print("Smile detected, drone going up...")
                   if drone_is_flying:
                       # Adjust the amount of vertical movement to 12 inches
                       drone.move_up(12)  # Move the drone up by 12 inches
                   cv2.putText(frame, "Smile Detected - Drone Going Up", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)


               # If the lip distance indicates a frown (larger gap between lips), move down
               elif lip_distance > 0.04:  # Frown
                   print("Frown detected, drone going down...")
                   if drone_is_flying:
                       # Adjust the amount of vertical movement to 12 inches
                       drone.move_down(12)  # Move the drone down by 12 inches
                   cv2.putText(frame, "Frown Detected - Drone Going Down", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)


       # Show the webcam feed with the hand landmarks and face landmarks drawn
       cv2.imshow("Hand and Face Detection", frame)


       # Exit on pressing 'q'
       if cv2.waitKey(1) & 0xFF == ord('q'):
           break


except KeyboardInterrupt:
   print("Emergency Stop (Ctrl+C)! Drone landing...")
   if drone_is_flying:
       drone.land()  # Safely land the drone if flying
   drone_is_flying = False  # Update the drone state


# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()


# Disconnect the drone after the program ends
drone.close()