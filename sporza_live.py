#script shows live scores of matches found on sporza
#written by Sebastiaan Lamproye (2018/12/02)

import requests
import sys
import time
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

def main():
    check_args()

def sporza_live():
    url = 'https://sporza.be/nl/live/'
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html.parser')

    print(time.asctime(time.localtime(time.time())))

    for matchdays in soup.find_all(class_="matchdays"):
        for competition in matchdays.find_all(class_="sc-titles"):
            if len(competition.find_all(class_="sc-header__title--normal")) > 0:
                competition_name = competition.find_all(class_="sc-header__title--normal")[0].text
            else:
                competition_name = ""

            if len(competition.find_all(class_="sc-header__title--thin")) >  0:
                match_day = competition.find_all(class_="sc-header__title--thin")[0].text
            else:
                match_day = ""
                
            print(color.CYAN + competition_name + color.END + " -" + color.GREEN + match_day + color.END)

            for scoreboard in matchdays.find_all("a",class_="sc-scoreboard__match"):
                try:
                    home_team = scoreboard.find_all(class_="sc-team__name")[0].text
                    away_team = scoreboard.find_all(class_="sc-team__name")[1].text
                    score_label = scoreboard.find_all(class_="sc-score__label")[0].text
                    home_score = scoreboard.find_all(class_="sc-score sc-score__home")[0].text
                    away_score = scoreboard.find_all(class_="sc-score sc-score__away")[0].text

                    #score_label is empty for some reason if value is 'rust'
                    if score_label == "":
                        score_label = "rust"
                    print('\t' + home_team + home_score + "-" + away_score + " " + away_team + "(" + score_label + ")")
                except:
                    #home_score and away_score are not available if match has not started yet
                    print('\t' + home_team + " - " + away_team + "(" + score_label + ")")
            print('')

def check_args():
    nrofarguments = len(sys.argv)
    if nrofarguments == 1:
        sporza_live()
    elif nrofarguments == 2:
        if sys.argv[1] == "-h":
            help_instr()
        else:
            try:
                polling_time = float(sys.argv[1])
                while True:
                    sporza_live()
                    time.sleep(polling_time)
            except:
                help()
    elif nrofarguments == 3:
        try:
            polling_time = float(sys.argv[1])
            if sys.argv[2] == "-c":
                while True:
                    print("\033c") #clear screen
                    sporza_live()
                    time.sleep(polling_time)
            else:
                help()
        except:
            help()
    else:
        help()

def help():
    print("invalid number of arguments or invalid argument values")
    print("for help, type: python " + sys.argv[0] + " -h")

def help_instr():
    print("- to run the script only once, type: python " + sys.argv[0])
    print("- to have the script update automatically each x seconds, type: python " + sys.argv[0] + " %NrOfSeconds%")
    print("- to have the script update automatically each x seconds and also clear the screen, type: python " + sys.argv[0] + " %NrOfSeconds%" + " -c")

if __name__ == "__main__":
    main()
