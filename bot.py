import Skype4Py
import time
import re
import requests
import BeautifulSoup
from random import randint

class GifBot(object):
	def __init__(self):
		# Create an instance of the Skype class.
		self.skype = Skype4Py.Skype(Events=self)

		# Connect the Skype object to the Skype client.
		self.skype.Attach()

		# Obtain some information from the client and print it out.
		print 'Your full name:', self.skype.CurrentUser.FullName
		print 'Your contacts:'
		for elem in self.skype.BookmarkedChats:
#	elem.SendMessage("SomeMessageHere")
#	print elem.Members
		   print elem.Topic

	def getGif(self, search):
		#r = requests.get("http://giphy.com/search/"+search)
		r = requests.get("http://www.reddit.com/r/gifs/search?q="+search+"+url%3A*.gif&sort=relevance&t=all")
		bs = BeautifulSoup.BeautifulSoup(r.text)

		#gifImg = bs.findAll('img', {'class':'gifs-gif unloaded'})
		gifImg = bs.findAll('a', {'class':'title may-blank '})

		total = len(gifImg)
		if total > 0:
		        #if total > 1:
		        #        gif = gifImg[0]['data-animated'] + " Or "+ gifImg[1]['data-animated']
		        #else:
			if total > 1:
			        gif = gifImg[randint(0,(total-1))]['href']
			else:
				gif = gifImg[0]['href']

		else:
		        gif = "Nothing man..."
		return gif

	def MessageStatus(self, msg, status):
		if status == Skype4Py.cmsReceived:
			#Skype name msg.FromHandle
			#Skype from your list msg.FromDisplayName
			print msg.Body , msg.FromDisplayName, msg.Chat.Topic
			#msg.MarkAsSeen()
			match = re.match("@gif (.*)" , msg.Body, re.IGNORECASE)
			if match:
				typeGif = match.group(1)
				urlGif = self.getGif(typeGif)
				#if typeGif.find("cat") >= 0:
				#	urlGif = "http://weknowgifs.com/wp-content/uploads/2013/04/fuck-this-thing-cat.gif"
				#elif typeGif.find("beer") >= 0:
				#	urlGif = "http://26.media.tumblr.com/tumblr_m2r261ETJi1rnmqv4o2_250.gif"
				#elif typeGif.find("baby") >= 0:
				#	urlGif = "http://25.media.tumblr.com/tumblr_lq9hd6W3Hp1r1ibsxo1_500.gif"
				#else:
				#	urlGif = "http://s2.quickmeme.com/img/f6/f626a08d9ebd17c3ffd922454f79d4964e594df3715fc8a983b675081776b2a6.jpg"
				#msg.Chat.SendMessage("Here we go " + msg.FromDisplayName + " Gif: " + urlGif)
				msg.Chat.SendMessage(urlGif)
			
	    #if status == Skype4Py.cmsReceived:
	      #if msg.Chat.Type in (Skype4Py.chatTypeDialog, Skype4Py.chatTypeLegacyDialog):
	        #for regexp, target in self.commands.items():
	         # match = re.match(regexp, msg.Body, re.IGNORECASE)
	          #if match:
	            #msg.MarkAsSeen()
	           # reply = target(self, *match.groups())
	            #if reply:
	            #  msg.Chat.SendMessage(reply)
	            #break
if __name__ == "__main__":
  bot = GifBot()
  
  while True:
    time.sleep(.2)
