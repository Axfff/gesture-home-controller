from picamera import PiCamera
from time import sleep

camera = PiCamera()
camera.start_preview(alpha=255)
camera.capture('img.jpg')
camera.stop_preview()


