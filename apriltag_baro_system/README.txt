AprilTag + Barometer Landing Test

Setup:
- Connect Pixhawk via USB (/dev/ttyACM0)
- pip install -r requirements.txt

Run:
python main_baro_test.py

Behavior:
- Align using AprilTag
- Descend using barometer
- LAND below 0.5m
