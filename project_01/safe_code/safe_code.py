"""
--------------------------------------------------------------------------
PocketVault
--------------------------------------------------------------------------
License:   
Copyright 2023 - JJ Tellez
Built on framework of combo_lock code by Erik Welsh

This code makes use of the incredible kRPC mod and python library.
More information and the download link can be found here: 
https://github.com/jjtellez25/ENGI301

My Hackster project for this can be found here: <INSERT HACKSTER LINK> 

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this 
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------

Use the following hardware components to set up the Safe and Sound Vault:  
  - LCD Display
  - Fingerprint
  - Servo
  - Button
  - Potentiometer


Uses:
  - Libraries developed in class

"""
import time
import board
import busio
import digitalio
from digitalio import DigitalInOut, Direction
import adafruit_fingerprint
import serial

import adafruit_character_lcd.character_lcd     as characterlcd
import Adafruit_BBIO.GPIO                       as GPIO
import button                                   as BUTTON
import servo                                    as SERVO
import potentiometer                            as POT

# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------

### Servo
SERVO_LOCK         = 0          # Fully anti-clockwise
SERVO_UNLOCK       = 100        # Fully clockwise

### Potentiometer

POT_DIVIDER        = 512       # Divider used to help reduce potentiometer granularity
POT_DIVIDER_2      = 2048      # Divider used to help reduce potentiometer granularity
POT_DIVIDER_3      = 1366      # Divider used to help reduce potentiometer granularity

# ------------------------------------------------------------------------
# Global variables
# ------------------------------------------------------------------------

# ------------------------------------------------------------------------
# Functions / Classes
# ------------------------------------------------------------------------

class PocketVault():
    """ PocketVault """
    finger         = None
    camera         = None
    button         = None
    servo          = None
    potentiometer  = None
    debug          = None

    
    def __init__(self, button="P2_8", servo="P1_36", 
                       potentiometer="P1_19"):
        """ Initialize variables and set up display """
        # Add display screen GPIO (red, green, blue)

        self.button         = BUTTON.Button(button)
        self.servo          = SERVO.Servo(servo, default_position=SERVO_LOCK)
        self.potentiometer  = POT.Potentiometer(potentiometer)
        self.debug          = True
        
        # Fingerprint
        uart = serial.Serial('/dev/ttyS4', 57600, timeout=1)
        self.finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)
        
        # Pin Config:
        lcd_rs = digitalio.DigitalInOut(board.P1_2) 
        lcd_en = digitalio.DigitalInOut(board.P1_4)
        lcd_d7 = digitalio.DigitalInOut(board.P2_24)
        lcd_d6 = digitalio.DigitalInOut(board.P2_22)
        lcd_d5 = digitalio.DigitalInOut(board.P2_20)
        lcd_d4 = digitalio.DigitalInOut(board.P2_18)
    
        lcd_columns = 16
        lcd_rows = 2
        
        red = digitalio.DigitalInOut(board.P2_2)
        green = digitalio.DigitalInOut(board.P2_4)
        blue = digitalio.DigitalInOut(board.P2_6)
        
        self.lcd = characterlcd.Character_LCD_RGB(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, red, green, blue)
        
        self._setup()

        # End def

    
    def _setup(self):
        """Setup the hardware components."""
        
        # RGB LCD
            # Backlight
        GPIO.setup("P2_2", GPIO.OUT)
        GPIO.setup("P2_4", GPIO.OUT)
        GPIO.setup("P2_6", GPIO.OUT)
            # Communication
        GPIO.setup("P2_18", GPIO.OUT)
        GPIO.setup("P2_20", GPIO.OUT)
        GPIO.setup("P2_22", GPIO.OUT)
        GPIO.setup("P2_24", GPIO.OUT)
        
        # Button
        GPIO.setup("P2_8", GPIO.IN)

    # End def
    
    ### LCD Functions
    
    def message(self, msg, color="white", sleep=True):
        """Display given message in LCD screen with color"""
        
        color_val = None
        self.lcd.clear()
        
        # Setting color
        if color == "red":
            color_val = [0,0,100]
        if color == "green":
            color_val = [0,100,0]    
        if color == "blue":
            color_val = [100,0,0]
        if color == "purple":
            color_val = [100,0,100]
        if color == "white" or color_val is None:
            color_val = [100,100,100]
        self.lcd.color = color_val
        
        # Display message
        self.lcd.message = msg

        if sleep:
            time.sleep(2)
        
    #End def
    
    ### Servo Functions (with LCD display)
    
    def lock(self):
        """Lock the lock:
               - Set display to "Locking..." for 3 seconds
               - Set display to "Locked" (blue screen)
               - Set servo to close
        """
        if self.debug:
            print("lock()")

        # Set servo to "Locked"
        self.servo.turn(SERVO_LOCK)
        
        # Set display to "Locked" on LCD with green display
        msg = "Locked!"
        self.message(msg,"green")

    # End def

    def unlock(self):
        """Unlock the lock.
               - Set display to "Success! Unlocking..." (green display)
               - Set display to "Unlocked" (blue screen)
               - Set servo to open
        """
        if self.debug:
            print("unlock()")
        
        # Set display "Unlocking..." on LCD
        msg = "Unlocking..."
        self.message(msg,"white",sleep=False)
        
        # Set servo to "Unlocked"
        self.servo.turn(SERVO_UNLOCK)

        # Set display to "Unlocked" on LCD with green display
        msg = "Unlocked!"
        self.message(msg,"green")
        
        
    # End def
    
    ### Fingerprint Functions (with LCD display)
    
    def get_fingerprint(self):
        """"Get finger print from user
            - Ask a finger print image
            - Template finger print image
            - See if it matches with saved finger print images
            - Display attempts remaining
        """
        while self.finger.get_image() != adafruit_fingerprint.OK:
            pass
        self.message("Templating...","white",sleep=False)
        if self.finger.image_2_tz(1) != adafruit_fingerprint.OK:
            return False
        self.message("Searching...","white",sleep=False)
        if self.finger.finger_search() != adafruit_fingerprint.OK:
            self.message("No Match Found!","red")
            return False
        else:
            self.message("Match Found!","green")
            return True
        
    # End def

    # Might not use this function
    def get_fingerprint_detail(self):
        """Get a finger print image, template it, and see if it matches!
        This time, print out each error instead of just returning on failure"""
        self.message("Getting image...","white")
        i = self.finger.get_image()
        if i == adafruit_fingerprint.OK:
            self.message("Image taken","white")
        else:
            if i == adafruit_fingerprint.NOFINGER:
                self.message("No finger \ndetected","white")
            elif i == adafruit_fingerprint.IMAGEFAIL:
                self.message("Imaging error","white")
            else:
                self.message("Other error","white")
            return False

        self.message("Templating...","white")
        i = self.finger.image_2_tz(1)
        if i == adafruit_fingerprint.OK:
            self.message("Templated","white")
        else:
            if i == adafruit_fingerprint.IMAGEMESS:
                self.message("Image too messy","white")
            elif i == adafruit_fingerprint.FEATUREFAIL:
                self.message("Could not \nidentify feature","white")
            elif i == adafruit_fingerprint.INVALIDIMAGE:
                self.message("Image invalid","white")
            else:
                self.message("Other error","white")
            return False

        self.message("Searching...","white")
        i = self.finger.finger_fast_search()
        # pylint: disable=no-else-return
        # This block needs to be refactored when it can be tested.
        if i == adafruit_fingerprint.OK:
            self.message("Found \nfingerprint!","green")
            return True
        else:
            if i == adafruit_fingerprint.NOTFOUND:
                self.message("No match found","red")
            else:
                self.message("Other error","red")
            return False

    # End def

    def enroll_finger(self, location):
        """Take a 2 finger images and template it, then store in 'location'"""
        for fingerimg in range(1, 3):
            if fingerimg == 1:
                self.message("Place finger \non sensor","white")
            else:
                pass

            while True:
                i = self.finger.get_image()
                if i == adafruit_fingerprint.OK:
                    self.message("Image taken","white")
                    break
                if i == adafruit_fingerprint.NOFINGER:
                    self.message("Waiting on \nfinger...","white")
                elif i == adafruit_fingerprint.IMAGEFAIL:
                    self.message("Imaging error","white")
                    return False
                else:
                    self.message("Other error","white")
                    return False

            self.message("Templating...","white",sleep=False)
            i = self.finger.image_2_tz(fingerimg)
            if i == adafruit_fingerprint.OK:
                self.message("Templated","white",sleep=False)
            else:
                if i == adafruit_fingerprint.IMAGEMESS:
                    self.message("Image too messy","white")
                elif i == adafruit_fingerprint.FEATUREFAIL:
                    self.message("Features not \nidentified","white")
                elif i == adafruit_fingerprint.INVALIDIMAGE:
                    self.message("Image invalid","white")
                else:
                    self.message("Other error","white")
                return False

            if fingerimg == 1:
                self.message("Place finger \nagain","white")
                time.sleep(1)
                while i != adafruit_fingerprint.NOFINGER:
                    i = self.finger.get_image()

        self.message("Creating \nmodel...","white",sleep=False)
        i = self.finger.create_model()
        if i == adafruit_fingerprint.OK:
            self.message("Model created!","green")
        else:
            if i == adafruit_fingerprint.ENROLLMISMATCH:
                self.message("Prints did \nnot match","white")
            else:
                self.message("Other error","white")
            return False

        msg = "Storing model \n#%d..." % location
        self.message(msg,"white",sleep=False)
        i = self.finger.store_model(location)
        if i == adafruit_fingerprint.OK:
            msg = "Model #%d\nStored!" % location
            self.message(msg,"green")
        else:
            if i == adafruit_fingerprint.BADLOCATION:
                self.message("Bad storage \nlocation","white")
            elif i == adafruit_fingerprint.FLASHERR:
                self.message("Flash storage \nerror","white")
            else:
                self.message("Other error","white")
            return False

        return True

    # End def
    
    def update_value(self,value):
        # Update the LCD display with the potentiometer value
        self.lcd.clear()
        self.message(str(value),"white",sleep=False)
        # Wait for a short time to avoid flickering
        time.sleep(0.1)
    
    # Show a value 1-8
    def show_analog_value(self):
        """Show the analog value on the screen:
               - Read raw analog value
               - Divide by 512 (remove two LSBs)
               - Display value
               - Return value
        """
        if self.debug:
            print("show_analog_value()")
            
        # Read value from Potentiometer
        value = self.potentiometer.get_value()

        # Divide value by POT_DIVIDER
        value = int(value // POT_DIVIDER) + 1

        # Update display (must be an integer)
        self.update_value(value)
        
        # Return value
        return value
    
    # Show a value from 1-2
    def show_analog_value_2(self):
        """Show the analog value on the screen:
               - Read raw analog value
               - Divide by 2048 (remove two LSBs)
               - Display value
               - Return value
        """
        if self.debug:
            print("show_analog_value()")
            
        # Read value from Potentiometer
        value = self.potentiometer.get_value()

        # Divide value by POT_DIVIDER
        value = int(value // POT_DIVIDER_2) + 1

        # Update display (must be an integer)
        self.update_value(value)
        
        # Return value
        return value
    
    # Show a value 1-3   
    def show_analog_value_3(self):
        """Show the analog value on the screen:
               - Read raw analog value
               - Divide by 1365 (remove two LSBs)
               - Display value
               - Return value
        """
        if self.debug:
            print("show_analog_value()")
            
        # Read value from Potentiometer
        value = self.potentiometer.get_value()

        # Divide value by POT_DIVIDER
        value = int(value // POT_DIVIDER_3) + 1

        # Update display (must be an integer)
        self.update_value(value)
        
        # Return value
        return value
        
    def set_display_input(self, number):
        """Set display to word "in: #" """
        self.message(str(number),"white")

    # End def
    
    def get_num(self):
        """Input a combination for the lock:
                - Wait for a button press doing nothing (start of user inputing combination)
                - Wait for button press; show analog value
                - Record analog value
                - Return analog value
        """
        i = 0
        while (i > 8) or (i < 1):
            try:
                
                # Initialize combination array
                number = None

                # Use knob to select user
                self.message("Use knob to \nselect user","white")
                (button_press_time, number) = self.button.wait_for_press(function=self.show_analog_value)
                
                break
                #i = int(input("Enter ID # from 1-8: "))
            except ValueError:
                pass
        return number
        
    # End def
    
    ### Main Code Functions

    def run(self):
        """Execute the main program."""
        program                      = True
        attempts_left                = 5
        cycle                        = 1
        mins                         = 5

        # Unlock the lock
        self.lock()        
        time.sleep(1)
        
        # Say "Hello!"
        self.message("Hello!","purple")
        
        # Ask user if they are enrolled
        msg = "1-previous user\n2-new user"
        self.message(msg,"white")
        # Wait for button press (show analog value 1-2)
        self.button.wait_for_press()
        self.message("Use knob to \nselect mode","white")
        (button_press_time, mode) = self.button.wait_for_press(function=self.show_analog_value_2)
        
        if mode == 1:
            pass
        if mode == 2:
            while(1):
                self.message("Have main user\nplace fingerprint","white")
                if self.get_fingerprint():
                    msg = "Hello User #" + str(self.finger.finger_id) + "!\nConfidence:" + str(self.finger.confidence)
                    self.message(msg,"green")
                    self.enroll_finger(self.get_num())
                    break
                else:
                    self.message("Try again","red")
        
        while(cycle==1):        
            while(1):
                # Program the safe
                if (program):
                    if self.debug:
                        print("Program Lock")
    
                # Set Display to try combination
                self.message("Place finger \nto unlock safe")
                
                # Check if fingerprint matches
                if self.get_fingerprint():
                    msg = "Hello User #" + str(self.finger.finger_id) + "!\nConfidence:" + str(self.finger.confidence)
                    self.message(msg,"green")
                    # Unlock the safe
                    self.unlock()
                    break
                else:
                    attempts_left = attempts_left - 1
                    msg = "Tries left: " + str(attempts_left)
                    self.message(msg,"red")
                    # User timeout session
                    if attempts_left == 0:
                        msg = "Try again in\n" + str(mins) + " mins"
                        self.message(msg,"red")
                        time.sleep(mins*60)
                        mins = mins + 5
                        attempts_left = 5
            
            # Locking safe mechanism
            self.message("Press button \nto lock safe","white")
            self.button.wait_for_press()
            self.message("Place finger \nto unlock safe")
            while(1):
                if self.get_fingerprint():
                    msg = "Hello User #" + str(self.finger.finger_id) + "!\nConfidence:" + str(self.finger.confidence)
                    self.message(msg,"green")
                    # Lock the safe
                    self.lock()
                    break
                else:
                    self.message("Try again!","red")
            
            msg = "1-unlock safe\n2-keep locked"
            self.message(msg,"white")
            # Wait for button press (show analog value)
            self.button.wait_for_press()
            self.message("Use knob to \nselect mode","white")
            (button_press_time, mode) = self.button.wait_for_press(function=self.show_analog_value_2)
            if mode == 1:
                pass
            if mode == 2:
                cycle = 2
                self.message("Cya later!","purple")

    # End def

    def cleanup(self):
        """Cleanup the hardware components."""
        
        # Set Display to something fun to show program is complete
        self.message("That did\n NOT work","white")
        

    # End def

# End class


# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':

    print("Program Start")

    # Create instantiation of the lock
    safe_code = PocketVault()

    try:
        # Run the lock
        safe_code.run()

    except KeyboardInterrupt:
        # Clean up hardware when exiting
        safe_code.cleanup()

    print("Program Complete")







 #Test code for fingerprint scanner with LCD display, button, and potentiometer
#    while True:
#        print("----------------")
#        print("Fingerprint templates:", safe_code.finger.templates)
#        print("e) enroll print")
#        print("f) find print")
#        print("d) delete print")
#        print("----------------")
        
#        if safe_code.finger.read_templates() != adafruit_fingerprint.OK:
#            raise RuntimeError("Failed to read templates")
#        msg = "1-enroll 2-find\n3-delete"
#        safe_code.message(msg,"white")
#        # Wait for button press (show analog value)
#        safe_code.message("Use knob to \nselect mode","white")
#        (button_press_time, mode) = safe_code.button.wait_for_press(function=safe_code.show_analog_value_3)
    
#        if mode == 1:
#            safe_code.enroll_finger(safe_code.get_num())
#        if mode == 2:
#            if safe_code.get_fingerprint():
#                msg = "Detected #" + str(safe_code.finger.finger_id) + "\nConfidence:" + str(safe_code.finger.confidence)
#                safe_code.message(msg,"white")
#            else:
#                safe_code.message("Finger not found","red")
#        if mode == 3:
#            if safe_code.finger.delete_model(safe_code.get_num()) == adafruit_fingerprint.OK:
#                safe_code.message("Deleted!","white")
#            else:
#                safe_code.message("Failed to delete","white")

