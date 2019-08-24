# Node-Red Yolo Pets and People

## Disclaimer
The python script used in this repository is based on the fantastic work and tutorials by Adrian Rosebrock over at https://www.pyimagesearch.com. If you find this repository interesting or helpful, I would highly recommend checking out his website for much more in depth tutorials on Python image analysis and AI.

## Premises
The initial idea behind this script was to improve presence detection of people and pets in the home in conjunction with existing technologies such as PIR, Doppler, etc. Using a variety of image sources this script can process an image and provide a useful output of detected people or pets. This output could be used to switch lights and appliances on and off, set moods, change alarm status's the list goes on. Combining the power of the YOLO algorithm in python with the flexibility of node red into a basic sub flow allows just this.

## Prerequisites
While every effort was made not to have dependencies in Node-Red, the same cannot be said for the Python script. To start, the script will **only run on python 3.6.3 and above**, not python 2.7. All its dependencies will need to be installed and working before the script can operate. These dependencies are OpenCV as the pipeline to load, process, and store images, as well as argparse for passing information to the script. These can easily be installed into python using pip;

- `pip install opencv-python`
- `pip install argparse`

The OpenCV-python install requires no other installation of OpenCV be present on the host machine. This is the only downside, but if you have OpenCV installed already and working for Python the script should work out of the box.

## Usage
> Note that Python 3.6.3 and above must be installed on the machine and its directory added to PATH

To use this sub flow correctly, clone or download this repository into a known place. Then copy and import via the clipboard the Node Red Sub Flow in the Yolo-Sub-Flow.json file. This will import the flow into node red for you under the category Image Recognition. This sub flow is based entirely on built in nodes so there are no dependencies that need to be installed in Node Red. 

![Example Flow](docs/Added%20Subflow.PNG)

Using various inputs of images from Node Red via a **FTP**, **HTTP**, **Pi Camera** or other image source, the Sub Flow saves the image, then runs the Yolo.py script on that image, then outputs the result from 3 outputs. The first output of the script is a JSON object containing information on if a Person, Cat, or Dog was found. The script also saves the last analysed image and the last image with detections for extra information, and outputs them via outputs 2 and 3 respectively.

![Example Flow](docs/Used%20Subflow.PNG)

Next fill in the contextual data in the sub flow menu. The **Images Folder** option is required and points to where you would like to store the images for the instance of the sub flow. The sub flow stores the last image as *Last Image.jpg*, the last analysed image as *Last Analysed Image.jpg*, and the last image with a detected Person or Pet as *Last Object Image.jpg*. 

> Note that if the same location is used for multiple nodes then the images will be overwritten by the last used node.

The **Yolo Folder** option is required and needs to point to the Yolo Data folder in this repository, so find where you have cloned this repository to and copy the complete link such as "c:\YoloData" or "usr/YoloData". This is for the python script to find the correct .cfg, .weights, and coco .names files.

> Note that windows paths contain \ when copied, be sure to replace these with / incase anything in the script misinterpret these

The **Detection Delay** option has a default value of 5 seconds and is used to ignore incoming messages for that select period. If the Sub flow is analysing an image and a new one is presented before the time out, the message is dropped by the sub flow. 

> Note that the delay time should be larger than the inference time witnessed on your machine or else it may cause overloading of resources.

The **Recognition Confidence** settings is the confidence level an object must be in order to be recognised as true and output into the image and JSON object. The **Maxima Threshold** setting is the level of non-maxima suppression to apply after detection to eliminate overlapping bounding boxes. These settings default to 50% and 0.3 respectively. 

![Example Flow](docs/Subflow%20Options.PNG)

For each usage case of this node it is best to play around with the Confidence and Non-Maxima suppression values to find a suitable combination for your application.

## Example Flow
The Example-Flow,.json contains an example for usage with a http request, Raspberry Pi camera, and FTP server nodes. These nodes combined with the base64 encode node and image output node can produce a working example of how the Yolo sub flow works. Simply import the JSON in the file into node red and install any missing nodes from the pallet manager.

![Example Flow](docs/Sample%20Flow%20Output.PNG)

###### Required Nodes
- node-red-contrib-browser-utils
- node-red-contrib-ftp-server
- node-red-node-base64
- node-red-contrib-image-output

## Performance Expectations
The most important thing to watch for when using this sub flow is overloading your system. Every time an instance of this sub flow is sent a new image, it spawns a new instance of the script in parallel with any others that may be running. On resource constrained environments such as the Raspberry Pi, these resources will be used up quickly and may lead to the Pi not responding or crashing. Due to this the Detection Delay was added so that intermediate messages are dropped before the process has finished during that period.

Besides considering resource constraints for your application, also consider inference times. For the application of home automation, using other sensors such as PIR in conjunction with the sub flow, inference times do not have to be fast as detection can be sensed fast by the PIR then confirmed with YOLO. However, if you are trying to activate something based on the first trigger of finding a person or pet, this will become an issue on slower machines, as it can take up to 30 seconds to process an image. Below is a list of inference times tested based on the hardware I had available;

- i7 7700k @4.0GHz - 0.9 seconds
- i5 4300 @2.5GHz - 4 seconds
- intel Atom x5-z8330 @1.44GHz - 14 seconds
- raspberry pi - 32 seconds

On the faster platforms, the bottle neck comes from initilising the script more so than the inference time. On my powerful i7, the actual forward pass time on the neural net is about 450ms, the rest is loading and storing the various files. However again this is suitable in my case and may not be in yours.

I have also not tested this on a GPU, as that was not what I intended using this for. The idea was to use something like the Raspberry Pi or in my case an Intel Compute Stick which is very low power to run my node red instance. Using systems more powerful defeats the purpose of what I was trying to achieve, however it would speed up inference time drastically allowing anyone to use this in a more real time scenario. Let me know the results if you use the script this way.

## Contributing
Any ideas on how to improve anything in this repository are very welcome, I am still very much a beginner in python and could stand to learn more in java script and node red. If you end up modifying the script or the sub flow, I’d love to know.