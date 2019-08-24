# import the necessary packages
import numpy as np
import argparse
import time
import cv2
import os

# Start the timer 
start = time.time()

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--folder", required=True,
                help="path to input image")
ap.add_argument("-y", "--yolo", required=True,
                help="base path to YOLO directory")
ap.add_argument("-c", "--confidence", type=float, default=0.05,
                help="minimum probability to filter weak detections")
ap.add_argument("-t", "--threshold", type=float, default=0.05,
                help="threshold when applyong non-maxima suppression")
args = vars(ap.parse_args())

# Output 
personDetected = "false"
dogDetected = "false"
catDetected = "false"

# load the COCO class labels our YOLO model was trained on
labelsPath = os.path.sep.join([args["yolo"], "coco.names"])
LABELS = open(labelsPath).read().strip().split("\n")

# initialize a list of colors to represent each possible class label
# np.random.seed(42)
COLORS = np.random.randint(126, 255, size=(len(LABELS), 3),
                           dtype="uint8")

# derive the paths to the YOLO weights and model configuration
# weightsPath = os.path.sep.join([args["yolo"], "yolov2.weights"])
# configPath = os.path.sep.join([args["yolo"], "yolov2.cfg"])

weightsPath = os.path.sep.join([args["yolo"], "yolov3.weights"])
configPath = os.path.sep.join([args["yolo"], "yolov3-608.cfg"])
# configPath = os.path.sep.join([args["yolo"], "yolov3-480.cfg"])
# configPath = os.path.sep.join([args["yolo"], "yolov3-320.cfg"])

# weightsPath = os.path.sep.join([args["yolo"], "yolov3-tiny.weights"])
# configPath = os.path.sep.join([args["yolo"], "yolov3-tiny.cfg"])
# weightsPath = os.path.sep.join([args["yolo"], "yolov2-lite.weights"])
# configPath = os.path.sep.join([args["yolo"], "yolov2-lite.cfg"])

# load our YOLO object detector trained on COCO dataset (80 classes)
# print("[INFO] loading YOLO from disk...")
net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

# load our input image and grab its spatial dimensions
image = cv2.imread(os.path.sep.join([args["folder"], "Last Image.jpg"]))
# image = cv2.imread(args["folder"])
(H, W) = image.shape[:2]

# determine only the *output* layer names that we need from YOLO
ln = net.getLayerNames()
ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

# construct a blob from the input image and then perform a forward
# pass of the YOLO object detector, giving us our bounding boxes and
# associated probabilities
blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),
                             swapRB=True, crop=False)
yoloStart = time.time()
net.setInput(blob)
layerOutputs = net.forward(ln)
end = time.time()

# show timing information on YOLO
# print("[INFO] YOLO took {:.6f} seconds".format(end - yoloStart))

# initialize our lists of detected bounding boxes, confidences, and
# class IDs, respectively
boxes = []
confidences = []
classIDs = []

# loop over each of the layer outputs
for output in layerOutputs:
    # loop over each of the detections
    for detection in output:
        # extract the class ID and confidence (i.e., probability) of
        # the current object detection
        scores = detection[5:]
        classID = np.argmax(scores)
        confidence = scores[classID]

        # filter out weak predictions by ensuring the detected
        # probability is greater than the minimum probability
        if confidence > args["confidence"] : #and (classID == 0 or classID == 15 or classID == 16):
            # scale the bounding box coordinates back relative to the
            # size of the image, keeping in mind that YOLO actually
            # returns the center (x, y)-coordinates of the bounding
            # box followed by the boxes' width and height
            box = detection[0:4] * np.array([W, H, W, H])
            (centerX, centerY, width, height) = box.astype("int")

            # use the center (x, y)-coordinates to derive the top and
            # and left corner of the bounding box
            x = int(centerX - (width / 2))
            y = int(centerY - (height / 2))

            # update our list of bounding box coordinates, confidences,
            # and class IDs
            boxes.append([x, y, int(width), int(height)])
            confidences.append(float(confidence))
            classIDs.append(classID)

            # Print true for output 
            if classID == 0:
                personDetected = "true"
            if classID == 15:
                catDetected = "true"
            if classID == 16:
                dogDetected = "true"

# apply non-maxima suppression to suppress weak, overlapping bounding
# boxes
idxs = cv2.dnn.NMSBoxes(boxes, confidences, args["confidence"],
                        args["threshold"])

# ensure at least one detection exists
if len(idxs) > 0:
    # loop over the indexes we are keeping
    for i in idxs.flatten():
        # extract the bounding box coordinates
        (x, y) = (boxes[i][0], boxes[i][1])
        (w, h) = (boxes[i][2], boxes[i][3])

        # draw a bounding box rectangle and label on the image
        # color = [int(c) for c in COLORS[classIDs[i]]]
        color = (np.random.randint(0, 256), np.random.randint(
            0, 256), np.random.randint(0, 256))
        cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
        text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])
        cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, color, 2)

# Write the image
if personDetected == "true" or dogDetected == "true" or catDetected == "true":
    cv2.imwrite(os.path.sep.join([args["folder"], "Last Object Image.jpg"]), image)
cv2.imwrite(os.path.sep.join([args["folder"], "Last Analysed Image.jpg"]), image)

# Print Output
end = time.time()
print("{\"Person\":" + personDetected + ", \"Dog\":" + dogDetected + ", \"Cat\":" + catDetected + ", \"Time\":{:.6f}".format(end - start) + "}")

# show the output image
# cv2.imshow("Yolo Image", image)
# cv2.imshow("Yolo Image", cv2.resize(image, None, fx=0.5, fy=0.5))
# cv2.waitKey(1000)