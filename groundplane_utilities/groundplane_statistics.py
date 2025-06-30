from pathlib import Path

import numpy as np

def get_z_values(data_3d: np.ndarray, frame_range: tuple[int, int]) -> np.ndarray:
    # data_3d = filter_z_values(data_3d)
    return data_3d[frame_range[0]:frame_range[1], :, 2]

def filter_z_values(z_values: np.ndarray, threshold: float = 50) -> np.ndarray:
    """
    remove values greater than threshold and less than -threshold
    """
    return np.where(
        (z_values > threshold) | (z_values < -threshold),
        np.nan,
        z_values
    )
    
def get_charuco_3d_data_from_recording(recording_path: Path) -> np.ndarray:
    data_3d = np.load(recording_path / "output_data" / "charuco_3d_xyz.npy")
    return data_3d

def print_z_values_statistics(data_3d: np.ndarray, frame_range: tuple[int, int]) -> None:
    z_values = get_z_values(data_3d, frame_range)
    for i in range(z_values.shape[1]):
        print(f"Z values for marker {i}:")
        print(f"\tMin: {np.nanmin(z_values[:, i])}")
        print(f"\tMax: {np.nanmax(z_values[:, i])}")
        print(f"\tMean: {np.nanmean(z_values[:, i])}")
        print(f"\tMedian: {np.nanmedian(z_values[:, i])}")
        print(f"\tStd Dev: {np.nanstd(z_values[:, i])}\n")
    
    print("Mean Z value across all markers:")
    mean_z = np.nanmean(z_values, axis=1)
    print(f"\tMin: {np.nanmin(mean_z)}")
    print(f"\tMax: {np.nanmax(mean_z)}")
    print(f"\tMean: {np.nanmean(mean_z)}")
    print(f"\tMedian: {np.nanmedian(mean_z)}")
    print(f"\tStd Dev: {np.nanstd(mean_z)}")

def main(recording_path: Path, frame_range: tuple[int, int]) -> None:
    data_3d = get_charuco_3d_data_from_recording(recording_path)
    print_z_values_statistics(data_3d, frame_range)

if __name__ == '__main__':
    # recording_path = Path(
    #     "/Users/philipqueen/freemocap_data/recording_sessions/calibration_after_camera_rotation/"
    # )
    recording_path = Path(
        "/Users/philipqueen/freemocap_data/recording_sessions/calibration_after_camera_rotation_undistorted/"
    )

    frame_range = (0, 4000)

    main(recording_path, frame_range)