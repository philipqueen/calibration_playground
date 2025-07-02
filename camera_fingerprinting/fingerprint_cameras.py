import cv2

def fingerprint_camera(cap: cv2.VideoCapture, port: int) -> int:
    
    camera_id = int(cap.get(cv2.CAP_PROP_GUID))
    return camera_id

if __name__ == "__main__":
    port = 0 
    cap = cv2.VideoCapture(port)
    print(fingerprint_camera(cap, port))

    cap.release()
    
    port = 1 
    cap = cv2.VideoCapture(port)
    print(fingerprint_camera(cap, port))    
    cap.release()