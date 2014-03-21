import Skype4Py
import time
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
		   print elem.Topic

	def getGif(self, search):
		#r = requests.get("http://giphy.com/search/"+search)
		r = requests.get("http://www.reddit.com/r/gifs/search?q="+search+"+url%3A*.gif&sort=relevance&t=all")
		bs = BeautifulSoup.BeautifulSoup(r.text)

		#gifImg = bs.findAll('img', {'class':'gifs-gif unloaded'})
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
			print msg.Body , msg.FromDisplayName, msg.Chat.Topic
			#msg.MarkAsSeen()
			match = re.match("@gif (.*)" , msg.Body, re.IGNORECASE)
			if match:
				typeGif = match.group(1)
				urlGif = self.getGif(typeGif)
				msg.Chat.SendMessage(urlGif)
			
if __name__ == "__main__":
  bot = GifBot()
  
  while True:
    time.sleep(.2)
