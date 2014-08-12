smartgarage
===========
Garage parking assistance and status monitoring.

*Currently, the web monitoring lives within the web directory, but is intended to be separated into a stand-alone project.*

## Install
Future versions will utilize pip
```
git clone https://github.com/jonni83/smartgarage.git
cd smartgarage/web/garageNet
npm install
```

## Config
The smartgarage.ini file contains the config that describes the physical setup

```
[General]
mode: bcm

[HallEffect]
leftclosed: 4
leftopen: 17
rightclosed: 2
rightopen: 3

[UltraSonic]
lefttrigger: 10
leftecho: 9
righttrigger: 7
rightecho: 8

[Relay]
red: 24
yellow: 23
green: 18
```

## Usage
Run the parking asistance python script

Run the garage status server

Run the garage web app