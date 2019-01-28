import subprocess as sp

#set start and end based on GPS values
start = True
end = False
extProc = 1
while True:
	if start == True:
		extProc = sp.Popen(['python3','test.py'])
		start = False
	if end == True:
		sp.Popen.terminate(extProc)
		end == False
