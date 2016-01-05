import sys
import signal
import getopt
import serial
import io
import time
import requests
import collections
from config import *

class TD(object):
    def __init__(self, maxlen=10):
        self.leveld = collections.deque(maxlen=10)
        self.tempd = collections.deque(maxlen=10)
        self.vbd = collections.deque(maxlen=10)
        self.msgno = 0

    def add (self, level, temp, Vb):
        self.leveld.append( (level + sum(self.leveld)) / (1 + len(self.leveld)) )
        self.tempd.append( (temp + sum(self.tempd)) / (len(self.tempd) + 1) )
        self.vbd.append( (Vb + sum(self.vbd)) / (len(self.vbd) + 1) )
        self.msgno =+ 1

    def avg (self):
        if (self.msgno > 0):
            return sum(self.leveld)/len(self.leveld),sum(self.tempd)/len(self.tempd),sum(self.vbd)/len(self.vbd)
        else:
            return None, None, None
    def len (self):
		return len(self.vbd)

data = [TD(), TD(), TD(), TD(), TD()]

UpdateRate = UpdateRate*1000	# convert seconds to milli seconds

millis = lambda: int(round(time.time() * 1000))

def log(msg):
	try:
		r = requests.post ( LogAddr, data={'msg': msg})
		print(r.status_code, r.reason, r.text)
	except:
		print "Requests error"


def processMsg (msg):
	nodeid = 0
	d = 0
	t = 0.0

	if msg.startswith("M:"):
		linetokens = msg.split()
		print linetokens

		try:
			nodeid = int(linetokens[2])
			d = int(linetokens[3])
			t = float(linetokens[4])
			Vb = int(linetokens[5])
#			print nodeid, d, t
			print nodeid, 
			sys.stdout.flush()
		except:
			print '-',
			return False
		else:
			data[nodeid].add(d, t, Vb)
			return True
	else:
		print '.',
		return False

def main(argv):                         
	try:                                
		opts, args = getopt.getopt(argv, "hp:", ["help", "port="])
	except getopt.GetoptError:
		usage()
		sys.exit(2)                     

	for opt, arg in opts:                
		if opt in ("-h", "--help"):      
			usage()                     
			sys.exit()                  
		elif opt in ("-p", "--port"): 
			serialport = arg               
			print "Serial Port: " + serialport
		else:
			usage()                     
			sys.exit()                  

	try:
		ser = serial.Serial(serialport, BaudRate, timeout=10)
	except:
		print "Unable to open serial port " + serialport
		sys.exit(2)

	ser.flush()

	last_update = millis()

	while True:	
		try:
			line = ser.readline()
#			print line,

			result = processMsg(line)
			if (result & (millis() - last_update > UpdateRate)):
				last_update = millis()
				print " "
				for i in range(5):
					if (data[i].len()) > 0:
						al,at,avb = data[i].avg()
						try:
							r = requests.post ( PostAddr, data={'tank_id': str(i), 'tank_level': str(al), 'temperature': str(at), 'Vb': str(avb)})
							print(r.status_code, r.reason, r.text)
						except:
							print "Requests error"

		except KeyboardInterrupt:
			print "\nClosing serial port..."
			ser.flush()
			ser.close()
			exit(0)



def usage():
	print "Options are:"
	print "-h or --help \n\t prints usage summary"
	print "-p /dev/ttyUSB0 or --port /dev/ttyUSB0 \n\tto specify the serial port"

if __name__ == "__main__":
	print ("ZL2CCO SenseNet Gateway running")
	main(sys.argv[1:])








