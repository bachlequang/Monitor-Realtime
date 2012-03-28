import os
class Command(object):
 
	def __init__(self, command):
		self.command = command
 
	def run(self, shell=True):
		import subprocess as sp
		process = sp.Popen(self.command, shell = shell, stdout = sp.PIPE, stderr = sp.PIPE)
		self.pid = process.pid
		self.output, self.error = process.communicate()
		self.failed = process.returncode
		return self
 
@property
def returncode(self): return self.failed

com = Command("ping -c 3 -W 1 dantri.com.vn").run()
if com.failed:
   print "PING FAILED"
   print com.error
else:
          print com.output