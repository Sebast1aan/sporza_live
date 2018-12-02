#script shows live scores of matches found on sporza
#written by Sebastiaan Lamproye (2018/12/02)

import requests
import io
import datetime
import os
from bs4 import BeautifulSoup

#colors which can be used for formatting output
class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

def sporza_live():
	url = 'https://sporza.be/nl/live/'
	source_code = requests.get(url)
	plain_text = source_code.text
	soup = BeautifulSoup(plain_text, 'html.parser')

	for matchdays in soup.find_all(class_="matchdays"):
		for competition in matchdays.find_all(class_="sc-titles"):
			competition_name = competition.find_all(class_="sc-header__title--normal")[0].text
			match_day = competition.find_all(class_="sc-header__title--thin")[0].text
			print(color.CYAN + competition_name + color.END + " -" + color.GREEN + match_day + color.END)

			for scoreboard in matchdays.find_all("a",class_="sc-scoreboard__match"):
				try:
					home_team = scoreboard.find_all(class_="sc-team__name")[0].text
					away_team = scoreboard.find_all(class_="sc-team__name")[1].text
					score_label = scoreboard.find_all(class_="sc-score__label")[0].text
					home_score = scoreboard.find_all(class_="sc-score sc-score__home")[0].text
					away_score = scoreboard.find_all(class_="sc-score sc-score__away")[0].text
					print('\t' + home_team + home_score + "-" + away_score + " " + away_team + "(" + score_label + ")")
				except:
					#home_score and away_score are not available if match has not started yet
					print('\t' + home_team + " - " + away_team + "(" + score_label + ")")
			print('')

sporza_live()
