#!/usr/bin/python3
# coding: utf-8
import sys
import os
import logging
import time
from datetime import date
import json
import threading
from  urllib import request, parse
from time import sleep
import datetime
import configparser
import concurrent.futures
import asyncio.coroutines
import getpass
import socket
import config
from services.servicodevalidacao import servicoDeValidacao
from services.DataUpdate import DataUpdate
from services.SMS import SMS
from services.watch import Watch
from services.recupecaoDeCarrinhos import recuperacaoDeCarrinhos
from utils.db import DB
from controle import Controle


class Initialize:
	
	def __init__(self,M):
		
		self.__cfg() 
		logging.basicConfig(
			filename=self.Config.get("LOGS","manager_log"),
			filemode='a+',
			level=logging.INFO,
			format='%(asctime)s %(name)18s #> %(message)s',
			datefmt='%d-%m-%Y %H:%M:%S'
			#stream=sys.stderr,
		)
		#Definindo objeto dos Serviços
		self.Controle = Controle(self)
		self.servicos = self.Controle.servicos
		self.database = DB(self)

		self.SMS = SMS(M)
		self.recuperacaoDeCarrinhos = recuperacaoDeCarrinhos(M)
		self.DataUpdate = DataUpdate(M)
		self.servicoDeValidacao = servicoDeValidacao(M)
		self.Watch = Watch(M)

		#Definindo objeto das API's
		
		self.job_sms = threading.Thread(target=self.SMS.start, name="SMS", args=(lambda:self.Controle.servicos.SMS.stop,))
		self.job_src = threading.Thread(target=self.recuperacaoDeCarrinhos.start, name="SRC", args=(lambda:self.Controle.servicos.SRC.stop,))
		self.job_servico_de_validacao = threading.Thread(target=self.servicoDeValidacao.start, name="SVC")
		self.job_dataupdate = threading.Thread(target=self.DataUpdate.start, name="SDU")
		self.job_watch = threading.Thread(target=self.Watch.start, name="WATCH")
		# Inicializando
	
	
	def __cfg(self):
		DIR							= os.getcwd()
		USER						= getpass.getuser()
		self.Config					= configparser.ConfigParser()
		self.Config_ENV				= configparser.ConfigParser()
		self.Config._interpolation	= configparser.ExtendedInterpolation()
		try:
			self.Config.read("{0}/config/DEFAULT.ini".format(DIR))
		except Exception as e:
			print(type(e))
			print(e)

		try:
			self.Config.set("KEY", "root", DIR)
			self.Config.set("KEY", "user",USER)
			with open("{0}/config/DEFAULT.ini".format(DIR), "w+") as configfile:		
				self.Config.write(configfile)
		except Exception as e:
			print(type(e))
			print(e)
		try:
			s	= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			s.connect(("8.8.8.8", 80))
			IP	= s.getsockname()[0]
			s.close()

		except Exception as e:

			print(type(e))
			print(e)
	
		#DEFINE ENV
		betas=["237.29","192.168.", "10.8.0"]
		try:	
			if any(beta in IP for beta in betas) :
				self.Config.set("KEY", "env", "BETA")

			elif "242.11" in IP or "242.52" in IP:
				self.Config.set("KEY", "env", "PROD")
			else:
				print("Não foi Possivel identivicar o ambiente!")
				try:
					print("Defina o tipo de Ambiente:")
					print("(1) BETA\n(2) PRODUCAO\n")
					env = input()
					
					if env == '1':
						self.Config.set("KEY", "env", "BETA")
					elif env == '2':
						self.Config.set("KEY", "env", "PROD")
					else:
						sys.exit("Opção invalida!")
				except Exception as e:
					print(type(e))
					print(e)
					raise Exception("Não foi Possivel identivicar o ambiente!")
					print(sys.exc_info()[0])
					sys.exit("Erro ao definir env")
				
				with open("{0}/config/DEFAULT.ini".format(DIR), "w+") as configfile:		
					self.Config.write(configfile)
	
		except Exception as e:
			print(type(e))
			print(e)
		try:
			 self.Config_ENV.read("config/{0}.ini".format(self.Config.get("KEY", "env")))
		except  Exception as e:
				print(type(e))
				print(e)
	
	def todict(self,obj, classkey=None):
		if isinstance(obj, dict):
			data = {}
			for (k, v) in obj.items():
				data[k] = self.todict(v, classkey)
			return data
		elif hasattr(obj, "_ast"):
			return self.todict(obj._ast())
		elif hasattr(obj, "__iter__") and not isinstance(obj, str):
			return [self.todict(v, classkey) for v in obj]
		elif hasattr(obj, "__dict__"):
			data = dict([(key, self.todict(value, classkey)) 
			for key, value in obj.__dict__.items() 
				if not callable(value) and not key.startswith('_')])
			if classkey is not None and hasattr(obj, "__class__"):
				data[classkey] = obj.__class__.__name__
			return data
		else:
			return obj

	def configFile(self):

		contrle_dict =  self.todict(self.Controle)
		for mod in contrle_dict:

			if 'api' in mod.casefold():
				for x in contrle_dict[mod]:
					if any(api in  x.casefold() for api in ["comtele", "mandrill"]):
						self.Config_ENV.set(contrle_dict[mod][x]['tag'],"enviados",str(contrle_dict[mod][x]['enviados']))
					else:
						self.Config_ENV.set(contrle_dict[mod][x]['tag'],"consultas",str(contrle_dict[mod][x]['consultas']))
		
		with open("{0}/config/{1}.ini".format(self.Controle.Key.root,self.Controle.Key.env ), "w+") as configfile:		
			self.Config_ENV.write(configfile)

	#TODO, metodo para atualizar configurações
	""" def setMyself(self, module):
		modulo = self.getControle(module)

		api_dict = modulo.__dict__
		for x in api_dict:

			self.Config_ENV.set(api_dict[x].tag, api_dict[x].__dict__)
		
		with open("{0}/config/BETA.ini".format(self.Controle.Key.root), "w+") as configfile:		
			self.Config_ENV.write(configfile)	
 """
	def Jobs(self):
		jobs = {
			'SMS': self.job_sms,
			'SVC': self.job_servico_de_validacao,
			'SDU': self.job_dataupdate,
			'WATCH':self.job_watch,
			'SRC':self.job_src
		}
		return jobs
	
	def getControle(self, module):
		if "db" in module.casefold():
			return self.Controle.DB
		elif 'files' in module.casefold():
			return self.Controle.files
		elif 'api' in module.casefold():
			return self.Controle.API
		elif 'modulos' in module.casefold():
			return self.Controle.servicos
		elif 'sms' in module.casefold():
			return self.Controle.servicos.SMS
		elif 'svc' in module.casefold():
			return self.Controle.servicos.SVC
		elif 'src' in module.casefold():
			return self.Controle.servicos.SRC
		elif 'sdu' in module.casefold():
			return self.Controle.servicos.SDU
		elif 'link' in module.casefold():
			return self.Controle.LINK
	
			
		self.controle	
	
	def setConfigFile(self, conf):
		
		if "DEFAULT".casefold() in conf.casefold():
			try:
				with open("{0}/config/DEFAULT.ini".format(self.Config.get("KEY", "root")), "w+") as configfile:		
					self.Config.write(configfile)
					return True
			except Exception as e:
				print(type(e))
				print(e)
				return False
		
		if "BETA".casefold() in conf.casefold():
			try:
				with open("{0}/config/BETA.ini".format(self.Config.get("KEY", "root")), "w+") as configfile:		
					self.Config_ENV.write(configfile)
					return True
			except Exception as e:
				print(type(e))
				print(e)
				return False

		elif "PROD".casefold() in conf.casefold():
			try:
				
				with open("{0}/config/PROD.ini".format(self.Config.get("KEY", "root")), "w+") as configfile:		
					self.Config_ENV.write(configfile)
				return True
			except Exception as e:
				print(type(e))
				print(e)
				return False
		