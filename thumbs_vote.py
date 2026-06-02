import cv2
import mediapipe as mp
import numpy as np
from collections import deque
import time

class ThumbsVoteApp:
    def __init__(self):
        # MediaPipe initialization
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        
        # Webcam setup
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
        # Vote tracking
        self.votes = {"pass": 0, "reject": 0}
        self.last_vote_time = 0
        self.vote_cooldown = 1.5  # seconds between votes
        
        # Gesture history for smoothing
        self.gesture_history = deque(maxlen=10)
        self.current_gesture = None
        
    def detect_thumbs_gesture(self, hand_landmarks):
        """
        Detect thumbs up or thumbs down gesture
        Returns: "thumbs_up", "thumbs_down", or None
        """
        # Get key points
        wrist = hand_landmarks[0]
        thumb_ip = hand_landmarks[3]  # Thumb IP joint
        thumb_mcp = hand_landmarks[2]  # Thumb MCP joint
        index_mcp = hand_landmarks[5]  # Index MCP joint
        middle_mcp = hand_landmarks[9]  # Middle MCP joint
        ring_mcp = hand_landmarks[13]  # Ring MCP joint
        pinky_mcp = hand_landmarks[17]  # Pinky MCP joint
        
        # Calculate distances and angles
        thumb_to_wrist_y = thumb_ip.y - wrist.y
        index_to_wrist_y = index_mcp.y - wrist.y
        
        # Check if thumb is extended (positive y means down on screen)
        thumb_extended = thumb_to_wrist_y < -0.15
        
        # Check if other fingers are curled (positive y means down)
        other_fingers_curled = (index_to_wrist_y > -0.1 and 
                               middle_mcp.y - wrist.y > -0.1 and 
                               ring_mcp.y - wrist.y > -0.1 and 
                               pinky_mcp.y - wrist.y > -0.1)
        
        if thumb_extended and other_fingers_curled:
            # Determine thumbs up or down based on wrist angle
            if thumb_mcp.y > wrist.y:
                return "thumbs_down"
            else:
                return "thumbs_up"
        
        return None
    
    def process_frame(self, frame):
        """Process single frame and detect gestures"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        
        gesture = None
        
        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0].landmark
            
            # Draw hand landmarks
            self.mp_drawing.draw_landmarks(
                frame,
                results.multi_hand_landmarks[0],
                self.mp_hands.HAND_CONNECTIONS
            )
            
            # Detect gesture
            gesture = self.detect_thumbs_gesture(hand_landmarks)
            
            # Smooth gesture with history
            if gesture:
                self.gesture_history.append(gesture)
                most_common = max(set(self.gesture_history), key=list(self.gesture_history).count)
                
                if most_common and most_common != self.current_gesture:
                    self.current_gesture = most_common
                    current_time = time.time()
                    
                    # Register vote if cooldown passed
                    if current_time - self.last_vote_time > self.vote_cooldown:
                        if most_common == "thumbs_up":
                            self.votes["pass"] += 1
                            self.last_vote_time = current_time
                        elif most_common == "thumbs_down":
                            self.votes["reject"] += 1
                            self.last_vote_time = current_time
        
        return frame, gesture
    
    def draw_ui(self, frame, gesture):
        """Draw UI elements on frame"""
        h, w, c = frame.shape
        
        # Draw vote counts
        cv2.rectangle(frame, (10, 10), (350, 100), (0, 0, 0), -1)
        cv2.putText(frame, f"PASS: {self.votes['pass']}", (20, 45),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
        cv2.putText(frame, f"REJECT: {self.votes['reject']}", (20, 85),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
        
        # Draw current gesture
        if gesture:
            if gesture == "thumbs_up":
                cv2.rectangle(frame, (w-350, h-150), (w-10, h-10), (0, 255, 0), -1)
                cv2.putText(frame, "THUMBS UP!", (w-340, h-60),
                           cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 3)
                cv2.putText(frame, "PASS", (w-340, h-20),
                           cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 2)
            elif gesture == "thumbs_down":
                cv2.rectangle(frame, (w-350, h-150), (w-10, h-10), (0, 0, 255), -1)
                cv2.putText(frame, "THUMBS DOWN!", (w-340, h-60),
                           cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)
                cv2.putText(frame, "REJECT", (w-340, h-20),
                           cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)
        
        # Draw instructions
        cv2.putText(frame, "Thumbs UP = PASS | Thumbs DOWN = REJECT", (10, h-20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, "Press 'q' to quit | 'r' to reset", (10, h-50),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        return frame
    
    def run(self):
        """Main loop"""
        print("Starting Thumbs Vote App...")
        print("Gesture Detection Active")
        print("Press 'q' to quit, 'r' to reset votes")
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            # Flip frame for selfie view
            frame = cv2.flip(frame, 1)
            
            # Process frame
            frame, gesture = self.process_frame(frame)
            
            # Draw UI
            frame = self.draw_ui(frame, gesture)
            
            # Display
            cv2.imshow("Thumbs Vote - Gesture Detection", frame)
            
            # Handle keys
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('r'):
                self.votes = {"pass": 0, "reject": 0}
                print("Votes reset!")
        
        # Cleanup
        self.cap.release()
        cv2.destroyAllWindows()
        self.hands.close()
        
        print(f"\nFinal Results:")
        print(f"PASS: {self.votes['pass']}")
        print(f"REJECT: {self.votes['reject']}")

if __name__ == "__main__":
    app = ThumbsVoteApp()
    app.run()