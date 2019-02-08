#use this subprocess as backup option,
#import works fine for starting another python script
#but import doesn't start scripts in parallel

#import subprocess as sp

from threading import Thread
from subprocess import call

def thread_second():
    call(["python3", "hello.py"])

#set start and end based on GPS values
#need more testing

start = True
#end = False
#extProc = 1
while True:
	if start == True:
		#extProc = sp.Popen(['python3','test.py'])
		#import hello
		processThread = Thread(target=thread_second)
		processThread.start()
		start = False
		while True:
			print("AAAAAAAAA")
		break
	#if end == True:
		#sp.Popen.terminate(extProc)
		#end == False
