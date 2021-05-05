import sys
sys.path.append('./object_detection/yolov3_pytorch')
sys.path.append('./object_detection/yolov3_opencv')
import cv2
import queue
import numpy as np
import requests
import imutils
import torch
import urllib.request
import matplotlib.pyplot as plt

from PIL import Image

# https://stackoverflow.com/questions/12984426/python-pil-ioerror-image-file-truncated-with-big-images
Image.LOAD_TRUNCATED_IMAGES = True

# from object_detection import ObjectDetection 
# from image_dataset import SingleImage

class Camera():
    url = 'http://192.168.4.70:8080/shot.jpg'
    locations_stream = queue.Queue()

    def __init__(self):
        pass

    # yolov3 version I wrote in PyTorch. This is slower than the ones below.
    def stream_yolov3_personal(self):
        net = ObjectDetection(conf_thresh=0.8, nms_thresh=0.4)
        while True:
            frame = Image.open(requests.get(self.url, stream=True).raw).convert('RGB')
            image, scale, padding = SingleImage(frame)[0]
            image = torch.unsqueeze(image, 0)
            detections = net.detect(image, scale, padding)
            image_with_detections = net.draw_result(frame, detections[0], show=False)
            opencvImage = cv2.cvtColor(np.array(image_with_detections), cv2.COLOR_RGB2BGR)
            # show the frame to our screen
            cv2.imshow("Frame", opencvImage)
            key = cv2.waitKey(1) & 0xFF
            # if the 'q' key is pressed, stop the loop
            if key == ord("q"):
                break

        # close all windows
        cv2.destroyAllWindows()


    # yolov3 version I found online for openCV. This is faster than the one above.
    # https://medium.com/analytics-vidhya/object-detection-with-opencv-python-using-yolov3-481f02c6aa35
    def stream_yolov3_opencv(self):
        net = cv2.dnn.readNet("./object_detection/yolov3_opencv/yolov3.weights","./object_detection/yolov3_opencv/yolov3.cfg")
        classes = []
        with open("./object_detection/yolov3_opencv/coco.names","r") as f:
            classes = [line.strip() for line in f.readlines()]
        layer_names = net.getLayerNames()
        outputlayers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
        colors= np.random.uniform(0,255,size=(len(classes),3))

        while True:
            # frame = Image.open(requests.get(self.url, stream=True).raw).convert('RGB')
            frame = urllib.request.urlopen(self.url)
            # Numpy to convert into a array
            frame = np.array(bytearray(frame.read()),dtype=np.uint8)
            # Decode the array to OpenCV usable format
            frame = cv2.imdecode(frame,-1)
            # frame = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)
            img = cv2.resize(frame,None,fx=0.5,fy=0.5)
            height, width, channels = img.shape

            #detecting objects
            blob = cv2.dnn.blobFromImage(img,0.00392,(416,416),(0,0,0),True,crop=False)
            net.setInput(blob)
            outs = net.forward(outputlayers)

            #Showing info on screen/ get confidence score of algorithm in detecting an object in blob
            class_ids=[]
            confidences=[]
            boxes=[]
            for out in outs:
                for detection in out:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    if confidence > 0.5:
                        #object detected
                        center_x= int(detection[0]*width)
                        center_y= int(detection[1]*height)
                        w = int(detection[2]*width)
                        h = int(detection[3]*height)
                    
                        #cv2.circle(img,(center_x,center_y),10,(0,255,0),2)
                        #rectangle co-ordinaters
                        x=int(center_x - w/2)
                        y=int(center_y - h/2)
                        #cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
                        
                        boxes.append([x,y,w,h]) #put all rectangle areas
                        confidences.append(float(confidence)) #how confidence was that object detected and show that percentage
                        class_ids.append(class_id) #name of the object that was detected

            indexes = cv2.dnn.NMSBoxes(boxes,confidences,0.4,0.6)

            font = cv2.FONT_HERSHEY_PLAIN
            valid_detections = []
            for i in range(len(boxes)):
                if i in indexes:
                    x,y,w,h = boxes[i]
                    label = str(classes[class_ids[i]])
                    if label == 'person':
                        valid_detections.append([x,y,w,h,label])
                    color = colors[i]
                    cv2.rectangle(img,(x,y),(x+w,y+h),color,2)
                    cv2.putText(img,label,(x,y+30),font,1,(255,255,255),2)
            self.locations_stream.put(valid_detections)     
            # show the frame to our screen
            cv2.imshow("Frame", img)
            key = cv2.waitKey(1) & 0xFF
            # if the 'q' key is pressed, stop the loop
            if key == ord("q"):
                break

        # close all windows
        cv2.destroyAllWindows()

    # https://pytorch.org/hub/ultralytics_yolov5/
    def stream_yolov5_ultralytics(self):
        # Model
        model = torch.hub.load('ultralytics/yolov5', 'yolov5s', force_reload=True)
        while True:
            frame = Image.open(requests.get(self.url, stream=True).raw).convert('RGB')
            image_with_detections = model(frame, size=640)  # includes NMS
            image_with_detections = image_with_detections.render()
            opencvImage = cv2.cvtColor(image_with_detections[0], cv2.COLOR_RGB2BGR)
            # show the frame to our screen
            cv2.imshow("Frame", opencvImage)
            key = cv2.waitKey(1) & 0xFF
            # if the 'q' key is pressed, stop the loop
            if key == ord("q"):
                break

        # close all windows
        cv2.destroyAllWindows()

    # https://pytorch.org/hub/intelisl_midas_v2/
    # https://towardsdatascience.com/depth-estimation-1-basics-and-intuition-86f2c9538cd1
    def stream_depth_map(self):
        # Model
        use_large_model = False

        if use_large_model:
            midas = torch.hub.load("intel-isl/MiDaS", "MiDaS")
        else:
            midas = torch.hub.load("intel-isl/MiDaS", "MiDaS_small")

        device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
        midas.to(device)
        midas.eval()   

        midas_transforms = torch.hub.load("intel-isl/MiDaS", "transforms")

        if use_large_model:
            transform = midas_transforms.default_transform
        else:
            transform = midas_transforms.small_transform
        while True:
            # Use urllib to get the image from the IP camera
            imgResp = urllib.request.urlopen(self.url)

            # Numpy to convert into a array
            imgNp = np.array(bytearray(imgResp.read()),dtype=np.uint8)

            # Decode the array to OpenCV usable format
            img = cv2.imdecode(imgNp,-1)

            # url, filename = ("https://github.com/pytorch/hub/raw/master/images/dog.jpg", "dog.jpg")
            # urllib.request.urlretrieve(url, filename)

            # img = cv2.imread(filename)
            # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            input_batch = transform(img).to(device)
            with torch.no_grad():
                prediction = midas(input_batch)

                prediction = torch.nn.functional.interpolate(
                    prediction.unsqueeze(1),
                    size=img.shape[:2],
                    mode="bicubic",
                    align_corners=False,
                ).squeeze()
                
            output = prediction.cpu().numpy()
            # print(output)

            # plt.imshow(output)
            # plt.show()

            depth_map_show = None
            depth_map_show = cv2.normalize(output, depth_map_show, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
            depth_map_show = cv2.applyColorMap(depth_map_show, cv2.COLORMAP_JET)

            # show the frame to our screen
            cv2.imshow("Depth Map", depth_map_show)
            key = cv2.waitKey(1) & 0xFF
            # if the 'q' key is pressed, stop the loop
            if key == ord("q"):
                break

            # close all windows
            cv2.destroyAllWindows()
            
    def stream_ball_locations(self):
        # define the lower and upper boundaries of the "green"
        # ball in the HSV color space, then initialize the
        # list of tracked points
        greenLower = (29, 86, 6)
        greenUpper = (64, 255, 255)

        # keep looping
        while True:
             # Use urllib to get the image from the IP camera
            imgResp = urllib.request.urlopen(self.url)

            # Numpy to convert into a array
            imgNp = np.array(bytearray(imgResp.read()),dtype=np.uint8)

            # Decode the array to OpenCV usable format
            frame = cv2.imdecode(imgNp,-1)
            # resize the frame, blur it, and convert it to the HSV
            # color space
            # frame size is 600 x 337 (w x h)
            frame = cv2.resize(frame, None, fx=3, fy=3, interpolation=cv2.INTER_LINEAR)
            frame = imutils.resize(frame, width=600)
            blurred = cv2.GaussianBlur(frame, (11, 11), 0)
            hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
            # construct a mask for the color "green", then perform
            # a series of dilations and erosions to remove any small
            # blobs left in the mask
            mask = cv2.inRange(hsv, greenLower, greenUpper)
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)

            # find contours in the mask and initialize the current
            # (x, y) center of the ball
            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            locations_in_frame = []

            # for c in cnts:
            if len(cnts) > 0:
                c = max(cnts, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                # only proceed if the radius meets a minimum size
                if radius > 10:
                    # draw the circle and centroid on the frame,
                    # then update the list of tracked points
                    cv2.circle(frame, (int(x), int(y)), int(radius),
                        (0, 255, 255), 2)
                    cv2.circle(frame, (int(x), int(y)), 5, (0, 0, 255), -1)
                    locations_in_frame.append([x, y, radius])
            self.locations_stream.put(locations_in_frame)

            # show the frame to our screen
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF
            # if the 'q' key is pressed, stop the loop
            if key == ord("q"):
                break
            
        # close all windows
        cv2.destroyAllWindows()