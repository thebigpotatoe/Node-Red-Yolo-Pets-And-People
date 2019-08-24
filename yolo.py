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

# Import the COCO class labels and create some label colours
labelsPath = os.path.sep.join([args["yolo"], "coco.names"])
LABELS = open(labelsPath).read().strip().split("\n")
COLORS = np.random.randint(126, 255, size=(len(LABELS), 3), dtype="uint8")

# Import the model CFG and Weights
weightsPath = os.path.sep.join([args["yolo"], "yolov3.weights"])
configPath = os.path.sep.join([args["yolo"], "yolov3.cfg"])
net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

# Determine only the *output* layer names that we need from YOLO
ln = net.getLayerNames()
ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

# Import the latest frame from the specified folder
image = cv2.imread(os.path.sep.join([args["folder"], "Last Image.jpg"]))
(H, W) = image.shape[:2]

# initialize our lists of detected bounding boxes, confidences, and# class IDs
boxes = []
confidences = []
classIDs = []

# Forward pass on the network
blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
net.setInput(blob)
layerOutputs = net.forward(ln)

# Loop over each of the layer outputs
for output in layerOutputs:
    # loop over each of the detections
    for detection in output:
        # extract the class ID and confidence
        scores = detection[5:]
        classID = np.argmax(scores)
        confidence = scores[classID]

        # Filter Detections and find bounding box
        if confidence > args["confidence"] : # and (classID == 0 or classID == 15 or classID == 16):
            # find bouding boxes
            box = detection[0:4] * np.array([W, H, W, H])
            (centerX, centerY, width, height) = box.astype("int")
            x = int(centerX - (width / 2))
            y = int(centerY - (height / 2))
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

# apply non-maxima suppression 
idxs = cv2.dnn.NMSBoxes(boxes, confidences, args["confidence"], args["threshold"])

# Put coloured bounding boxes over the image
if len(idxs) > 0:
    # loop over the indexes we are keeping
    for i in idxs.flatten():
        # extract the bounding box coordinates
        (x, y) = (boxes[i][0], boxes[i][1])
        (w, h) = (boxes[i][2], boxes[i][3])

        # draw a bounding box rectangle
        color = (np.random.randint(0, 256), np.random.randint(0, 256), np.random.randint(0, 256))
        cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
        text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])
        cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,0.5, color, 2)

# Write the image back to specified folder
if personDetected == "true" or dogDetected == "true" or catDetected == "true":
    cv2.imwrite(os.path.sep.join([args["folder"], "Last Object Image.jpg"]), image)
cv2.imwrite(os.path.sep.join([args["folder"], "Last Analysed Image.jpg"]), image)

# Print Output
end = time.time()
print("{\"Person\":" + personDetected + ", \"Dog\":" + dogDetected + ", \"Cat\":" + catDetected + ", \"Time\":{:.6f}".format(end - start) + "}")
