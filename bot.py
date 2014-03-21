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

		self.lastPlayer = 0
		self.players = []
		print "*** Started!"
	def getUrban(self, search):
		r = requests.get("http://www.urbandictionary.com/define.php?term="+search)
		
		bs = BeautifulSoup.BeautifulSoup(r.text)

                urban = bs.findAll('div', {'class':'meaning'})

                total = len(urban)
                if total > 0:
			return urban[0].text
		else:
			return "Nothing bro... google it!"

	def getGif(self, search):
		r = requests.get("http://www.reddit.com/r/gifs/search?q="+search+"+url%3A*.gif&sort=relevance&t=all")
		bs = BeautifulSoup.BeautifulSoup(r.text)

		gifImg = bs.findAll('a', {'class':'title may-blank '})

		total = len(gifImg)
		if total > 0:
			if total > 1:
			        gif = gifImg[randint(0,(total-1))]['href']
			else:
				gif = gifImg[0]['href']

		else:
		        gif = "Nothing man..."
		return gif

	def MessageStatus(self, msg, status):
		if status == Skype4Py.cmsReceived:
			#Skype from your list msg.FromDisplayName
			print msg.Body , msg.FromDisplayName, msg.Chat.Topic
			#msg.MarkAsSeen()
			match = re.match("@gif (.*)" , msg.Body, re.IGNORECASE)
			if match:
				typeGif = match.group(1)
				urlGif = self.getGif(typeGif)
				msg.Chat.SendMessage(urlGif)
			else:
				match = re.match("@urban (.*)" , msg.Body, re.IGNORECASE)
				if match:
					urban = match.group(1)
        	                        meaning = self.getUrban(urban)
	                                msg.Chat.SendMessage(meaning)
				else:
					match = re.match("@game" , msg.Body, re.IGNORECASE)
					if match:
						#reset players after one minute
						if len(self.players) > 3 and (time.time()-self.lastPlayer) > 60:
							self.players = []
 
						if len(self.players) > 3:
							msg.Chat.SendMessage("Already full! Players: "+self.players[0]+
										" - "+self.players[1]+" - "
										+self.players[2]+" - "
										+self.players[3])
						else:
							remain = (3-(len(self.players)))
							self.players.append(msg.FromDisplayName)
							if remain == 0:
								 msg.Chat.SendMessage("Lets play! Players: "+self.players[0]+
                                                                                " - "+self.players[1]+" - "
                                                                                +self.players[2]+" - "
                                                                                +self.players[3])
							else:
								msg.Chat.SendMessage("We need "+str(remain)+" player/s!")
							self.lastPlayer = time.time()


if __name__ == "__main__":
  bot = GifBot()
  
  while True:
    time.sleep(.2)
