import cv2
from call_modle import recognize_faces,prepare_modle,unload_model

def capture_face():
    cap = cv2.VideoCapture(0)
    
    print("Press C When You Are Ready To Click Picture \nPress Q If You Wanna Quit")
    
    while True:
        ret,frame = cap.read()

        if not ret:
            return False
        
        frame = cv2.flip(frame,1)
        
        cv2.imshow("frame",frame)

        if cv2.waitKey(1) == ord('c'):
            # Capture
            result = recognize_faces(frame)
            cv2.destroyAllWindows()
            
            if isinstance(result,str):
                if result == "Multiple Faces Detected":
                    return result
                elif result == "No Faces Found":
                    return result
            else:
                return result

if __name__ == "__main__":
    prepare_modle()
    print(capture_face())
    unload_model()
    
    