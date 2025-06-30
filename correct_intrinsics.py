import json
from pathlib import Path

import cv2
import numpy as np

cam_to_intrinsics_path_map = {
    24676894: "/Users/philipqueen/basler_intrinsics/Basler_acA1300-200um__24676894__20250625_112826560_intrinsics.json",
    24908831: "/Users/philipqueen/basler_intrinsics/Basler_acA2040-90umNIR__24908831__20250625_113806886_intrinsics.json",
    24908832: "/Users/philipqueen/basler_intrinsics/Basler_acA2040-90umNIR__24908832__20250625_113856144_intrinsics.json",
    25000609: "/Users/philipqueen/basler_intrinsics/Basler_acA2040-90umNIR__25000609__20250625_114031910_intrinsics.json",
    25006505: "/Users/philipqueen/basler_intrinsics/Basler_acA2040-90umNIR__25006505__20250625_114110681_intrinsics.json"
}


def save_corrected_video(
    input_video_path: Path,
    output_video_path: Path,
    camera_matrix: np.ndarray,
    dist_coeffs: np.ndarray,
):
    print("Saving corrected video...")
    cap = cv2.VideoCapture(str(input_video_path))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

    include_all_pixels = 1 # 1: all pixels are retained with some extra black in margins, 0: only valid pixels are shown
    # we can do 1 here because we crop it down anyways

    new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, dist_coeffs, (width, height), include_all_pixels, (width, height))
    x, y, w, h = roi

    out = cv2.VideoWriter(
        str(output_video_path),
        cv2.VideoWriter.fourcc(*"mp4v"),
        cap.get(cv2.CAP_PROP_FPS),
        (w, h),
    )

    while True:
        ret, image = cap.read()

        if not ret:
            break

        corrected_image = cv2.undistort(image, camera_matrix, dist_coeffs, None, new_camera_matrix)
        cropped_corrected_image = corrected_image[y:y+h, x:x+w]

        # cv2.imshow("Corrected Image", cropped_corrected_image)
        # cv2.waitKey(1)
        out.write(cropped_corrected_image)

    cap.release()
    out.release()

    print(f"Corrected video saved to {output_video_path}")

def get_calibration_from_json(json_path: Path) -> tuple[np.ndarray, np.ndarray]:
    with open(json_path, "r") as f:
        data = json.load(f)

    camera_matrix = np.array(data["camera_matrix"])
    dist_coeffs = np.array(data["distortion_coefficients"])

    return camera_matrix, dist_coeffs

def run_intrinsic_correction(
    input_video_path: Path,
    output_video_path: Path,
    json_path: Path
):
    camera_matrix, dist_coeffs = get_calibration_from_json(json_path)

    print(f"Camera matrix: {camera_matrix}")
    print(f"Distortion coefficients: {dist_coeffs}")

    save_corrected_video(
        input_video_path=input_video_path,
        output_video_path=output_video_path,
        camera_matrix=camera_matrix,
        dist_coeffs=dist_coeffs,
    )

if __name__ == "__main__":
    synchronized_video_path = Path(
        "/Users/philipqueen/calibration_AFTER_CAMERA_ROTATION/synchronized_videos/"
    )
    output_video_path = synchronized_video_path.parent / "undistorted_videos"
    output_video_path.mkdir(exist_ok=True)

    for video in synchronized_video_path.glob("*.mp4"):
        camera_id = int(video.stem)
        json_path = Path(cam_to_intrinsics_path_map[camera_id])

        if not json_path.exists():
            print(f"Calibration data for camera {camera_id} not found at {json_path}. Skipping video {video}.")
            continue

        output_video = output_video_path / f"{video.stem}_corrected.mp4"
        run_intrinsic_correction(video, output_video, json_path)