from pathlib import Path
import cv2
import numpy as np
from skellytracker.trackers.charuco_tracker.charuco_tracker import CharucoTracker

# flag definitions -> https://docs.opencv.org/4.x/d9/d0c/group__calib3d.html#ga3207604e4b1a1758aa66acb6ed5aa65d
flags = (
            # cv2.CALIB_USE_INTRINSIC_GUESS +  #starting values for camera matrix are provided
            # cv2.CALIB_ZERO_TANGENT_DIST +  # p1 and p2 are set to zero and not changed
            cv2.CALIB_FIX_ASPECT_RATIO + # keeps fx/fy ratio constant 
            cv2.CALIB_FIX_PRINCIPAL_POINT +  # doesn't change center point
            # cv2.CALIB_FIX_FOCAL_LENGTH
            cv2.CALIB_RATIONAL_MODEL  # solves for k4, k5, k6 (adds additional points to distortion coefficients)
            # cv2.CALIB_THIN_PRISM_MODEL
            # cv2.CALIB_TILTED_MODEL
            ) # TODO: this doesn't need to be a global, just setting it here for now

def setup_5x7_tracker() -> CharucoTracker:
    charuco_squares_x_in = 7
    charuco_squares_y_in = 5
    number_of_charuco_markers = (charuco_squares_x_in - 1) * (charuco_squares_y_in - 1)
    charuco_ids = [str(index) for index in range(number_of_charuco_markers)]

    return CharucoTracker(
        tracked_object_names=charuco_ids,
        squares_x=charuco_squares_x_in,
        squares_y=charuco_squares_y_in,
        dictionary=cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250),
    )

def run_intrinsics(input_video_path: Path, output_video_path: Path):
    charuco_tracker = setup_5x7_tracker()

    board = charuco_tracker.board
    detector = charuco_tracker.charuco_detector

    all_charuco_corners = []
    all_charuco_ids = []

    all_image_points = []
    all_object_points = []

    # all_images = []

    cap = cv2.VideoCapture(str(input_video_path))

    image_size = (int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
    camera_matrix = np.array([[float(image_size[1]), 0, image_size[1] / 2], [0, float(image_size[0]), image_size[0] / 2], [0, 0, 1]])
    dist_coeffs = np.zeros((5, 1))

    all_camera_matrices = []
    all_dist_coeffs = []

    frame_number = -1
    while True:
        ret, image = cap.read()
        frame_number += 1

        if not ret:
            break

        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        current_object_points = np.array([])
        current_image_points = np.array([])

        current_charuco_corners, current_charuco_ids, _, _ = (
            detector.detectBoard(gray_image)
        )

        if current_charuco_corners is not None and len(current_charuco_corners) > 5:
            current_object_points, current_image_points = board.matchImagePoints(current_charuco_corners, current_charuco_ids, current_object_points, current_image_points)

            if not current_image_points.any() or not current_object_points.any():
                print(f"Point matching failed for frame {frame_number}.")
                continue

            print(f"Frame captured: {frame_number}")

            all_charuco_corners.append(current_charuco_corners)
            all_charuco_ids.append(current_charuco_ids)
            all_image_points.append(current_image_points)
            all_object_points.append(current_object_points)
            # all_images.append(image)

    ret, camera_matrix, dist_coeffs, _, _ = cv2.calibrateCamera(
        all_object_points, all_image_points, image_size, camera_matrix, dist_coeffs, flags=flags
    ) # TODO: only call this at the end, or every X landmarks

    print(f"Camera matrix: {camera_matrix}")
    print(f"Distortion coefficients: {dist_coeffs}")

    cap.release()


if __name__ == "__main__":
    input_video_path = Path("/Users/philipqueen/freemocap_data/recording_sessions/session_2024-06-27_15_07_36/recording_15_13_46_gmt-4_calibration/synchronized_videos/Camera_000_synchronized.mp4")
    run_intrinsics(input_video_path=input_video_path, output_video_path=None)
