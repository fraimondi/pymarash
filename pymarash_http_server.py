"""
@author: Franco Raimondi

Inspired by the code available at https://github.com/MrYsLab/s2a_fm

"""

import logging
import usb.core, usb.util, time
from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer
from string import split

# Port for the HTTP server (it should match what is declared in the .json file)
port = 14275

# A dictionary associating the command received from Scratch with a bit pattern
# to be sent to the USB link 
armcmds = dict()
armcmds["rotateccw"] = [0,2,0]
armcmds["rotatecw"] = [0,1,0]
armcmds["shoulderup"] = [64,0,0]
armcmds["shoulderdown"] = [128,0,0]
armcmds["elbowup"] = [16,0,0]
armcmds["elbowdown"] = [32,0,0]
armcmds["wristup"] = [4,0,0]
armcmds["wristdown"] = [8,0,0]
armcmds["gripopen"] = [1,0,0]
armcmds["gripclose"] = [2,0,0]

# Let's find the arm (the ID is fixed)
RoboArm = usb.core.find(idVendor=0x1267, idProduct=0x000)


#Check if the arm is detected and stop here if not
if RoboArm is None:
    raise ValueError("Arm not found")

# A class to handle HTTP requests
class GetHandler(BaseHTTPRequestHandler):

    # This is where we do the translation from HTTP request to USB command
    def do_GET(self):

        # remove the "/" at the beginning
        arguments = self.path[1:]

        # split the URL using the separator character "/"
        # (see Scratch documentation for off-line extensions)
        cmd_list = split(arguments, '/')

        s = 'okay'
        # If the command is to turn the light on or off we send directly the instruction
        # I add a small timeout at the end of each instruction in case the client keeps
        # sending messages
        if cmd_list[0] == 'lighton':
            RoboArm.ctrl_transfer(0x40,6,0x100,0,[0,0,1])
            time.sleep(0.1)
        elif cmd_list[0] == 'lightoff':
            RoboArm.ctrl_transfer(0x40,6,0x100,0,[0,0,0])
            time.sleep(0.1)
        # If the command is one of the commands that we know (see dictionary above)
        # then we invoke it. Notice that all these commands come with a duration
        # that is found in cmd_list[2].
        # FIXME: maybe add a check that the duration is in a valid range?
        elif cmd_list[0] in armcmds.keys():
            MoveArm(float(cmd_list[2]),armcmds[cmd_list[0]])

        elif cmd_list[0] == 'poll':
            # We do nothing for poll requests!
            s = 'okay'

        # If the command is not one of the above, then print an error and return.
        else:
            print "Some error with this command!"+cmd_list[0]
            return

        # If we reach this point, everything should be OK and we send an 'okay' message back
        self.send_resp(s)

    def send_resp(self, response):
        """
        HTTP response. It always starts with an heading, then it attached
        """

        crlf = "\r\n"
        http_response = "HTTP/1.1 200 OK" + crlf
        http_response += "Content-Type: text/html; charset=ISO-8859-1" + crlf
        http_response += "Content-Length" + str(len(response)) + crlf
        http_response += "Access-Control-Allow-Origin: *" + crlf
        http_response += crlf

        # send it out the door to Scratch
        self.wfile.write(http_response)

# A function to execute an instruction for a certain time
def MoveArm(Duration, ArmCmd):
    #Start the movement
    RoboArm.ctrl_transfer(0x40,6,0x100,0,ArmCmd)
    #Stop the movement after waiting a specified duration
    time.sleep(Duration)
    ArmCmd=[0,0,0]
    RoboArm.ctrl_transfer(0x40,6,0x100,0,ArmCmd)
    # As above: adding a small timeout to avoid flooding
    time.sleep(0.1)

def start_server():

    try:
        server = HTTPServer(('localhost', port), GetHandler)
        print 'Starting py-marash HTTP Server!'
        print 'Use <Ctrl-C> to exit the extension\n'
        print 'You can now start Scratch and import the extension'
    except Exception:
        logging.debug('Something wrong here')
        print 'HTTP Socket may already be in use or Arm is not connected - restart Scratch'
        raise
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logging.info('py-marash HTTP server: keyboard interrupt exception')
        print "Goodbye !"
        raise KeyboardInterrupt
    except Exception:
        logging.debug('py-marash: Exception %s' % str(Exception))
        raise

if __name__ == "__main__":
        start_server()
