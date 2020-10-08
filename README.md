# becalm-station
## Instroduction to the BeCalm software Components

BeCalm is a software for telemetry and medical followup of COVID patients
It is made of 3 components:

### Becalm Station 
Can be found in https://github.com/idatis-org/becalm-station/ , it contains software that allows to setup a Raspberry Pi as a self contained measuring unit of vital constants of a patient. It is meant to be used with a respiratory assisted system based on opoen ventilators, such as the Declathlon Mask non intrussive ventilator https://github.com/bneiluj/covid-19-open-source-ventilators#UTBM-Decathlon-Valve-for-caregiver. 
as of now it allows to connect a pressure sensor placed inside the ventilator and determine Respiratory frequency, max and minimum pressure inside the mask. These are the standard measures used by comercially available ventilator systems. It is prepared as well to connect an oximeter but developement has stopped at that point (looking for contributors ! )

### Becalm Server
Can be found under https://github.com/idatis-org/becalm-server, it contains the server software ready to run in any linux distribution that enables to store measures coming from Becalm Station. The server has been designed for high performance, allowing hundreds of Becalm Stations to submit real time measures and store them to make then available for mass monitoring of COVID patiends. The software is at this stage 100% functional

### Becalm Frontend 
A separate web based frontend, found under https://github.com/idatis-org/becalm-frontend , that can be run in any linux distrubution and enables visualization of the data provided by the Becalm Server. The frontend enables monitoring in real time of hundreds of patients that are connected to a Becalm Station. The Becalm Frontend is at this stage 100% functional

## Instralling and Running Becalm Station
The Becalm Station software is meant to run in a Raspberry PI to which a pressure sensor is connected. Others sensors such as PulsiOxymeter sensor Max30100 / Max30102 or the CO2 concentration sensor CJMCU-811 have not been implemented.
A dummy sensor for development purposes only, can be used to run the Becalm Station software in a device with no physical sensor connected.

Becalm Station is a set of several python scripts that need to be run independently. It has been made to be lightweight and modular, so you have to understand the architecture. We will describe here how to download and run Becalm Station software using the dummysensor that provides dummy measures of heartbeat, PEEP (positive end-expiratory pressure) , respiratory rate and spO2.

Running the Becalm Station software in a Raspberry PI with a physical sensor attached is straightforward, as it requires only to start the corresponding sensor driver instead of the dummysensor driver.

### Installing Becalm Station
Download the software:
`
  git clone https://github.com/idatis-org/becalm-station.git
`
Install Python3 if it is not installed and some required modules
```
      sudo apt-get update
      sudo apt-get upgrade
      sudo apt-get install python3
      sudo apt-get install python3-pip
```
Install required Python modules:
```
      pip3 install flask
      pip3 install flask_cors
      pip3 install flask_resful
      pip3 install flask_restful
      pip3 install flask_apscheduler
```

### Running the Becalm Station software
The becalm Station requires a running Becalm Server to which it will send the data that it collects. You can as well use the Idatis hosted becalm server. For that you will have to request idatis at becalm@idatis.org, the provisioning of your device(s) and you will receive the IDs that can be used to post data to the Idatis becalm server (becalm.idatis.org port 4000)

The address and port of the server running the Becalm Server has to be provided in the broker.py file, open it with a text editor to modify the following lines to match your configuration:

```
# The Server hostname and port where we can contact the becalm server service
# You can use the Idatis becalm server to store and to inspect your measures in real time
# Send a mail to becalm@idatis.org to request provisioning of new devices, they will send you an ID
# that can be used to post to the Idatis' hosted Becalm server
serverAddr="idatis.valora.io"
serverPort="4000"
sensorId='1'
```


Once this is done you can start the sensor driver (here we will run the dummy sensor)

```
      ./dummysensor.py
```

And finally start the broker, that takes measures from the sensors and sends them to the Becalm Server:
```
      ./broker.py
```
