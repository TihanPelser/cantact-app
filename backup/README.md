# CANtact-app

CANtact-app is an open source software tool for interfacing with Controller Area
Network systems from the desktop. It is primarily intended to be used with the
[CANtact hardware](https://github.com/linklayer/cantact-hw), but should work
with any device that uses the LAWICEL protocol.

## Screenshot
![CANtact Screenshot](https://raw.github.com/linklayer/cantact-app/master/cantact-screenshot.png)

## Installation
### Prerequisites
The `ant` and `netbeans` packages.  

### Build
`git clone https://github.com/linklayer/cantact-app`  
`cd cantact-app`  
`ant build`  
 - `ant build` requires a proper `CLASSPATH`.  If you don't know what an appropriate `CLASSPATH` should be you can open the netbeans IDE (via `netbeans`) and view the IDE Log Output.  

## Features
- Display of CAN bus trace
- Live display, showing the most recent data for each frame
- Simple transmission of CAN frames
- Javascript scripting interface
- ISOTP transmit and receive
- Saving of CAN traces (in candump format)

## TODO
- OBD-II, and UDS protocol implementations
- CAN databases and signal decoding
