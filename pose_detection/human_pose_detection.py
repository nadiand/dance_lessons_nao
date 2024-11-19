
# import necessary packages

import cv2
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

# # For static images:
def cords(file):
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

        annotated_image = image.copy()
        # Draw segmentation on the image.
        # To improve segmentation around boundaries, consider applying a joint
        # bilateral filter to "results.segmentation_mask" with "image".
        condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
        bg_image = np.zeros(image.shape, dtype=np.uint8)
        bg_image[:] = BG_COLOR
        annotated_image = np.where(condition, annotated_image, bg_image)
        # # Draw pose landmarks on the image.
        # mp_drawing.draw_landmarks(
        #     annotated_image,
        #     results.pose_landmarks,
        #     mp_pose.POSE_CONNECTIONS,
        #     landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
        # cv2.imwrite('/tmp/annotated_image' + '.png', annotated_image)
        # # Plot pose world landmarks.
        # mp_drawing.plot_landmarks(
        #     results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS)
    
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

def mean_difference(reference, dict, verbose=False):
    reference_list = []
    original_list = []
    mirrored_list = []

    for mirror_key in reference:
      if mirror_key == "original":
        for point in reference[mirror_key]:
           for coord in reference[mirror_key][point]:
              reference_list.append(reference[mirror_key][point][coord])
              original_list.append(dict[mirror_key][point][coord])
      else:
         for point in reference[mirror_key]:
           for coord in reference[mirror_key][point]:
              mirrored_list.append(dict[mirror_key][point][coord])

    reference_arr = np.array(reference_list)
    original_arr = np.array(original_list)
    mirrored_arr = np.array(mirrored_list)
 
    mean_error_original = abs(reference_arr-original_arr).mean()
    mean_error_mirrored = abs(reference_arr-mirrored_arr).mean()

    if verbose:
       print("original: ", mean_error_original)
       print("mirrored: ", mean_error_mirrored)
    return mean_error_original, mean_error_mirrored

def get_angle(point1, point2):
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

def get_angle_between_lines(point1, point2, shared_point):
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



shit = cords('./pictures/shit.jpg')
not_shit = cords('./pictures/not_shit.jpg')
reference = cords('./pictures/reference.jpg')
dab = cords('./pictures/dab.jpg')
bad = cords('./pictures/bad.jpg')
passed = cords('./pictures/pass.jpg')

# print("shit")
# mean_difference(reference, shit, verbose=True)
# print("not_shit")
# mean_difference(reference, not_shit, verbose=True)
# print("dab")
# mean_difference(reference, dab, verbose=True)
# print("bad")
# mean_difference(reference, bad, verbose=True)
# print("passed")
# mean_difference(reference, passed, verbose=True)
# print("reference")
# mean_difference(reference, reference, verbose=True)

print(get_angle(reference["original"]["LEFT_WRIST"],reference["original"]["LEFT_ELBOW"]))
print(get_angle(reference["original"]["LEFT_ELBOW"],reference["original"]["LEFT_SHOULDER"]))
print(get_angle(reference["original"]["RIGHT_ELBOW"],reference["original"]["RIGHT_SHOULDER"]))
print(get_angle(shit["original"]["LEFT_ELBOW"],shit["original"]["LEFT_WRIST"]))
print(get_angle(shit["original"]["RIGHT_ELBOW"],shit["original"]["RIGHT_WRIST"]))
print("angle elbow: ", get_angle_between_lines(reference["original"]["LEFT_WRIST"],reference["original"]["LEFT_SHOULDER"],reference["original"]["LEFT_ELBOW"]))
print("angle elbow: ", get_angle_between_lines(shit["original"]["RIGHT_WRIST"],shit["original"]["RIGHT_SHOULDER"],shit["original"]["RIGHT_ELBOW"]))


# print(reference-dab)
# print((reference-dab).mean())
# print((reference-mdab).mean())
# print((reference-shit).mean())
# print((reference-mshit).mean())
# print((reference-bad).mean())
# print((reference-mbad).mean())
# print((reference-passed).mean())
# print((reference-mpassed).mean())

# For webcam input:
# cap = cv2.VideoCapture(0)
# with mp_pose.Pose(
#     min_detection_confidence=0.5,
#     min_tracking_confidence=0.5) as pose:
#   print("test")
#   while cap.isOpened():
#     success, image = cap.read()
#     if not success:
#       print("Ignoring empty camera frame.")
#       # If loading a video, use 'break' instead of 'continue'.
#       continue

#     # To improve performance, optionally mark the image as not writeable to
#     # pass by reference.
#     image.flags.writeable = False
#     image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#     results = pose.process(image)
#     if results.pose_landmarks is not None:
#       print(results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].x)
#     # print(results.pose_landmarks)

#     # Draw the pose annotation on the image.
#     image.flags.writeable = True
#     image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
#     mp_drawing.draw_landmarks(
#         image,
#         results.pose_landmarks,
#         mp_pose.POSE_CONNECTIONS,
#         landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
#     # Flip the image horizontally for a selfie-view display.
#     cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
#     if cv2.waitKey(5) & 0xFF == 27:
#       break
# cap.release()
