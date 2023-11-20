<h1>Safe and Sound Vault</h1>
<h2>Brief Project Background</h2>
If you were searching for the latest, most secure, state-of-the-art safe, look no further than the FingerLock Fortress 3000. Built out of the strongest material on earth (wood), the FingerSafe Fortress 3000 is the latest and most innovative solution that guarantees 24/7 protection of any valuables! Using fingerprint recognition, you don't have to worry about remembering a code to access the safe, rather simply enroll your fingerprint and access any valuables knowing only enrolled users can access the safe.
<h2>Link to Hackster.io</h2>
To fully build this project, check out the following link with in-depth instructions:

https://www.hackster.io/jjt6/fingerprint-safe-using-pocketbeagle-68aadb

<h2>Software Build Instructions</h2>
The following libraries were installed for my hardware components to run properly. Install the following libraries:
<h3>RGB LCD</h3>

- sudo apt-get update
- sudo pip3 install Adafruit_BBIO
- sudo pip3 install adafruit-blinka
- sudo pip3 install adafruit-circuitpython-charlcd

After installing these libraries run rgb_lcd_test.py to test RGB LCD screen.
<h3>Fingerprint Sensor</h3>

- sudo pip3 install adafruit-circuitpython-fingerprint

After installing this libraries run fingerprint_test.py to test fingerprint sensor.
<h2>Software Operations Instructions</h2>
Complete the following steps to run the code:

- git clone https://github.com/jjtellez25/ENGI301.git
- cd /var/lib/cloud9/ENGI301/project_01
- sudo ./run

If this does not work, the file may not be executable. Run the following line to solve the issue, and then you should be able to run the code using the sudo ./run command.
- chmod 755 run

To make the code run automatically on boot, run the following commands.
- sudo crontab -e
- @reboot sleep 30 && sh /var/lib/cloud9/ENGI301/project_01/run > /var/lib/cloud9/logs/cronlog 2>&1
- Exit and Save
