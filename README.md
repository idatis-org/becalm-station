# becalm-station
BeCalm Station software.

BeCalm is a software for telemetry and medical followup of COVID patients
It is made of 3 components:

- Becalm Station: Can be found in https://github.com/idatis-org/becalm-station/ , it contains software that allows to setup a Raspberry Pi as a self contained measuring unit of vital constants of a patient. It is meant to be used with a respiratory assisted system based on opoen ventilators, such as the Declathlon Mask non intrussive ventilator https://github.com/bneiluj/covid-19-open-source-ventilators#UTBM-Decathlon-Valve-for-caregiver. 
as of now it allows to connect a pressure sensor placed inside the ventilator and determine Respiratory frequency, max and minimum pressure inside the mask. These are the standard measures used by comercially available ventilator systems. It is prepared as well to connect an oximeter but developement has stopped at that point (looking for contributors ! )

- Becalm Server: Can be found under https://github.com/idatis-org/becalm-server, it contains the server software ready to run in any linux distribution that enables to store measures coming from Becalm Station. The server has been designed for high performance, allowing hundreds of Becalm Stations to submit real time measures and store them to make then available for mass monitoring of COVID patiends. The software is at this stage 100% functional

- Becalm Frontend: A separate web based frontend, found under https://github.com/idatis-org/becalm-frontend , that can be run in any linux distrubution and enables visualization of the data provided by the Becalm Server. The frontend enables monitoring in real time of hundreds of patients that are connected to a Becalm Station. The Becalm Frontend is at this stage 100% functional


