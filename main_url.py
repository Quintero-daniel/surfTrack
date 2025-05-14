import cv2
import streamlink

def main():
    streams = streamlink.streams("https://www.twitch.tv/caseoh_")
    if 'best' in streams:
        cap = cv2.VideoCapture(streams['best'].url)
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imshow("Frame", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
    else:
        print("No streams available")

if __name__ == "__main__":
    main()