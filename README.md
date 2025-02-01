# WifiBF
 OSX Wifi password checker


### Usage
You might need to install the OSX command-line tools, you can invoke this by simply typing the following in the Terminal:
 
> python3
 
After python3 is installed you can simply run this script like:

> python3 wifibf.py

Example output:
![](scrot.jpg)

Optionally you can try:

> python wifibf-single-thread.py

In case multi processing does not give the desired result.

### Operantion
This script uses OSX built-in command-line tools to scan and connect to SSIDS in scanning range using a list of passwords you can find in the script. Optionally you can use an external text file (see code). 

### Limitations
* There seem to be some false positives when there are multiple Access Points with the same name (dual band 2.4/5g) this needs more research.
