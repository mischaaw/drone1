🚁 Drone Control with Facial Expressions & Hand Gestures 🤖

Welcome to an interactive and fun drone control system that responds to facial expressions and hand gestures! 🎉 Using the power of MediaPipe for face and hand detection, this program allows you to control your drone in the coolest way possible. Whether you're smiling, frowning, or waving your hand, this program listens to your every move. 😎

🚀 Features ✨

Smile 😁 = Drone Takes Off
Frown 😞 = Drone Lands
Hand Gesture ✋ = Drone Does a Flip
Webcam Feed 📸 with live face and hand landmarks displayed
Real-Time Control with your face and hands - no controllers needed!


🛠️ Requirements 📦

Before you get started, make sure you have the following:

Python 3.6+
Libraries:
opencv-python (for webcam video handling)
mediapipe (for face & hand detection)
numpy (for distance calculation)
codrone-edu (for controlling the drone)

📥 Installation 🖥️

1. Install Python Dependencies
First, ensure you have Python 3.6+ installed. Then, open your terminal and run the following to install all required libraries:

pip install opencv-python mediapipe numpy codrone-edu
2. Pair Your Drone 🚁
Make sure your Cordon EDU drone is paired with your computer. Follow the instructions in the Cordon EDU SDK documentation to connect the drone to your machine.

3. Clone This Repository (Optional) 🌱
If you're using a GitHub repository, clone it to your local machine:

git clone https://github.com/your-username/drone-control.git
4. Run The Script 🏃
Once you’re ready, navigate to the folder where your script is located, and run the script:

python drone_control.py
You’ll see your webcam feed pop up with the live detection of your face and hands. Get ready for some drone action! 🛸

5. Exit the Program 🏁
To stop the program, simply press the ‘q’ key. Your drone will land safely! ✨

🤖 How It Works 💡

Smile Detection 😁
The program detects your smile by analyzing the distance between the corners of your mouth.
If your mouth distance is above a certain threshold (0.075+), it recognizes the smile and commands the drone to take off. 🚀

Frown Detection 😞
Similarly, if the mouth distance drops below a threshold (0.060-), it detects a frown and tells the drone to land. 🌍

Hand Detection ✋
Using MediaPipe Hand Tracking, if the program detects a hand gesture, the drone will perform a flip. 😜

🛠️ Troubleshooting 🔧

Webcam not showing? Make sure your webcam is properly connected to your computer and accessible by OpenCV.
Drone not responding? Ensure your drone is properly connected via the codrone-edu library. Double-check your pairing setup.
Facial landmarks not showing correctly? Adjust the mouth_distance thresholds to fine-tune smile and frown detection based on your face.

👏 Special Thanks 🙏

A big shoutout to:

MediaPipe: For face and hand tracking magic! ✨
OpenCV: For handling the webcam feed and capturing live video. 🎥
Cordon EDU SDK: For making the drone come to life! 🚁
Now, go ahead and have fun controlling your drone with just your smile, frown, or hand gestures! 😄👋

Feel free to tweak or adjust this as needed! This version is more dynamic and visually appealing while keeping things lighthearted and fun. 🎉