#!/usr/bin/python3
# coding: utf-8


import os
import sys
import time
from time import sleep
import datetime
from datetime import date
import logging
import getpass
import subprocess

class Startup(object):
	def __init__(self, *args, **kwargs):
		self.USER = getpass.getuser()
		logging.basicConfig(
			filename='/home/{0}/PythonServer/logs/StartUp.log'.format(self.USER),
			filemode='a+',
			level=logging.INFO,
			format='PID %(process)5s %(name)18s: %(message)s',
			#stream=sys.stderr,
 		)
		self.log = logging.getLogger('Serviço de Atualização da Base de Dados')
		self.procs = ['sms.py','uwsgi','servico_de_validacao.py','Databaseupdate.py']
		self.delays={'validacao':300}
		self.start_time = 0
		self.i()
	
	def i(self):

		
		while True:
			if not self.checkIfProcessRunning(self.procs[0]):
					self.log.info('{0} . Inicializando serviço de SMS'.format(datetime.datetime.now()))
					os.system('python3 sms.py &')
				
			else:
				pass
			if not self.checkIfProcessRunning(self.procs[1]):
					self.log.info('{0} . Inicializando Servidor API'.format(datetime.datetime.now()))
					os.system('uwsgi --http 10.255.237.29:5000 --wsgi-file /home/{0}/PythonServer/Server/server.py --callable app --processes 4 --threads 2 --stats 127.0.0.1:9191 &'.format(self.USER))
			
			else:
				pass
			if not self.checkIfProcessRunning(self.procs[2]) and not self.checkIfProcessRunning(self.procs[3]):
				if self.start_time ==0:
					self.start_time = time.time()
					self.log.info('{0} . Inicializando serviço de Validação de Cadastros'.format(datetime.datetime.now()))
					os.system('nohup python3 servico_de_validacao.py &')
				elif time.time()- self.start_time > self.delays['validacao']:
					self.start_time = time.time()
					os.system('nohup python3 servico_de_validacao.py &')
			else:
				pass
			if not self.checkIfProcessRunning(self.procs[3]) and not self.checkIfProcessRunning(self.procs[2]):
				
					modtime =os.path.getmtime("/home/"+self.USER+"/PythonServer/queries/query.txt")
					#modificationTime = time.strftime('%H:%M:%S', time.time(mod))
					if modtime < self.start_time:
						pass
					else:
						log.info('{0} . Inicializando serviço de Atualização de Dados'.format(datetime.datetime.now()))
						os.system('python3 Databaseupdate.py &')
			
			else:

				pass
			

			
		sleep(5)

	def checkIfProcessRunning(self,processName):
		'''
		Check if there is any running process that contains the given name processName.
		'''
		#Iterate over the all the running process

		ps = subprocess.Popen(['ps', 'aux'], stdout=subprocess.PIPE).communicate()[0]
		processes = ps.decode().split('\n')
		# this specifies the number of splits, so the splitted lines
		# will have (nfields+1) elements
		nfields = len(processes[0].split()) - 1
		
		for row in processes[1:]:
			try:
				proc = row.split(None, nfields)
				if len(proc)>0:

					# Check if process name contains the given name string.
					if processName.lower() in proc[10].lower():
						return True
				else: 
					pass
			except:
				pass
		return False 

		
	

	
Startup()
