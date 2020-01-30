#!/usr/bin/python3
# coding= utf-8


class Controle(object):
	def __init__(self,I):
		#TODO: Registrar logs "Carregando configurações!"
		
		self.Config 	= I.Config
		self.Config_ENV = I.Config_ENV
		self.Key 		= Key(self)
		self.DB 		= DB(self)
		self.API		= API(self)
		self.LINK 		= LINK(self)
		self.logs		= logs(self)
		self.files		= files(self)
		self.servicos 	= servicos(self)
	""" TODO:
		! Concluir metodo get/set das variaveis de controle assim como escrita dela no arquivo de configuração
	"""
	
	
	
	def reloadControle(self,I, module = "all"):
		#TODO: Registrar logs
		if "all" in module:
			self.Config 	= I.Config
			self.Config_ENV = I.Config_ENV
			self.Key 		= Key(self)
			self.DB 		= DB(self)
			self.API		= API(self)
			self.LINK 		= LINK(self)
			self.logs		= logs(self)
			self.files		= files(self)
			self.servicos 	= servicos(self)
			return
		elif "svc" in module:
			self.servicos.SVC = self.servicos.SVC(self)
			pass
		elif "sdu" in module:
			self.servicos.SDU = self.servicos.SDU(self)
			return
		elif "src" in module:
			self.servicos.SRC = self.servicos.SRC(self)
			return
		elif "sms" in module:
			self.servicos.SMS = self.servicos.SMS(self)
			return

	def writeConfigFile(self,*args, **kwargst):
			try:
				conf = kwargst['conf']
			except:
				try:
					conf = args[0]
				except:
					conf = None
			finally:
				if not conf or "all" in conf:
					try:
						with open("{0}/config/DEFAULT.ini".format(self.Key.root), "w+") as configfile:		
							self.Config.write(configfile)
							return True
					except Exception as e:
						print(type(e))
						print(e)
						return False
					try:
						with open("{0}/config/{1}.ini".format(self.Key.root,self.Key.env), "w+") as configfile:		
							self.Config.write(configfile)
							return True
					except Exception as e:
						print(type(e))
						print(e)
						return False
				elif "env" in conf:
					try:
						with open("{0}/config/{1}.ini".format(self.Key.root,self.Key.env), "w+") as configfile:		
							self.Config.write(configfile)
							return True
					except Exception as e:
						print(type(e))
						print(e)
						return False
				elif "default" in conf:
					try:
						with open("{0}/config/DEFAULT.ini".format(self.Key.root), "w+") as configfile:		
							self.Config.write(configfile)
							return True
					except Exception as e:
						print(type(e))
						print(e)
						return False
				else:
					return False
				
		
class Key(Controle):

	def __init__(self,Controle):
		
		
	
		
		self.env  = Controle.Config.get("KEY","env")
		self.root = Controle.Config.get("KEY","root")
		self.user = Controle.Config.get("KEY","user")

class DB(Controle):

	def __init__(self,Controle):
		

		self.MYSQL_R = self.MYSQL_R(Controle)
		self.MYSQL_W = self.MYSQL_W(Controle)
	class MYSQL_R(object):
		
		def __init__(self,Controle):
		
		
			self.host				= Controle.Config_ENV.get("MYSQL_R","host")
			self.user				= Controle.Config_ENV.get("MYSQL_R","user")
			self.passwd				= Controle.Config_ENV.get("MYSQL_R","passwd")
			self.database			= Controle.Config_ENV.get("MYSQL_R","database")
			self.raise_on_warnings	= Controle.Config_ENV.get("MYSQL_R","raise_on_warnings")

	class MYSQL_W(object):
		def __init__(self,Controle):
			
			self.host				= Controle.Config_ENV.get("MYSQL_W","host")
			self.user				= Controle.Config_ENV.get("MYSQL_W","user")
			self.passwd				= Controle.Config_ENV.get("MYSQL_W","passwd")
			self.database			= Controle.Config_ENV.get("MYSQL_W","database")
			self.raise_on_warnings	= Controle.Config_ENV.get("MYSQL_W","raise_on_warnings")

class API(Controle):
	def __init__(self,Controle):
	
		
		self.mandrill 	= self.mandrill(Controle)
		self.hubd		= self.hubd(Controle)
		self.soa 		= self.soa(Controle)
		self.comtele 	= self.comtele(Controle)
		self.viacep 	= self.viacep(Controle)
	
			

	
	class viacep:
		def __init__(self,Controle):
			self.tag		= "VIACEP"
			self.consultas	= int(Controle.Config_ENV.get(self.tag,"consultas"))
		def setControle(self,*args, **kwargst):
			try:
				variavel = kwargst['vars']
			except:
				try:
				variavel = args[0]
				except:
					return False
			else:
				keys = variavel.keys()
				for key in keys:
					if 'consultas' in key:
						self.consultas = variavel['consultas']
						Controle.Config_ENV.set(self.tag, 'consultas',self.consultas )
						return True
					else:
						return False
		def getControle(self,*args, **kwargst):
				return var = {
					"consultas":self.consultas
				}
			
	class comtele:
		def __init__(self,Controle):
			self.tag		= "COMTELE"
			self.api_key	= Controle.Config_ENV.get(self.tag,"api_key")
			self.enviados	= int(Controle.Config_ENV.get(self.tag,"enviados"))
		
		def setControle(self,*args, **kwargst):
			try:
				variavel = kwargst['vars']
			except:
				try:
				variavel = args[0]
				except:
					return False
			else:
				keys = variavel.keys()
				for key in keys:
					if 'enviados' in key:
						self.enviados = variavel['enviados']
						Controle.Config_ENV.set(self.tag, 'enviados',self.enviados )
						return True
					elif 'api_key' in key:
						self.consultas = variavel['consultas']
						Controle.Config_ENV.set(self.tag, 'api_key',self.consultas )
						
		def getControle(self,*args, **kwargst):
				return var = {
					"enviados":self.enviados,
					"api_key":self.api_key
				}
			
	class mandrill:
		def __init__(self,Controle):
			self.tag		= "MANDRILL"
			self.api_key	= Controle.Config_ENV.get(self.tag,"api_key")
			self.enviados	= int(Controle.Config_ENV.get(self.tag,"enviados"))
		def setControle(self,*args, **kwargst):
			try:
				variavel = kwargst['vars']
			except:
				try:
				variavel = args[0]
				except:
					return False
			else:
				keys = variavel.keys()
				for key in keys:
					if 'enviados' in key:
						self.enviados = variavel['enviados']
						Controle.Config_ENV.set(self.tag, 'enviados',self.enviados )
						return True
					elif 'api_key' in key:
						self.api_key = variavel['api_key']
						Controle.Config_ENV.set(self.tag, 'api_key',self.api_key )
						
		def getControle(self,*args, **kwargst):
				return var = {
					"enviados":self.enviados,
					"api_key":self.api_key
				}
	class hubd:
		def __init__(self,Controle):
			self.tag		= "HUBD"
			self.url		= Controle.Config_ENV.get(self.tag,"url")
			self.api_key	= Controle.Config_ENV.get(self.tag,"api_key")
			self.consultas 	= int(Controle.Config_ENV.get(self.tag,"consultas"))
		def setControle(self,*args, **kwargst):
			try:
				variavel = kwargst['vars']
			except:
				try:
				variavel = args[0]
				except:
					return False
			else:
				keys = variavel.keys()
				for key in keys:
					if 'url' in key:
						self.url = variavel['url']
						Controle.Config_ENV.set(self.tag, 'url',self.url )
						return True
					elif 'api_key' in key:
						self.api_key = variavel['api_key']
						Controle.Config_ENV.set(self.tag, 'api_key',self.api_key )
					elif 'consultas' in key:
						self.consultas = variavel['consultas']
						Controle.Config_ENV.set(self.tag, 'consultas',self.consultas )
					
						
		def getControle(self,*args, **kwargst):
				return var = {
					"url":			self.url,
					"api_key":		self.api_key,
					"consultas":	self.consultas
				}
	class soa:
		def __init__(self,Controle):
			self.tag		= "SOA"
			self.url		= Controle.Config_ENV.get(self.tag,"url")
			self.key		= Controle.Config_ENV.get(self.tag,"key")
			self.user		= Controle.Config_ENV.get(self.tag,"user")
			self.consultas	= int(Controle.Config_ENV.get(self.tag,"consultas"))
		
		def setControle(self,*args, **kwargst):
			try:
				variavel = kwargst['vars']
			except:
				try:
				variavel = args[0]
				except:
					return False
			else:
				keys = variavel.keys()
				for key in keys:
					if 'url' in key:
						self.url = variavel['url']
						Controle.Config_ENV.set(self.tag, 'url',self.url )
						return True
					elif 'key' in key:
						self.key = variavel['key']
						sControle.Config_ENV.set(self.tag, 'key',self.key )
					elif 'user' in key:
						self.key = variavel['user']
						Controle.Config_ENV.set(self.tag, 'user',self.user )
					elif 'consultas' in key:
						self.consultas = variavel['consultas']
						Controle.Config_ENV.set(self.tag, 'consultas',self.consultas )
					
						
		def getControle(self,*args, **kwargst):
				return var = {
					"url":			self.url
					"user":			self.url
					"key":			self.enviados,
					"consultas":	self.consultas
				
				}

class LINK(Controle):
	def __init__(self,Controle):
	
		self.link_site		= Controle.Config_ENV.get("LINK","link_site")
		self.link_de_compra	= Controle.Config_ENV.get("LINK","link_de_compra")
		self.contact_mail	= Controle.Config_ENV.get("LINK","contact_mail")
  
	def setControle(self,*args, **kwargst):
			try:
				variavel = kwargst['vars']
			except:
				try:
				variavel = args[0]
				except:
					return False
			else:
				keys = variavel.keys()
				for key in keys:
					if 'link_site' in key:
						self.link_site = variavel['link_site']
						Controle.Config_ENV.set('LINK', 'link_site',self.link_site )
						return True
					elif 'link_de_compra' in key:
						self.link_de_compra = variavel['link_de_compra']
						Controle.Config_ENV.set('LINK', 'link_de_compra',self.link_de_compra )
					elif 'contact_mail' in key:
						self.link_de_compra = variavel['contact_mail']
						Controle.Config_ENV.set('LINK', 'contact_mail',self.contact_mail )
						
		def getControle(self,*args, **kwargst):
				return var = {
					"link_site":		self.link_site,
					"link_de_compra":	self.link_de_compra,
					"contact_mail":		self.contact_mail
				}
class logs(Controle):

	def __init__(self,Controle):

		self.manager_log	= Controle.Config.get("LOGS","manager_log")
		self.sdu_log		= Controle.Config.get("LOGS","sdu_log")
		self.svc_log		= Controle.Config.get("LOGS","svc_log")
		self.sms_log		= Controle.Config.get("LOGS","sms_log")
		self.api_log		= Controle.Config.get("LOGS","api_log")
		self.startup_log	= Controle.Config.get("LOGS","startup_log")
		self.watch_log		= Controle.Config.get("LOGS","watch_log")

class files(Controle):
	def __init__(self,Controle):

		self.query			= Controle.Config.get("FILES","query")
		self.responses		= Controle.Config.get("FILES","responses")
		self.responses_api	= Controle.Config.get("FILES","responses_api")
		self.responses_sms	= Controle.Config.get("FILES","responses_sms")
	def getControle(self, parameter_list):
		return var = {
			'query' :self.query,
			'responses' :self.responses,
			'responses_api' :self.responses_api,
			'responses_sms' :self.responses_sms	
		}
class servicos(Controle):
	def __init__(self,Controle):

		self.SMS	= self.SMS(Controle)
		self.SVC	= self.SVC(Controle)
		self.SDU	= self.SDU(Controle)
		self.SRC	= self.SRC(Controle)
		self.WATCH	= self.WATCH(Controle)

	class WATCH:
		def __init__(self,Controle):
			self.addr	= Controle.Config.get("WATCH","addr")
			self.port	= int(Controle.Config.get("WATCH","port"))
	class SMS:
		def __init__(self,Controle):
		
			
			self.init				= Controle.Config.getboolean("SMS","sms_init")
			self.init_time			= None
			self.delay				= None
			self.keepAlive			= True
			self.lasttimerunning	= None
			self.nextrun			= None
			self.firstTime			= True
			self.stop				= False
			self.query				= Controle.Config.get("SMS",'query')
			

		def setControle(self,*args, **kwargst):

			#  @param Dict{var:value}
			try:
				variavel = kwargst['vars']
			except:
				try:
					variavel = args[0]
				except:
					return False
			else:
				keys = variavel.keys()
				for key in keys:
					if 'init' in key:
						self.init = variavel[key] 
						Controle.Config.set("SMS","init", self.init)  
					elif 'init_time' in key:
						self.init_time = variavel[key]
						
					elif 'delay' in key:
						self.delay = variavel[key]
						
					elif 'keepAlive' in key:
						self.keepAlive = variavel[key]
						
					elif 'lasttimerunning' in key:
						self.lasttimerunning = variavel[key]
						
					elif 'nextrun' in key:
						self.nextrun = variavel[key]
						
					elif 'firstTime' in key:
						self.firstTime = variavel[key]
						
					elif 'stop' in key:
						self.stop = variavel[key]
						
					else:
						return False
				return True
		
		def getControle(self):
			return var = {
					'init': 			self.init,
					'init_time': 		self.init_time,
					'delay': 			self.delay,
					'keepAlive': 		self.keepAlive,
					'lasttimerunning': 	self.lasttimerunning,
					'nextrun': 			self.nextrun,
					'firstTime': 		self.firstTime,
					'stop': 			self.stop,
					'query':			self.query
			}
		
	class SVC:
		def __init__(self,Controle):
		
			self.init= Controle.Config.getboolean("SVC","svc_init")
			self.init_time			= None
			self.delay				= float(Controle.Config.get("SVC","delay"))
			self.keepAlive			= True
			self.lasttimerunning	= None
			self.nextrun			= None
			self.firstTime			= True
			self.stop				= False
			self.query_set			= None 
			self.query				= []

			if "," in Controle.Config.get("SVC", "set"):
				self.query_set = Controle.Config.get("SVC", "set").split(",")
			else:
				self.query_set = list(Controle.Config.get("SVC", "set").split(","))
			if isinstance(self.query_set, list):
				for x in self.query_set:
					self.query.append(Controle.Config.get("SVC",x))

		def setControle(self,*args, **kwargst):

			#  @param Dict{var:value}
			try:
				variavel = kwargst['vars']
			except:
				try:
					variavel = args[0]
				except:
					return False
			else:
				keys = variavel.keys()
				for key in keys:
					if 'init' in key:
						self.init = variavel[key] 
						Controle.Config.set("SVC","init", self.init)  
					elif 'init_time' in key:
						self.init_time = variavel[key]
						
					elif 'delay' in key:
						self.delay = variavel[key]
					Controle.Config.set("SVC","delay", self.init) 
						
					elif 'keepAlive' in key:
						self.keepAlive = variavel[key]
						
					elif 'lasttimerunning' in key:
						self.lasttimerunning = variavel[key]
						
					elif 'nextrun' in key:
						self.nextrun = variavel[key]
						
					elif 'firstTime' in key:
						self.firstTime = variavel[key]
						
					elif 'stop' in key:
						self.stop = variavel[key]
					
					elif 'query' in key:
						
						if len(variavel[key]) > self.query:
								self.query = list(set().union(self.query,variavel[key])) 
							for i, x in enumerate(self.query):
								Controle.Config.set("SVC",i, x)
						else:
							self.query = variavel[key]
					elif 'query_set' in key:
						
						if len(variavel[key]) > self.query_set:
							self.query_set = list(set().union(self.query_set, variavel[key]))
						else:
							self.query = variavel[key]
						q_s = ','.join([str(x) for x in self.query_set ])
						Controle.Config.set("SVC","set", q_s)  
					else:
						return False
				return True
		
		def getControle(self,*args, **kwargst):
			return var = {
					'init': 			self.init,
					'init_time': 		self.init_time,
					'delay': 			self.delay,
					'keepAlive': 		self.keepAlive,
					'lasttimerunning': 	self.lasttimerunning,
					'nextrun': 			self.nextrun,
					'firstTime': 		self.firstTime,
					'stop': 			self.stop
					'query_set':		self.query_set
					'query':			self.query
			}
		
	class SDU:
			
		def __init__(self,Controle):
			self.init= Controle.Config.getboolean("SDU","sdu_init")
			self.init_time			= None
			self.delay				= None
			self.keepAlive			= True
			self.lasttimerunning	= None
			self.nextrun			= None
			self.firstTime			= True
			self.stop				= False
		
		def setControle(self,*args, **kwargst):

			#  @param Dict{var:value}
			try:
				variavel = kwargst['vars']
			except:
				try:
					variavel = args[0]
				except:
					return False
			else:
				keys = variavel.keys()
				for key in keys:
					if 'init' in key:
						self.init = variavel[key] 
						Controle.Config.set("SDU","init", self.init)  
					elif 'init_time' in key:
						self.init_time = variavel[key]
						
					elif 'delay' in key:
						self.delay = variavel[key]
						
					elif 'keepAlive' in key:
						self.keepAlive = variavel[key]
						
					elif 'lasttimerunning' in key:
						self.lasttimerunning = variavel[key]
						
					elif 'nextrun' in key:
						self.nextrun = variavel[key]
						
					elif 'firstTime' in key:
						self.firstTime = variavel[key]
						
					elif 'stop' in key:
						self.stop = variavel[key]
						
					else:
						return False
				return True
		
		def getControle(self):
			return var = {
					'init': 			self.init,
					'init_time': 		self.init_time,
					'delay': 			self.delay,
					'keepAlive': 		self.keepAlive,
					'lasttimerunning': 	self.lasttimerunning,
					'nextrun': 			self.nextrun,
					'firstTime': 		self.firstTime,
					'stop': 			self.stop
			}
		
	class SRC:
		
		def __init__(self,Controle):
			self.init				= Controle.Config.getboolean("SRC","src_init")
			self.init_time			= None
			self.delay				= float(Controle.Config.get("SRC","delay"))
			self.keepAlive			= True
			self.lasttimerunning	= None
			self.nextrun			= None
			self.firstTime			= True
			self.stop				= False
			self.querys				= Controle.Config.get("SRC","query")
		
		def setControle(self,*args, **kwargst):

			#  @param Dict{var:value}
			try:
				variavel = kwargst['vars']
			except:
				try:
					variavel = args[0]
				except:
					return False
			else:
				keys = variavel.keys()
				for key in keys:
					if 'init' in key:
						self.init = variavel[key] 
						Controle.Config.set("SRC","init", self.init)  
					elif 'init_time' in key:
						self.init_time = variavel[key]
						
					elif 'delay' in key:
						self.delay = variavel[key]
						Controle.Config.set("SRC","delay", self.delay) 
						
					elif 'keepAlive' in key:
						self.keepAlive = variavel[key]
						
					elif 'lasttimerunning' in key:
						self.lasttimerunning = variavel[key]
						
					elif 'nextrun' in key:
						self.nextrun = variavel[key]
						
					elif 'firstTime' in key:
						self.firstTime = variavel[key]
						
					elif 'stop' in key:
						self.stop = variavel[key]
					elif 'query' in key:
						self.query = variavel[key]
						Controle.Config.set("SRC","query", self.query) 
						
					else:
						return False
				return True
		
		def getControle(self):
			return var = {
					'init': 			self.init,
					'init_time': 		self.init_time,
					'delay': 			self.delay,
					'keepAlive': 		self.keepAlive,
					'lasttimerunning': 	self.lasttimerunning,
					'nextrun': 			self.nextrun,
					'firstTime': 		self.firstTime,
					'stop': 			self.stop,
					'query':			self.query
			}
		


