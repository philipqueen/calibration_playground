from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt


def get_charuco_3d_data_from_recording(recording_path: Path) -> np.ndarray:
    data_3d = np.load(recording_path / "output_data" / "charuco_3d_xyz.npy")
    return data_3d

def plot_charuco_3d_data(data_3d: np.ndarray, undistorted_data_3d: np.ndarray, frame_range: tuple[int, int]) -> None:
    frame_step = 100
    frames = np.arange(frame_range[0], frame_range[1], frame_step)

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    ax.set_zlim(-100, 100)

    for i, frame in enumerate(frames):
        data_3d_frame = data_3d[frame, :, :]
        undistorted_data_3d_frame = undistorted_data_3d[frame, :, :]

        ax.scatter(data_3d_frame[:, 0], data_3d_frame[:, 1], data_3d_frame[:, 2], c='r', label='Original')
        ax.scatter(undistorted_data_3d_frame[:, 0], undistorted_data_3d_frame[:, 1], undistorted_data_3d_frame[:, 2], c='b', label='Undistorted')

    plt.title(f'Charuco 3D Data from Frame {frame_range[0]} to {frame_range[1]}')
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    recording_path = Path(
        "/Users/philipqueen/freemocap_data/recording_sessions/calibration_after_camera_rotation/"
    )
    undistorted_recording_path = Path(
        "/Users/philipqueen/freemocap_data/recording_sessions/calibration_after_camera_rotation_undistorted/"
    )

    frame_range = (0, 4000)

    data_3d = get_charuco_3d_data_from_recording(recording_path)
    undistorted_data_3d = get_charuco_3d_data_from_recording(undistorted_recording_path)


    data_3d = data_3d[frame_range[0]:frame_range[1]]
    undistorted_data_3d = undistorted_data_3d[frame_range[0]:frame_range[1]]

    plot_charuco_3d_data(data_3d, undistorted_data_3d, frame_range)

