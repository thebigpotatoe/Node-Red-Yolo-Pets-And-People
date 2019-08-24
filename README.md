# Node-Red-Yolo-Script

The pythin script used in this repository is based on the fantastic work and tutorials by Ardian Rosebrock over at https://www.pyimagesearch.com. If you find this repository interesting or helpful i would highly recomend checking out his website for much more in depth tutorials on Python image analysis and AI.

The initial idea behind this script to detect eithe people or pets in a home and provide a useful output if they were detected. Combining the power of the YOLO algorithim in python with the flexibility of node red into a basic subflow allows just this.

Using various inputs of images from Node red via a FTP, HTTP, Pi Camera or other image source, the script takes the image, saves it, then runs the Yolo.py script on that image. The output of the script is a JSOM object contatining information on if a Person, Cat, or Dog was found. The script also saves the last analysed image and the last image with detections for extra information.

To use this subflow correctly, clone or download this repository into a known place, remeber where this is as we will be refering to it later. 

Then copy and import via the clipboard the Node Red Subflow in the .json file. This will import the flow into node red for you. This sub flow is based entirely on built in nodes so there are no dependencies that need to be downloaded. 

Next fill in the contextual data in the sub flow menu. This is where you point the sub flow to the location of the Yolo cfg, weights, and coco names files that are included in this repository. Next the file location is where you can choose to place the saved images from the script for analysis and output. These files are overwritten each time the script is run, so put them somewhere that can be accessed quckily such as an SSD drive for better perfromance.

The other settings are for thresholds in the algorithim. These are the confidence limit for the miniumum accepted probability of a detection to be true, NMS limit for the non maxima suppression limt and delay time between inferences.

- Explain each of the settings in teh subflow in more details 


- Example flow 
- Performance 
- Suggestions and usage ideas
