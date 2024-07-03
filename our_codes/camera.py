# import qi
# import argparse
# import os
# import sys
# import time
# from naoqi import ALProxy

# class CameraViewer(object):
#     def __init__(self, app):
#         super(CameraViewer, self).__init__()
#         app.start()
#         session = app.session
#         self.video_service = session.service("ALVideoDevice")
#         self.resolution = 2    # VGA
#         self.color_space = 11  # RGB
#         self.fps = 30          # Frames per second
#         self.name_id = None

#     def start_camera(self):
#         # Subscribe to the camera
#         self.name_id = self.video_service.subscribe("camera_viewer", self.resolution, self.color_space, self.fps)
#         print("Camera subscribed with ID:", self.name_id)

#         # Retrieve and display images
#         for i in range(50):  # Change the range value to capture more frames
#             nao_image = self.video_service.getImageRemote(self.name_id)

#             if nao_image is None:
#                 print("Failed to retrieve image")
#                 continue

#             image_width = nao_image[0]
#             image_height = nao_image[1]
#             array = nao_image[6]

#             # Print or process the image data as needed
#             print("Image width:", image_width, "Image height:", image_height)
#             # Add your image processing code here

#             time.sleep(0.1)

#         self.video_service.unsubscribe(self.name_id)
#         print("Camera unsubscribed")

#     def run(self):
#         print("Starting Camera Viewer")
#         self.start_camera()
#         print("Stopping Camera Viewer")

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--ip", type=str, default=os.environ.get('PEPPER_IP', '127.0.0.1'),
#                         help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
#     parser.add_argument("--port", type=int, default=9559,
#                         help="Naoqi port number")
#     args = parser.parse_args()

#     try:
#         connection_url = "tcp://" + args.ip + ":" + str(args.port)
#         app = qi.Application(["CameraViewer", "--qi-url=" + connection_url])
#     except RuntimeError:
#         print("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) + ".\n"
#               "Please check your script arguments. Run with -h option for help.")
#         sys.exit(1)

#     camera_viewer = CameraViewer(app)
#     camera_viewer.run()









import qi
import argparse
import sys
import os
import time
import cv2
import numpy as np
from naoqi import ALProxy

class CameraViewer(object):
    def __init__(self, app):
        super(CameraViewer, self).__init__()
        app.start()
        session = app.session
        self.video_service = session.service("ALVideoDevice")
        self.resolution = 2    # VGA
        self.color_space = 11  # RGB
        self.fps = 30          # Frames per second
        self.name_id = None

    def start_camera(self):
        # Subscribe to the camera
        self.name_id = self.video_service.subscribe("camera_viewer", self.resolution, self.color_space, self.fps)
        print("Camera subscribed with ID:", self.name_id)

        # Retrieve and display images
        for i in range(50):  # Capture 50 frames as an example
            nao_image = self.video_service.getImageRemote(self.name_id)

            if nao_image is None:
                print("Failed to retrieve image")
                continue

            image_width = nao_image[0]
            image_height = nao_image[1]
            array = nao_image[6]

            # Create a numpy array from the string
            image_string = str(bytearray(array))
            img_np = np.frombuffer(image_string, np.uint8).reshape((image_height, image_width, 3))

            # Convert image from RGB to BGR (OpenCV format)
            img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

            # Display the image
            cv2.imshow("Pepper Camera", img_bgr)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            time.sleep(0.1)

        self.video_service.unsubscribe(self.name_id)
        cv2.destroyAllWindows()
        print("Camera unsubscribed")

    def run(self):
        print("Starting Camera Viewer")
        self.start_camera()
        print("Stopping Camera Viewer")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default=os.environ.get('PEPPER_IP', '127.0.0.1'),
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")
    args = parser.parse_args()

    try:
        connection_url = "tcp://" + args.ip + ":" + str(args.port)
        app = qi.Application(["CameraViewer", "--qi-url=" + connection_url])
    except RuntimeError:
        print("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) + ".\n"
              "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    camera_viewer = CameraViewer(app)
    camera_viewer.run()
