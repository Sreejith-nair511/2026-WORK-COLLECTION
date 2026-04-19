# Precision Landing (RPi5 + Pixhawk + ArUco)

## Setup
pip3 install -r requirements.txt

## Run
python3 main.py

## Requirements
- PX4 running on Cube Orange
- USB connection (/dev/ttyACM0)
- Camera connected
- Printed ArUco marker

## Notes
- Uses OFFBOARD mode
- Sends velocity commands continuously
- Lands when marker centered
