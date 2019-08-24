# Node-Red-Yolo-Script

## Disclaimer
The python script used in this repository is based on the fantastic work and tutorials by Ardian Rosebrock over at https://www.pyimagesearch.com. If you find this repository interesting or helpful I would highly recomend checking out his website for much more in depth tutorials on Python image analysis and AI.

## Premisis
The initial idea behind this script was to improve presence detection of people and pets in the home in conjunction with existining technologies such as PIR, Doplar, etc. Using a variuety of image sources this script can proccess an image and provide a useful output of detected people or pets. This output could be used to switch lights and appliances on and off, set moods, change alarm status's the list goes on. Combining the power of the YOLO algorithim in python with the flexibility of node red into a basic subflow allows just this.

## Usage
Using various inputs of images from Node red via a FTP, HTTP, Pi Camera or other image source, the script takes the image, saves it, then runs the Yolo.py script on that image. The output of the script is a JSOM object contatining information on if a Person, Cat, or Dog was found. The script also saves the last analysed image and the last image with detections for extra information.

To use this subflow correctly, clone or download this repository into a known place, remeber where this is as we will be refering to it later. 

Then copy and import via the clipboard the Node Red Subflow in the .json file. This will import the flow into node red for you. This sub flow is based entirely on built in nodes so there are no dependencies that need to be downloaded. 

Next fill in the contextual data in the sub flow menu. This is where you point the sub flow to the location of the Yolo cfg, weights, and coco names files that are included in this repository. Next the file location is where you can choose to place the saved images from the script for analysis and output. These files are overwritten each time the script is run, so put them somewhere that can be accessed quckily such as an SSD drive for better perfromance.

The other settings are for thresholds in the algorithim. These are the confidence limit for the miniumum accepted probability of a detection to be true, NMS limit for the non maxima suppression limt and delay time between inferences.

- Explain each of the settings in teh subflow in more details 

## Example Flow
###### Required Nodes
- node-red-contrib-browser-utils
- node-red-contrib-ftp-server
- node-red-node-base64
- node-red-contrib-image-output

The Example-Flow,.json contains an example for usage with a http request, raspberry pi camera, and FTP server nodes. These nodes combined with the base64 encode node and image output node can produce a working example of how the Yolo sub flow works. Simply import the JSON in the file into node red and install any missing nodes from the pallet manager.

[Example Flow](https://github.com/thebigpotatoe/Node-Red-Yolo-Script/blob/master/docs/Sample%20Flow%20Output.PNG)

## Performance Expectations
The most important thing to watch for when using this subflow is overloading your system. Every time the node is sent a new image, it spawns a new instance of the script in parallel with any others that may be running. On resource constrained environemnts such as the raspberry pi, these resources will be used up quickly and may lead to the pi not responding or crashing. Due to this the Detection Delay was added so that intermediate messages are dropped before the proccess has finsihed during that period.

Besides considering resaource constaraints for your application, also consider inference times. For the application of home automation in conjunction with other sensors, inference times do not have to be fast. however if you are trying to activate something based on the first trigger of finding a person or pet, this will become an issue. Below is a list of inference times tested based on the hardware I had available.

- i7 7700k @4.0GHz - 900ms
- i5 @2.4GHz - 
- intel Atom x5-z8330 @1.44GHz - 14 seconds
- raspberry pi - 32 seconds

## Contributing
Any ideas on how to improve anything in this repository are very welcome, I am still very much a begeiner in python and could stand to learn more in java script and node red.
