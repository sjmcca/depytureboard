# Depyture Board

Display the latest departure information for a journey between 
two stations.

This is based on scraping the network rail website rather than
a stable API so honestly it might break at any time if they 
change their website, specifically the page 
[here]("https://www.nationalrail.co.uk/live-trains/departures)

## Physical Setup

The board is built around displaying on a 
[Waveshare 1.54in e-Paper display](https://www.waveshare.com/1.54inch-e-paper.htm).

Here's a good pinout diagram for the Pi4, which is _think_ is the 
same across models, but maybe check if you don't have a 4:

![](https://www.raspberrypi.com/documentation/computers/images/GPIO-Pinout-Diagram-2.png?hash=df7d7847c57a1ca6d5b2617695de6d46)

Which can be matched up to the e-Paper cable using the table under 
the header [Working With Raspberry Pi](https://www.waveshare.com/wiki/1.54inch_e-Paper_Module_Manual#Program_Principle)
Probably also follow the steps to enable SPI interface on the Pi.

Your Pi will need an internet connection, either ethernet or Wifi is
fine.


## Code Setup

If you don't already have Python3:

```bash
sudo apt-get update
sudo apt-get install python3
sudo apt-get install python3-pip
```

Then clone the repo and install dependencies:

```bash
git clone <link here>
cd depytureboard
python -m venv venv
venv/bin/pip install -r requirements.txt
venv/bin/pip install wavesharelib
```

## Run

Currently there's no command args to tell the board which
journey to monitor, so it's just set to Witham to Liverpool
Street. 

```bash
venv/bin/python depytureboard.py
```


## Other bits

Standard setup instructions for using python with the 
e-Paper display can be found [here](https://www.waveshare.com/wiki/1.54inch_e-Paper_Module_Manual#Python)
We install the dependencies for the e-Paper display from 
these instructions through requirements.txt (hopefully)

```bash
sudo apt-get update
sudo apt-get install python3-pip
sudo apt-get install python3-pil
sudo apt-get install python3-numpy
sudo pip3 install spidev
sudo apt install python3-gpiozero
```



## Future

- Other e-Paper display support
- Find an actual API to get the data, rather than scraping
- Configurable stations