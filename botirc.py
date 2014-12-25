#python
# -*- coding: utf8 -*-


import irclib
import ircbot
import random
import imp
import os

file_path = os.path.dirname(os.path.realpath(__file__))

class Bot(ircbot.SingleServerIRCBot):
	test_quizz = 0
	chan_irc = "#linuxlab"
	reponse =""
	
	def __init__(self):
		ircbot.SingleServerIRCBot.__init__(self, [("irc.esgi-linuxlab.fr", 6667)],"Andre_Cabuzo", "Bot surveillant de trolling")
		self.salutations = ["Salut à toi ","Bien le bonjour, ","Salut ","Hey, ", "Coucou "]
	def on_kick(self, serv, ev):
		serv.join(Bot.chan_irc)
		serv.privmsg(Bot.chan_irc, "salope")
	def handle_module(self, called_module, serv, nick, chan, msg):
			try:
				if called_module+".py" in os.listdir(file_path+"/modules/"):
					mod = imp.load_source(called_module, file_path+"/modules/"+called_module+".py")
					mod.__init__(serv, nick, chan, msg)
				else:
					print "Unimplemented function :"+called_module
			except Exception as error:
				print "Exception : "+str(error)
	def on_welcome(self, serv, ev):
		serv.join(Bot.chan_irc)
	def on_pubmsg(self, serv, ev):
		auteur = irclib.nm_to_n(ev.source())
		#On met tout en minuscule au cas ou
		message = ev.arguments()[0].lower()
		if message[0:1]=="!":
			self.handle_module(message.split(" ")[0][1:], serv, auteur, Bot.chan_irc, message)


	def on_privmsg(self, serv, ev):
		message = ev.arguments()[0]
		auteur = irclib.nm_to_n(ev.source())
		if "admin1234" in message:
			serv.privmsg(auteur,"bonjour admin")
			serv.mode(Bot.chan_irc,"+o "+auteur)
		if "quitte" in message:
			ircbot.SingleServerIRCBot.die(self, ":'(")
			print "Bot IRC has quit properly"
			exit()

	def on_join(self, serv, ev):
		auteur = irclib.nm_to_n(ev.source())
		if auteur not in ['Andre_Cabuzo']:
			serv.privmsg(Bot.chan_irc, self.salutations[random.randint(1,4)]+auteur+"!")


if __name__ == "__main__":
	print "Bot IRC started."
	Bot().start()
	print "Bot IRC has quit properly"
