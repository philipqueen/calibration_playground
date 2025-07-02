# Based on https://github.com/chinaheyu/cv2_enumerate_cameras/blob/main/cv2_enumerate_cameras/macos_backend.py
# and reimplementing parts of https://github.com/opencv/opencv/blob/66e5fce9282fb2a9daaec9a79e0e7ed8bb01db06/modules/videoio/src/cap_avfoundation_mac.mm#L360

import re
import time
import AVFoundation


from cv2_enumerate_cameras.camera_info import CameraInfo

try:
    import cv2

    CAP_AVFOUNDATION = cv2.CAP_AVFOUNDATION
except ModuleNotFoundError:
    CAP_AVFOUNDATION = 1200

supported_backends = (CAP_AVFOUNDATION,)


def cameras_generator(apiPreference):
    _VID_RE = re.compile(r"VendorID_(\d+)")
    _PID_RE = re.compile(r"ProductID_(\d+)")

    devs = AVFoundation.AVCaptureDevice.devicesWithMediaType_(
        AVFoundation.AVMediaTypeVideo
    )

    devs = devs.arrayByAddingObjectsFromArray_(
        AVFoundation.AVCaptureDevice.devicesWithMediaType_(
            AVFoundation.AVMediaTypeMuxed
        )
    )

    devs = list(devs)

    print(f"Found {len(devs)} devices")
    print(f"type of devices: {type(devs)}")

    devs.sort(key=lambda d: d.uniqueID())

    print(devs)

    # for i, device in enumerate(devs):
    #     print(f"Device {i}: {device.localizedName()}")
    #     cap = cv2.VideoCapture(i, apiPreference)

    #     for i in range(10):
    #         ret, frame = cap.read()  # Attempt to read from the device to initialize it

    #         if ret:
    #             cv2.imshow(f"Device {i}: {device.localizedName()}", frame)
    #             cv2.waitKey(1)
    #         else:
    #             print(f"Device {i} failed to read frame. It may not be available or not supported by OpenCV.")

    #     cap.release()
    for i, d in enumerate(devs):
        model = str(d.modelID())
        vid_m = _VID_RE.search(model)
        pid_m = _PID_RE.search(model)

        # success = d.lockForConfiguration_(None)  # Lock the device for configuration
        # if success:
        #     print(f"Configuring device {i}: {d.localizedName()}")
        #     for index in range(3):
        #         cap = cv2.VideoCapture(index, apiPreference)
        #         if cap.isOpened():
        #             print(f"Device {i} is opened with index {index}")
        #             cap.set(cv2.CAP_PROP_FPS, 30)
        #         else:
        #             print(f"Device {i} failed to open with index {index}")
        #             time.sleep(0.1)
        #         cap.release()
        # else:
        #     print(f"Failed to lock device {i}: {d.localizedName()}")
        # d.unlockForConfiguration()

        # print(f"Device {i}: {d}")
        print(f"  localizedName: {d.localizedName()}")
        print(f"  manufacturer: {d.manufacturer()}")
        print(f"  deviceType: {d.deviceType()}")
        print(f"  modelID: {d.modelID()}")
        print(f"  position: {d.position()}") # position only works for iOS (front, back, other)
        print(f"  uniqueID: {d.uniqueID()}")  # unique ID persists across time (https://developer.apple.com/documentation/avfoundation/avcapturedevice/uniqueid)
        # just need a way to get the unique ID based on openCV port number

        # print(f'device connected: {d.isConnected()}')
        # print(f"device in use: {d.isInUseByAnotherApplication()}")

        # if d.isInUseByAnotherApplication():
        #     raise RuntimeError(
        #         f"Device {d.localizedName()} is in use by another application. "
        #         "Please close the application and try again."
        #     )
        # # print(f' session running: {d.session.running()}')

        yield CameraInfo(
            index=d.position(),
            name=d.localizedName(),
            path=None,  # macOS does not provide a path
            vid=int(vid_m.group(1)) if vid_m else None,
            pid=int(pid_m.group(1)) if pid_m else None,
            backend=apiPreference,
        )


__all__ = ["supported_backends", "cameras_generator"]

if __name__ == "__main__":

    for c in cameras_generator(CAP_AVFOUNDATION):
        print(c)

    # cap = cv2.VideoCapture(2, CAP_AVFOUNDATION)
    # time.sleep(5)  # wait for camera to initialize
    # cap.release()
