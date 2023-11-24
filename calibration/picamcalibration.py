import cv2
import time
import sys
import argparse
import os
from picamera2 import Picamera2 

def save_snaps(width=0, height=0, name="snapshot", folder=".", raspi=False):
    if raspi:
        os.system('sudo modprobe bcm2835-v4l2')
    
    picam2 = PiCamera2()
    picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (width, height)}))
    picam2.start()

    try:
        if not os.path.exists(folder):
            os.makedirs(folder)
            # Création du dossier s'il n'existe pas
            try:
                os.stat(folder)
            except:
                os.mkdir(folder)
    except:
        pass

    nSnap = 0
    w, h = width, height  # Corrected variable names

    fileName = "%s/%s_%d_%d_" % (folder, name, w, h)
    while True:
        frame = picam2.capture_array()

        cv2.imshow('camera', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        if key == ord(' '):
            print("Saving image ", nSnap)
            cv2.imwrite("%s%d.jpg" % (fileName, nSnap), frame)
            nSnap += 1

    picam2.stop()
    cv2.destroyAllWindows()

def main():
    # Valeurs par défaut
    SAVE_FOLDER = "."
    FILE_NAME = "snapshot"
    FRAME_WIDTH = 2028
    FRAME_HEIGHT = 1520
    parser = argparse.ArgumentParser(
        description="Saves snapshot from the camera. \n q to quit \n spacebar to save the snapshot")
    parser.add_argument("--folder", default=SAVE_FOLDER, help="Path to the save folder (default: current)")
    parser.add_argument("--name", default=FILE_NAME, help="Picture file name (default: snapshot)")
    parser.add_argument("--dwidth", default=FRAME_WIDTH, type=int, help="<width> px (default the camera output)")
    parser.add_argument("--dheight", default=FRAME_HEIGHT, type=int, help="<height> px (default the camera output)")
    parser.add_argument("--raspi", default=False, type=bool, help="<bool> True if using a Raspberry Pi")
    args = parser.parse_args()

    SAVE_FOLDER = args.folder
    FILE_NAME = args.name
    FRAME_WIDTH = args.dwidth
    FRAME_HEIGHT = args.dheight

    save_snaps(width=args.dwidth, height=args.dheight, name=args.name, folder=args.folder, raspi=args.raspi)

    print("Files saved")

if __name__ == "__main__":
    main()
