from pypylon import pylon
import cv2
import numpy
import time
from CommonAssit import PathFileControl
import threading

camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

camera.Open()

print("DeviceClass: ", camera.GetDeviceInfo().GetDeviceClass())
print("DeviceFactory: ", camera.GetDeviceInfo().GetDeviceFactory())
print("ModelName: ", camera.GetDeviceInfo().GetModelName())

############################################################
Hardware_Trigger = True

if Hardware_Trigger:
    # reset registration
    camera.RegisterConfiguration(pylon.ConfigurationEventHandler(), pylon.RegistrationMode_ReplaceAll, pylon.Cleanup_Delete)

# The parameter MaxNumBuffer can be used to control the count of buffers
# allocated for grabbing. The default value of this parameter is 10.
camera.MaxNumBuffer = 5

# set exposure time
# camera.ExposureTimeRaw.SetValue(100)

# Select the Frame Start trigger
camera.TriggerSelector.SetValue('FrameStart')
# Acquisition mode
camera.AcquisitionMode.SetValue('Continuous')
# Enable triggered image acquisition for the Frame Start trigger
camera.TriggerMode.SetValue('On')
# Set the trigger source to Line 1
camera.TriggerSource.SetValue('Line1')
# Set the trigger activation mode to rising edge
camera.TriggerActivation.SetValue('RisingEdge')
# Set the delay for the frame start trigger to 300 µs
# camera.TriggerDelayAbs.SetValue(300.0)
# Pixel format
# camera.PixelFormat.SetValue('Mono8')

##############################################################

camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
converter = pylon.ImageFormatConverter()

converter.OutputPixelFormat = pylon.PixelType_BGR8packed
converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

count_trigger = 1
count_image =1

time_0 = time.time()
PathFileControl.generatePath("./save_images")

def saveImageThread(count_image, img):
    cv2.imencode(".png", img)[1].tofile('./save_images/%06d.png' % count_image)
    # cv2.imwrite('./save_images/%06d.png' % count_image, img)
grabResult = None
while camera.IsGrabbing():
    print("count_trigger: ", count_trigger)
    count_trigger += 1
    try:
        grabResult = camera.RetrieveResult(1000, pylon.TimeoutHandling_ThrowException)

        if grabResult.GrabSucceeded():
            print("grabResult is succeeded!")
            # Access the image data
            image = converter.Convert(grabResult)
            img = image.GetArray()
            # img = cv2.resize(img,(100, 200))
            # cv2.imshow("image", img)
            thread = threading.Thread(target=saveImageThread, args=(count_image, img))
            thread.start()
            # cv2.imwrite('./save_images/%06d.png'%count_image, img)
            # print("%06d.png saved"%count_image)
            count_image += 1

        grabResult.Release()
    except:
        if grabResult is not None:
            grabResult.Release()
        count_trigger -= 1
        continue


camera.StopGrabbing()
print("end")