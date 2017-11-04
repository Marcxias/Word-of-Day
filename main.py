import json
import os

import requests
import arrow

from bs4 import BeautifulSoup


class MWWord(object):

	url = "https://www.merriam-webster.com/word-of-the-day"

	def __init__(self, url=None):
		self.url = url or "https://www.merriam-webster.com/word-of-the-day" 
		page = requests.get(self.url).text
		self.soup = BeautifulSoup(page, "html.parser")

	def getWord(self):
		return self.soup.h1.text.title()

	def getAttribute(self):
		return self.soup.select(".main-attr")[0].text

	def getDefinition(self):
		return list(filter(
			lambda x: ":" in x[:5],	
			map(
				lambda x: x.text,
				self.soup.select(".wod-definition-container")[0].select("p")
			)
		))

	def getExamples(self):
		return list(filter(
			lambda x: ":" not in x[:5],	
			map(
				lambda x: x.text.replace('\xa0', ' '),
				self.soup.select(".wod-definition-container")[0].select("p")
			)
		))

	def getYouKnow(self):
		return self.soup.select(".wod-did-you-know-container")[0].select("p")[0].text

	def getPodCastLink(self):
		return "https://rss.art19.com/episodes/{}.mp3".format(self.soup.select("#art19-podcast-player")[0]["data-episode-id"])


if __name__ == '__main__':
	
	todayWord = MWWord()
	date = arrow.utcnow().to('Asia/Shanghai').format('YYYY-MM-DD')

	with open(f"{date}.json", "w") as f:
		json.dump({
			"word": todayWord.getWord(),
			"attr": todayWord.getAttribute(),
			"definition": todayWord.getDefinition(),
			"example": todayWord.getExamples(),
			"background": todayWord.getYouKnow(),
			"podcast": todayWord.getPodCastLink()
			}, f, indent=4, ensure_ascii=False)
