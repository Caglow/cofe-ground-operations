


import time
import threading
import traceback

import queVars

if not queVars.fakeGalil:
	import socket
	print "Using real socket at start"
else:
	import fakeSocket as socket
	print "Using fake socket at start"

import sys

import struct
import drParse

import os.path



# Enables and disables logging of timestamps for analysis
logTimeStamps = True

CONF_TIMEOUT = 0.5


class GalilInterface:

	numAxis		=	2		# the DMC-2120 has two axes
	running		=	True

	pos		= [0,0,0,0,0,0,0,0,0]
	vel		= [0,0,0,0,0,0,0,0,0]
	inMot		= [0,0,0,0,0,0,0,0,0]

	oldTime = 0

	udpInBuffer = ""

	threads = []

	def __axisIntToLetter(self, axis):
		return chr(65+axis)

	def __axisLetterToInt(self, axis):
		return ord(axis[-1])-65

	def __init__(self, ip, port = 23, fakeGalil = False, poll = False, resetGalil = False, download = True, unsol = True):


		self.port = port
		self.ip = ip

		print "Starting Interface"
		if not fakeGalil:
			import socket
			print "using real socket at instantiation"
		else:
			import fakeSocket as socket
			print "using fake socket at instantiation"




		self.con = socket.create_connection((self.ip, self.port ), CONF_TIMEOUT)
		self.con.settimeout(CONF_TIMEOUT)


		if resetGalil:
			print "Resetting Galil"
			self.resetGalil(download)
			


		self.sendOnly("IHT=-3;")	# Close ALL THE (other) SOCKETS

		if poll:
			print "Beginning Solicited TCP Polling"
			self.__startPolling()

		if unsol:
			print "Opening Unsolicited messages socket."
			self.__initUnsolicitedMessageSocket()

	def __initUnsolicitedMessageSocket(self):
		# The reccomended way for handling both solicited and unsolicited messages from the galil is to use two sockets. One socket is for normal 
		# comms, and the other is configured for handling the unsolicited messages (e.g. interrupt messages, etc...)


		self.unsolCon = socket.create_connection((self.ip, self.port+1 ), CONF_TIMEOUT)

		self.unsolCon.sendall("CF I;\r\n")
		self.recieveOnly(self.unsolCon)

		# I *think* the response garbling I was seeing was CW being set. This causes the MSB of all ascii characters in unsolicited
		# messages to be set. I don't know what the default setting is, though. 
		self.unsolCon.sendall("CW 2;\r\n")
		self.recieveOnly(self.unsolCon)
		
		self.startPollingUnsol()


	def startPollingUnsol(self):

			self.pollUnsolTh = threading.Thread(target = self.pollUnsol, name = "galilUnsolicitedPollThread")
			self.pollUnsolTh.start()
			self.threads.append(self.pollUnsolTh)


	def pollUnsol(self):
		
		retString = ""
		while self.running:

			
			try:
				retString += self.unsolCon.recv(1)

			except socket.timeout:					# Exit on timeout
				pass

			except socket.error:					# I've Seen socket.error errors a few times. They seem to not break anything.
										# Therefore, we just ignore them
				print "wut"
				pass

			if retString.find("\r\n")+1:				# 
				message, retString = retString.split("\r\n", 1)
				print "Received message - ", message
				
				if logTimeStamps:
					if message.find("Input Timestamp") + 1:
						# for some bizarre reason, the galil returns timestamps with four trailing zeros (e.g. xxx.0000)
						# The timestamps are ALWAYS just an integer
						# Anyways, the python int() function can't handle strings with a decimal, so we split off the 
						# empty fractional digits
						time = int(message.split()[-1].split(".")[0])
						delta = time - self.oldTime
						self.oldTime = time
						print "Timestamp", int(time), "Delta", delta
						with open("tsLog.txt", "a") as fp:
							fp.write("Timestamp, %s, %s \n" % (time, delta))


	def flushBufUDP(self, socketConnection, galilAddrTup):

		self.sendAndRecieveUDP("TP;", socketConnection, galilAddrTup)
		for x in range(2):
			self.receiveUDP(socketConnection)
	
		self.udpInBuffer = ""
		self.flushSocketRecvBuf(socketConnection)

	def receiveUDP(self, socketConnection):
		startTime = time.time()
		ret = ""
		while time.time() < (startTime + CONF_TIMEOUT):
			try:
				tmp, ip = socketConnection.recvfrom(1024)
				self.udpInBuffer += tmp
			except:
				pass
			#print self.udpInBuffer
			
			if self.udpInBuffer.find(":")+1:
				ret, self.udpInBuffer = self.udpInBuffer.split(":", 1)
				ret = ret.rstrip().lstrip()
				if ret:		# Check we actually have something.
							# Occationally, you just get two colons ("::"), which results in an empty ret
					break

		return ret



	def sendAndRecieveUDP(self, cmdStr, socketConnection, addrTuple):
		#First, we need to clear the input buffer, because we want to get rid of any previous strings
		self.flushSocketRecvBuf(self.con)


		cmdStr = cmdStr + "\r\n"
		socketConnection.sendto(cmdStr, addrTuple) 		# send the command string
		time.sleep(0.2)				# give some time for the galil to respond

		socketConnection.settimeout(CONF_TIMEOUT)
		return self.receiveUDP(socketConnection)


	def initUDPMessageSocket(self):

		print "Opening UDP Socket"
		
		# We need to know the local address to bind to to receive UDP messages from the galil
		# There is not particularly elegant way to get this. As such, we open a TCP socket connection
		# and then look at the local connection information to figure out which interface we're using to 
		# talk to the galil over TCP. It's probably safe to use that for UDP too
		con = socket.create_connection((self.ip, self.port ), 1)
		localIP = (con.getsockname()[0])
		con.shutdown(socket.SHUT_RDWR)
		con.close()

		UDP_PORT = 5005
		UDP_ADDR_TUPLE = (localIP, UDP_PORT)
		GALIL_UDP_ADDR_TUPLE = (self.ip, UDP_PORT)

		# UDP socket for DR (data record) logging from the galil
		drSock = socket.socket(socket.AF_INET, # Internet
 		                    socket.SOCK_DGRAM, # UDP
 		                    socket.IPPROTO_UDP)

		drSock.bind(UDP_ADDR_TUPLE)

		print "Flushing UDP connection",
		self.flushBufUDP(drSock, GALIL_UDP_ADDR_TUPLE)
		print "Done"
		ret = ""
		# It seems that occationally the initial response from the galil on a UDP socket
		# is garbage. Therefore, we loop until we see a proper response to the initial query
		while not ret.find("IH") + 1:
			ret =  self.sendAndRecieveUDP("WH;", drSock, GALIL_UDP_ADDR_TUPLE)
			if not ret.find("IH") + 1:
				print "Bad return value -", ret

		self.udpHandleNumber = self.__axisLetterToInt(ret)
		if (self.udpHandleNumber > 7) or (self.udpHandleNumber < 0) :
			raise ValueError, "Invalid handle number. Garbled data on init?"

		print "UDP Handle: \"%s\", e.g. handle %d" % (ret, self.udpHandleNumber)
		
		ret =  self.sendAndRecieveUDP("QZ;", drSock, GALIL_UDP_ADDR_TUPLE)
		self.infoTopology = ret
		
		# receive until we start timing out.
		tmp = self.receiveUDP(drSock)
		while tmp:
			print "Ret: \"", tmp, "\""
			tmp = self.receiveUDP(drSock)

		drSock.sendto("DR 103,%s\r\n" % self.udpHandleNumber, GALIL_UDP_ADDR_TUPLE)

		#drSock.settimeout(1)
		#time.sleep(1)

		
		
		#print data, addr
		print "UDP Init done"

		self.startPollingUDP(drSock, GALIL_UDP_ADDR_TUPLE)


		#self.startPollingUDP()


	def startPollingUDP(self, udpSock, galilAddrTup):

			self.pollUDPTh = threading.Thread(target = self.pollUDP, name = "galilUDPPollThread", args = (udpSock, galilAddrTup))
			self.pollUDPTh.start()
			self.threads.append(self.pollUDPTh)


	def pollUDP(self, udpSock, galilAddrTup):
		fp = open("posvelDR.txt", "a")
		while self.running:

			
			try:
				dat, ip = udpSock.recvfrom(1024)
				#print "received", len(dat), ip, 
				dr = drParse.parseDataRecord(dat)

				if dr:
					ts = ((dr["I"]["GI8"] & 0x1F) * 2**24) + (dr["I"]["GI9"] * 2**16) + (dr["I"]["GI5"] * 2**8) + (dr["I"]["GI4"])
					#print dr["I"]["GI4"], dr["I"]["GI5"], dr["I"]["GI9"], dr["I"]["GI8"] & 0x1F
					curTOW = drParse.getMsTOWwMasking()
					towErr = curTOW - ts
					logStr = "DR Received, %s, %s, %s, %s\n" % (int(time.time()*1000), curTOW, ts, towErr)
					#logStr = "DR Received, %s, %s, %s, %s\n" % (dr["I"]["GI4"], dr["I"]["GI5"], dr["I"]["GI9"], dr["I"]["GI8"])
					print logStr,
					fp.write(logStr)
				else:
					fp.write("Bad DR Received, %s\n" % (time.time()))
			except socket.timeout:					# Exit on timeout
				pass

			except socket.error:				# I've Seen socket.error errors a few times. They seem to not break anything.
										# Therefore, we just ignore them
				print "wut"
				fp.write("Socket Error, %s, %s\n" % (time.time(), time.strftime("Datalog - %Y/%m/%d, %a, %H:%M:%S", time.localtime())))
				pass
		# Turn off the data-record outputs
		self.sendAndRecieveUDP("DR 0,0;\r\n", udpSock, galilAddrTup)	

		# Tell the galil to close the UDP socket
		# This *seems* to work, though supposedly the IH command only works on sockets the galil opens as master.
		# Undocumented features, AHOY!	
		# Never mind, it's documented, just in more recent docs
		self.sendAndRecieveUDP("IHS=-3;\r\n", udpSock, galilAddrTup)	# IHS=-3 means "close the socket this command is received on"


		for x in range(5):
			print "Waiting for any remaining packets, ", 5-x
			
			try:
				dat, ip = udpSock.recvfrom(1024)
				#print "received", len(dat), ip

			except socket.timeout:					# Exit on timeout
				pass

			except socket.error:					# I've Seen socket.error errors a few times. They seem to not break anything.
										# Therefore, we just ignore them
				print "wut"
				pass

		fp.close()

	def __downloadFunctions(self):

		#
		# Download a file of galilCode to the remote controller.
		#
		# Note: The galil only supports one "file" of code. Every time you download new routines, it overwrites everything
		# that is currently on the galil. You can have multiple functions in one code-file, so it's not a serious problem,
		# just something you have to keep in mind.
		#

		#First, we need to clear the input buffer, because we want to get rid of any previous strings
		self.con.settimeout(0.0)
		try:
			self.con.recv(256)
		except:
			pass

		gcFile = os.path.join(os.getcwd(), 'galilCode', "stageCode.dmc")
		codeFile = open(gcFile, "r")
		routines = codeFile.read()
		codeFile.close()

		self.con.sendall("DL\r")					# Enter program download mode

		lineNum = 1							# for printing a nice representation of the code

		print "Starting download of galilcode routines"
		print "LineNum, Code"
		for line in routines.split("\n"):

			line = line.rstrip()					# Strip whatever variety of \r\n chars are in the file

			if line == "":						# add a comment character ("'") to all empty lines
				line = "'"					# so they don't break the galil
										# the galil terminal does this silently, behind the scenes, when you send a code file.
										# very confusing, since the manual states that empty lines are not allowed, but they
										# work anyways within the galilTerminal application

			cleanedLine = line + "\r"				# the Galil wants carriage-return (only!) line endings.
										# I wonder if the original galil protocol design work was done on a mac?

			if len(cleanedLine) > 80:				# Check line lengths
				print "Error - Line %d too long" % lineNum
				print "Ensure all galilCode lines are shorter then 80 characters"
				print "Line contents: ", cleanedLine
				raise ValueError

			print str(lineNum).zfill(4), cleanedLine.rstrip()	# Print linenum and line (and strip the extra \r / \n) (for debugging)
			lineNum += 1

			self.con.sendall(cleanedLine)				# finally, send the line
			try:
				if self.con.recv(256):				# and check for a response
										# (there shouldn't be. You only get a response of there is an error)
					raise ValueError, "Error downloading galil code"
			except:
				pass

			time.sleep(0.05)					# a short pause so we don't overflow the galil's TCP input buffer
												# (Yes, it was happening)

		self.con.sendall("\\\r")					# leave program download mode

		time.sleep(0.1)							# Needed to work around some bugs in the crApple python TCP stack

		print "Sent"
		try:
			print "Recieved - ", self.con.recv(64).rstrip().lstrip().rstrip(":").lstrip(":")			# Check status return code from the download operaton
										# It should be two colons ("::"). Should probably check that
		except:
			print "Galil Timed Out"
			traceback.print_exc(6)


		self.con.settimeout(CONF_TIMEOUT)


	def __startPolling(self):
		self.polCon = socket.create_connection((self.ip, self.port + 1), CONF_TIMEOUT)
		self.polCon.settimeout(CONF_TIMEOUT)
		#self.con.setblocking(0)

		self.pollPosTh = threading.Thread(target = self.posVelPol, name = "galilPollThread")
		self.pollPosTh.start()
		self.threads.append(self.pollPosTh)



		#for x in range(self.numAxis):				# the GUI monitors the calil status by watching these arrays.
		#							# At the moment, if they are not at least filled with 0's, the gui errors.
		#							# Probably better to fix the GUI, but this is easier ATM.
		#		self.pos.append(0)
		#		self.vel.append(0)
		#		self.inMot.append(0)


	def flushSocketRecvBuf(self, socketCon):
		#python socket.socket doesn't have a flush() function! WTF?

		try:
			socketCon.settimeout(0.0)
			socketCon.recv(1024)
		except:
			pass
		finally:
			socketCon.settimeout(CONF_TIMEOUT)


	def posVelPol(self):
		fp = open("posvelpol.txt", "a")
		while self.running:
			self.flushSocketRecvBuf(self.polCon)
				
			try:
				# Horrible one-liners of DOOOOOOOMMMMM
				#
				# This line takes the return values from the "TP" command, cleans them, breaks them into separate variables
				# typeconverts to int, and stuffs them into a list
				#

				self.polCon.sendall("TP\r\n")
				temp =  [int(float(i)) for i in self.recieveOnly(self.polCon).rstrip("\r\n:").strip().strip(":").replace(", ", " ").split()]
				self.pos = temp

				# and for the "TV" command
				self.polCon.sendall("TV\r\n")
				temp = [int(float(i)) for i in self.recieveOnly(self.polCon).rstrip("\r\n:").strip().strip(":").replace(", ", " ").split()]
				self.vel = temp

				#Now, we check axis state (moving or not moving)

				# First, construct a query string based on the number of axis the galil has
				motionStStr = "MG "
				for x in range(self.numAxis):
					axLetter = self.__axisIntToLetter(x)
					motionStStr += ", _BG%s, _MO%s" % (axLetter, axLetter)
				motionStStr += "\r\n"

				# then query the galil
				self.polCon.sendall(motionStStr)
				recStr = self.recieveOnly(self.polCon)

				#finally, another horrible one-liner to parse the return string

				self.inMot = [bool(int(i.split(".")[0])) for i in recStr.rstrip("\r\n:").strip().strip(":").replace(", ", " ").split()]

				#print motionStStr, recStr

				#print recStr
				#print "Pos, Vel", self.pos, self.vel

				#print "Polled"
				fp.write("Polled, %s, %s\n" % (time.time(), time.strftime("Datalog - %Y/%m/%d, %a, %H:%M:%S", time.localtime())))
			except:
				print "Communications Error"
				fp.write("Comm Error, %s, %s\n" % (time.time(), time.strftime("Datalog - %Y/%m/%d, %a, %H:%M:%S", time.localtime())))
				traceback.print_exc()

			time.sleep(0.1)

		fp.close()

	def checkAxis(self, axis):						# Check if an axis number is valid
		if (axis + 1) > self.numAxis:
			print axis
			raise ValueError, "Invalid Axis"


	def sendOnly(self, cmdStr, debug = True):				# Send a command string without listening for a response
		cmdStr = cmdStr + "\r"						# append the line terminator the galil wants

		if debug: print "Sent Command - \"", cmdStr.rstrip().strip(), "\""

		self.con.sendall(cmdStr)


	def recieveOnly(self, socketConnection, mask=False):				# Recieve from the galil until the galil sends a line terminator
										# The terminates lines with either a  ":" or a "?"
										#
										# ":" - Indicates the previous command was successful
										# "?" - Indicates there was an error in the previous command (either syntax or system)



		retString = ""
		while not retString.find(":")+1:				# Galil return strings end with a colon (":"). We loop on the socket untill we either see a colon, or time out
			try:
				retString += socketConnection.recv(1)

			except socket.timeout:					# Exit on timeout
				print "Galil Timed Out"
				traceback.print_exc(6)
				break

			except socket.error:					# I've Seen socket.error errors a few times. They seem to not break anything.
										# Therefore, we just ignore them
				print "wut"
				pass

			if retString.find("?")+1:				# print error info if we recieve a error
				print "Syntax Error - ",
				print "Returned Value:", retString
				print "Error Code:"
				print self.sendAndRecieve("TC1")		# "TC1" - This queries the galil for what the previous error was caused by
				break
		return retString

	def sendAndRecieve(self, cmdStr, debug = True):
		#
		#	This is probably a little brittle for long term reliance
		#
		# Anyways, you pass the command you want to send the galil, and a
		# line termniator is autmatically appended, and the return value is read
		# back, and returned.
		#
		# The return value has the line terminator and some of the window decoration (":")
		# stripped from it to make it easier to parse
		#

		#First, we need to clear the input buffer, because we want to get rid of any previous strings
		self.flushSocketRecvBuf(self.con)


		self.sendOnly(cmdStr, debug)			# send the command string
		time.sleep(0.050)				# give some time for the galil to respond
		retString = ""


		retString = self.recieveOnly(self.con)				# check for the response.
		retString = retString.rstrip("\r\n:").strip().strip(":")	# and strip off the garbage the galil sends to make interacting with it over telnet easier.

		return retString

	def getPosition(self):

		positionStr = self.sendAndRecieve("TP")

		retVals = []

		if positionStr:

										# parse the returned string of ints into a list of actual ints.

			stripStr = positionStr.replace(" ", "")

			for item in stripStr.split(","):
				try:	retVals.append( int(item) )
				except:
					print positionStr
					raise ValueError

		return retVals

	def getVelocity(self):

		velocityStr = self.sendAndRecieve("TV")

		retVals = []

		if velocityStr:
										# parse the returned string of ints into a list of actual ints.

			stripStr = velocityStr.replace(" ", "")

			for item in stripStr.split(","):
				try:	retVals.append( int(item) )
				except:
					print velocityStr
					raise ValueError

		return retVals


	# Most of these commands are pretty self-explanitory.
	# They do what is says on the tin.
	# Mostly, the diffrerence is just in the command string

	def moveAbsolute(self, axis, position):
		self.checkAxis(axis)
		command = "PA%s=%d" % (self.__axisIntToLetter(axis), position)

		responseStr = self.sendAndRecieve( command )
		#print command, positionStr

		return responseStr


	def moveRelative(self, axis, deltaPosition):
		self.checkAxis(axis)
		command = "PR%s=%d" % (self.__axisIntToLetter(axis), deltaPosition)

		responseStr = self.sendAndRecieve( command )
		#print command, positionStr

		return responseStr


	def setMoveSpeed(self, axis, velocity):
		self.checkAxis(axis)
		command = "SP%s=%d" % (self.__axisIntToLetter(axis), velocity)

		responseStr = self.sendAndRecieve( command )
		#print command, positionStr

		return responseStr


	def moveAtSpeed(self, axis, velocity):
		self.checkAxis(axis)
		command = "JG%s=%d" % (self.__axisIntToLetter(axis), velocity)

		responseStr = self.sendAndRecieve( command )
		#print command, positionStr

		return responseStr


	def beginMotion(self, axis = None):
		if axis != None:
			command = "BG %s" % chr(65+axis)			# Chr converts to an axis letter (e.g. A, B, C, D, etc...)
										# The galil inanely wants an axis letter here, instead of a number
		else:
			command = "BG"

		responseStr = self.sendAndRecieve( command )

		return responseStr

	def inMotion(self, axis):
		command = "MG _BG%s " % chr(65+axis)				# Chr converts to an axis letter (e.g. A, B, C, D, etc...)
										# The galil inanely wants an axis letter here, instead of a number

		responseStr = self.sendAndRecieve( command , debug = False)


		#print "PositionStr - ", positionStr
		return responseStr

	def endMotion(self, axis = None):
		if axis != None:
			command = "ST %s" % self.__axisIntToLetter(axis)	# Chr converts to an axis letter (e.g. A, B, C, D, etc...)
										# The galil inanely wants an axis letter here, instead of a number
		else:
			command = "ST"

		responseStr = self.sendAndRecieve( command )

		return responseStr

	def motorOn(self, axis = None):
		if axis != None:
			command = "SH %s" % self.__axisIntToLetter(axis)	# Chr converts to an axis letter (e.g. A, B, C, D, etc...)
										# The galil inanely wants an axis letter here, instead of a number
		else:
			command = "SH"

		responseStr = self.sendAndRecieve( command )

		return responseStr

	def motorOff(self, axis = None):
		if axis != None:
			command = "MO %s" % self.__axisIntToLetter(axis)	# Chr converts to an axis letter (e.g. A, B, C, D, etc...)
										# The galil inanely wants an axis letter here, instead of a number
		else:
			command = "MO"

		responseStr = self.sendAndRecieve( command )

		return responseStr

	def homeAxis(self, axis):

		command = "#HOME%s" % self.__axisIntToLetter(axis)
		self.executeFunction(command)

	def executeFunction(self, func):

		if func[0] != "#":						# if the function name is not prefixed with a "#", add one.
			func = "#" + func

		command = "XQ %s" % func


		responseStr = self.sendAndRecieve( command )

		return responseStr

	def resetGalil(self, download = True):	
				#We re-download the galilcode on reset, since resetting clears the function memory
				# if you don't want to re-download the functions, pass download = false

		command = "RS"

		self.sendOnly( command )

		time.sleep(0.5)
		if download:
			self.__downloadFunctions()



	def close(self, motorsOff = True):		#Optionally turn the motors off, and then try to close the socket
										# connection gracefully

		if self.running:			# This can be called both manually and by __del__
			self.running = False 	# Therefore, we look at self.running to determine if we need to stop the threads 
			for thread in self.threads:			# Stop the various threads
				if thread:
					print "Stopping thread:", thread
					thread.join()

		if self.con:
			try:							# Since this is called both manually and by the destructor, we have to simply catch and ignore errors here.
										# otherwise, there are errors arising from the fact that it winds up trying to close a closed connection.


				print "Closing Connection"

				if motorsOff:
					self.sendOnly("MO")


				self.sendOnly("IHT=-3;")	# Close ALL THE (other) SOCKETS
				self.con.shutdown(socket.SHUT_RDWR)
				self.con.close()
				self.con = None
			except:
				pass


	def __del__(self):
		self.close()


if __name__ == "__main__":

	gInt = GalilInterface(ip = "192.168.1.250", fakeGalil=False, poll = False, resetGalil = True, unsol = False, download = False)


	time.sleep(1)
	print "done"
	gInt.initUDPMessageSocket()
	#gInt.motorOn()
	#gInt.executeFunction("MAIN")
	
	try:
		while 1:
			time.sleep(10)
	except KeyboardInterrupt:
		print "Exiting"

	gInt.close(False)
	sys.exit(0)

#print con.recv(1)
