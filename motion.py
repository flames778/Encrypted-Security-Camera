import cv2
import numpy as np

class MotionDetector:
    def __init__(self, threshold=5000):
        self.subtractor = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=50, detectShadows=False)
        self.threshold = threshold

    def detect(self, frame) -> bool:
        """
        Returns True if motion is detected in the frame.
        """
        # Apply background subtraction
        mask = self.subtractor.apply(frame)
        
        # Optional: reduce noise with morphological operations
        kernel = np.ones((5,5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        
        # Count non-zero pixels
        changed_pixels = cv2.countNonZero(mask)
        
        return changed_pixels > self.threshold
