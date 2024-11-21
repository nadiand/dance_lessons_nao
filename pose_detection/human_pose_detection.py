import cv2
import mediapipe as mp
import numpy as np
import time

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

class PoseDetector:
    ATTRIBUTES = ['left forearm', 'left arm', 'right arm', 'left elbow', 'right elbow', 'right forearm']
   
    def __init__(self, ref_file, nr_pics, verbose):
        self.ref_landmarks = self.get_landmark_coords(ref_file)
        self.verbose = verbose
        self.nr_pictures = nr_pics

        # Open a connection to the webcam (default camera is device 0)
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Error: Could not access the webcam.")
        if self.verbose:
            print("Camera opened")

    def take_pics(self, sleep_time = 0.5):
        if self.verbose:
            print("Start taking pictures")
        while True:
            # Read the video frame-by-frame
            ret, frame = self.cap.read()
            if not ret:
                print("Error: Unable to capture video.")
                break
            for i in range(0, self.nr_pictures):
                cv2.imwrite('captured_image' + str(i) + '.jpg', frame)
                time.sleep(sleep_time)
            if self.verbose:
                print("Stop taking pictures")
            break

        # maybe we dont want to release the camera cuz we'll be calling this function often. maybe we should find the function
        # to "capture" the camera again and put it intthe beginning of this funciton TODO


    def get_landmark_coords(self, file, draw=False):
        IMAGE_FILES = (file)
        BG_COLOR = (192, 192, 192) # gray
        with mp_pose.Pose(
            static_image_mode=True,
            model_complexity=1,
            enable_segmentation=True,
            min_detection_confidence=0.5) as pose:
            # for idx, file in enumerate(IMAGE_FILES):
            image = cv2.imread(IMAGE_FILES)
            image_height, image_width, _ = image.shape
            # Convert the BGR image to RGB before processing.
            results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

            # if not results.pose_landmarks:
            #   continue
            # print(
            #     f'Nose coordinates: ('
            #     f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].x}, '
            #     f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].y})'
            # )

            if draw:

                annotated_image = image.copy()
                # Draw segmentation on the image.
                # To improve segmentation around boundaries, consider applying a joint
                # bilateral filter to "results.segmentation_mask" with "image".
                condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
                bg_image = np.zeros(image.shape, dtype=np.uint8)
                bg_image[:] = BG_COLOR
                annotated_image = np.where(condition, annotated_image, bg_image)
                # Draw pose landmarks on the image.
                self.draw_image_landmarks(annotated_image, results)
            
        
        combined_pos = {
        "original": {
            "LEFT_WRIST": {
                "x": results.pose_world_landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_WRIST].x,
                "y": results.pose_world_landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_WRIST].y,
            },
            "RIGHT_WRIST": {
                "x": results.pose_world_landmarks.landmark[mp.solutions.pose.PoseLandmark.RIGHT_WRIST].x,
                "y": results.pose_world_landmarks.landmark[mp.solutions.pose.PoseLandmark.RIGHT_WRIST].y,
            },
            "LEFT_ELBOW": {
                "x": results.pose_world_landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_ELBOW].x,
                "y": results.pose_world_landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_ELBOW].y,
            },
            "RIGHT_ELBOW": {
                "x": results.pose_world_landmarks.landmark[mp.solutions.pose.PoseLandmark.RIGHT_ELBOW].x,
                "y": results.pose_world_landmarks.landmark[mp.solutions.pose.PoseLandmark.RIGHT_ELBOW].y,
            },
            "LEFT_SHOULDER": {
                "x": results.pose_world_landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER].x,
                "y": results.pose_world_landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER].y,
            },
            "RIGHT_SHOULDER": {
                "x": results.pose_world_landmarks.landmark[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER].x,
                "y": results.pose_world_landmarks.landmark[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER].y,
            },
        },
        # Left and Right have been flipped, as well as the x cooridnate
        "mirrored": {
            "LEFT_WRIST": {
                "x": -results.pose_world_landmarks.landmark[mp.solutions.pose.PoseLandmark.RIGHT_WRIST].x,
                "y": results.pose_world_landmarks.landmark[mp.solutions.pose.PoseLandmark.RIGHT_WRIST].y,
            },
            "RIGHT_WRIST": {
                "x": -results.pose_world_landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_WRIST].x,
                "y": results.pose_world_landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_WRIST].y,
            },
            "LEFT_ELBOW": {
                "x": -results.pose_world_landmarks.landmark[mp.solutions.pose.PoseLandmark.RIGHT_ELBOW].x,
                "y": results.pose_world_landmarks.landmark[mp.solutions.pose.PoseLandmark.RIGHT_ELBOW].y,
            },
            "RIGHT_ELBOW": {
                "x": -results.pose_world_landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_ELBOW].x,
                "y": results.pose_world_landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_ELBOW].y,
            },
            "LEFT_SHOULDER": {
                "x": -results.pose_world_landmarks.landmark[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER].x,
                "y": results.pose_world_landmarks.landmark[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER].y,
            },
            "RIGHT_SHOULDER": {
                "x": -results.pose_world_landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER].x,
                "y": results.pose_world_landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER].y,
            },
        },
        }

        return combined_pos

    def draw_image_landmarks(self, annotated_image, results):
        mp_drawing.draw_landmarks(
                annotated_image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
        cv2.imwrite('/tmp/annotated_image' + '.png', annotated_image)
        # Plot pose world landmarks.
        mp_drawing.plot_landmarks(
            results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS)

    def mean_difference(self, dict):
        reference_list = []
        original_list = []
        mirrored_list = []

        for mirror_key in self.ref_landmarks:
            if mirror_key == "original":
                for point in self.ref_landmarks[mirror_key]:
                    for coord in self.ref_landmarks[mirror_key][point]:
                        reference_list.append(self.ref_landmarks[mirror_key][point][coord]) # TODO calculate this upon init for ref
                        original_list.append(dict[mirror_key][point][coord])
        else:
            for point in self.ref_landmarks[mirror_key]:
                for coord in self.ref_landmarks[mirror_key][point]:
                    mirrored_list.append(dict[mirror_key][point][coord])

        reference_arr = np.array(reference_list)
        original_arr = np.array(original_list)
        mirrored_arr = np.array(mirrored_list)
    
        mean_error_original = abs(reference_arr-original_arr).mean()
        mean_error_mirrored = abs(reference_arr-mirrored_arr).mean()

        if self.verbose:
            print("original: ", mean_error_original)
            print("mirrored: ", mean_error_mirrored)

        return mean_error_original, mean_error_mirrored

    def get_angle(self, point1, point2):
        """
        Calculate the angle between two points relative to the horizontal axis (x-axis).

        Args:
        - point1 (tuple or list): The first point (x1, y1).
        - point2 (tuple or list): The second point (x2, y2).

        Returns:
        - float: The angle between the points and the x-axis in degrees.
        """
        
        # Unpack points
        x1 = point1["x"]
        y1 = point1["y"]
        x2 = point2["x"]
        y2 = point2["y"]

        # Calculate the difference in coordinates
        delta_x = x2 - x1
        delta_y = y2 - y1
        
        # Use np.arctan2 to get the angle in radians
        angle_rad = np.arctan2(delta_y, delta_x)
        
        # Convert the angle to degrees
        angle_deg = np.degrees(angle_rad)
        
        return angle_deg

    def get_angle_between_lines(self, point1, point2, shared_point):
        """
        Calculate the angle between two lines that share a common point.

        Args:
        - point1 (tuple or list): The first point (x1, y1).
        - point2 (tuple or list): The second point (x2, y2).
        - shared_point (tuple or list): The shared point (sx, sy) where the two lines intersect.

        Returns:
        - float: The angle between the lines in degrees.
        """
        
        # Unpack points
        x1 = point1["x"]
        y1 = point1["y"]
        x2 = point2["x"]
        y2 = point2["y"]
        sx = shared_point["x"]
        sy = shared_point["y"]
        
        # Create vectors for both lines (shared_point to point1 and shared_point to point2)
        v1 = np.array([x1 - sx, y1 - sy])  # Vector for the first line
        v2 = np.array([x2 - sx, y2 - sy])  # Vector for the second line
        
        # Calculate the dot product of the two vectors
        dot_product = np.dot(v1, v2)
        
        # Calculate the magnitudes (lengths) of the vectors
        mag_v1 = np.linalg.norm(v1)
        mag_v2 = np.linalg.norm(v2)
        
        # Calculate the cosine of the angle
        cos_theta = dot_product / (mag_v1 * mag_v2)
        
        # Clip value to avoid domain errors due to floating point precision
        cos_theta = np.clip(cos_theta, -1.0, 1.0)
        
        # Calculate the angle in radians
        angle_rad = np.arccos(cos_theta)
        
        # Convert the angle to degrees
        angle_deg = np.degrees(angle_rad)
        
        return angle_deg

    def get_pos_errors(self, pose, mirror_key):
        # Compute angles for ref # TODO calculate this upon init for ref
        angle_ref_left_elbow_wrist = self.get_angle(self.ref_landmarks["original"]["LEFT_ELBOW"], self.ref_landmarks["original"]["LEFT_WRIST"])
        angle_ref_left_shoulder_elbow = self.get_angle(self.ref_landmarks["original"]["LEFT_SHOULDER"], self.ref_landmarks["original"]["LEFT_ELBOW"])
        angle_ref_right_elbow_wrist = self.get_angle(self.ref_landmarks["original"]["RIGHT_ELBOW"], self.ref_landmarks["original"]["RIGHT_WRIST"])
        angle_ref_right_shoulder_elbow = self.get_angle(self.ref_landmarks["original"]["RIGHT_SHOULDER"], self.ref_landmarks["original"]["RIGHT_ELBOW"])

        # Compute angles for pose2
        angle_pose_left_elbow_wrist = self.get_angle(pose[mirror_key]["LEFT_ELBOW"], pose[mirror_key]["LEFT_WRIST"])
        angle_pose_left_shoulder_elbow = self.get_angle(pose[mirror_key]["LEFT_SHOULDER"], pose[mirror_key]["LEFT_ELBOW"])
        angle_pose_right_elbow_wrist = self.get_angle(pose[mirror_key]["RIGHT_ELBOW"], pose[mirror_key]["RIGHT_WRIST"])
        angle_pose_right_shoulder_elbow = self.get_angle(pose[mirror_key]["RIGHT_SHOULDER"], pose[mirror_key]["RIGHT_ELBOW"])

        # Compute elbow angles using `get_angle_between_lines`
        elbow_angle_ref_left = self.get_angle_between_lines(
            self.ref_landmarks["original"]["LEFT_WRIST"],
            self.ref_landmarks["original"]["LEFT_SHOULDER"],
            self.ref_landmarks["original"]["LEFT_ELBOW"]
        )
        elbow_angle_ref_right = self.get_angle_between_lines(
            self.ref_landmarks["original"]["RIGHT_WRIST"],
            self.ref_landmarks["original"]["RIGHT_SHOULDER"],
            self.ref_landmarks["original"]["RIGHT_ELBOW"]
        )
        elbow_angle_pose_left = self.get_angle_between_lines(
            pose[mirror_key]["LEFT_WRIST"],
            pose[mirror_key]["LEFT_SHOULDER"],
            pose[mirror_key]["LEFT_ELBOW"]
        )
        elbow_angle_pose_right = self.get_angle_between_lines(
            pose[mirror_key]["RIGHT_WRIST"],
            pose[mirror_key]["RIGHT_SHOULDER"],
            pose[mirror_key]["RIGHT_ELBOW"]
        )

        # Compute and print mean differences
        diff_left_elbow_wrist = abs(angle_ref_left_elbow_wrist - angle_pose_left_elbow_wrist)
        diff_left_shoulder_elbow = abs(angle_ref_left_shoulder_elbow - angle_pose_left_shoulder_elbow)
        diff_right_elbow_wrist = abs(angle_ref_right_elbow_wrist - angle_pose_right_elbow_wrist)
        diff_right_shoulder_elbow = abs(angle_ref_right_shoulder_elbow - angle_pose_right_shoulder_elbow)
        diff_elbow_left = abs(elbow_angle_ref_left - elbow_angle_pose_left)
        diff_elbow_right = abs(elbow_angle_ref_right - elbow_angle_pose_right)

        if self.verbose:
            print(diff_left_elbow_wrist, diff_right_elbow_wrist, diff_left_shoulder_elbow, diff_right_shoulder_elbow, diff_elbow_left, diff_elbow_right)

        return [diff_left_elbow_wrist, diff_left_shoulder_elbow, diff_right_shoulder_elbow, diff_elbow_left, diff_elbow_right, diff_right_elbow_wrist]

    def get_best_error(self, pose):
        non_mirrored = np.mean(self.get_pos_errors(pose, "original"))
        mirrored = np.mean(self.get_pos_errors(pose, "mirrored"))
        if self.verbose:
            print("non-mirrored: ", non_mirrored)
            print("mirrored: ", mirrored)

        return min(mirrored, non_mirrored)
    
    def best_fitting_image_error(self):
        best_err, best_pic = np.inf, 0
        for i in range(0, self.nr_pictures):
            pos_dict = self.get_landmark_coords('captured_image' + str(i) + '.jpg')
            err = self.get_best_error(pos_dict)
            if best_err > err:
                best_err = err
                best_pic = i

        return best_err, best_pic
    
    def biggest_mistake(self, pic_id):
        pos_dict = self.get_landmark_coords('captured_image' + str(pic_id) + '.jpg')
        errors = self.get_pos_errors(pos_dict, "original")
        worst_error = np.argmax(errors)
        return self.ATTRIBUTES[worst_error]
    
    def detect_motion(self, threshold=100):
        # read first two frames
        ret1, frame1 = self.cap.read()
        ret2, frame2 = self.cap.read()

        print("Detecting motion... (scenario will start once detected)")

        counter = 0
        while True:
            if not ret1 and ret2:
                print("Failed to grab frames.")
                break

            # Display the current frame
            #cv2.imshow("Camera Feed", frame1)

            # Compute the absolute difference between two frames
            diff = cv2.absdiff(frame1, frame2)
            
            # Convert the difference to grayscale
            gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
            
            # Apply Gaussian blur to reduce noise
            blur = cv2.GaussianBlur(gray, (5, 5), 0)
            
            # Threshold the image to identify significant changes
            _, thresh = cv2.threshold(blur, threshold, 255, cv2.THRESH_BINARY)
            
            # Dilate the thresholded image to fill in small gaps
            dilated = cv2.dilate(thresh, None, iterations=2)
            
            # Find contours (outlines of motion)
            contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            
            # Check if any contour area is large enough to signify motion
            for contour in contours:
                if cv2.contourArea(contour) > 500:  # Adjust size as needed
                    counter+=1
                    print(counter)
                    if counter>=30:
                        return True

            # Update frames
            frame1 = frame2
            ret2, frame2 = self.cap.read()
                
        return False



