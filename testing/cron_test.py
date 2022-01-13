from datetime import datetime

def test_cron():
  f = open("/Users/danielmelchor/Documents/CodeProjects/covid-bot/crontext.txt", 'w')
  f.write("Cron ran at " + datetime.today().strftime("%m/%d/%Y %H:%M:%S"))
  f.close()
