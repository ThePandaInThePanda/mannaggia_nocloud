#! /usr/bin/env python
import re, random, time, argparse, subprocess, os
#####var
db = "santi_e_beati.txt"	#the santi e beati db
tts = "pico2wave -w"
tts_opt = "--lang=it-IT"
audiofile = "mannaggia.wav"	#name of the audiofile that will be created
player = "aplay -q"		#audio player
months = ["jan","feb","mar","apr","may","jun","jul","ago","sep","oct","nov","dec"]
month31 = ["jan","mar","may","jul","ago","oct","dec"]
month30 = ["apr","jun","sep","nov"]
#####argparse:
parser = argparse.ArgumentParser(prog="mannaggia-nocloud")
parser = argparse.ArgumentParser(description='Mannaggiatore off-the-cloud, idea from github.com/LegolasTheElf/mannaggia')
parser.add_argument('-w','--wait', help='wait time in seconds between one amnnaggia and the other',required=False,default=3)
parser.add_argument('-d','--date', help='do the mannaggia for a specific date express like "1 jan" or 23 dec"',required=False)
parser.add_argument('-r','--random', help='random day for santi e beati', action="store_true", default=False, required=False)
args = parser.parse_args()
#####random selection of month/day and manual selection of the day
if args.random :
        rm = random.choice(months)
	if rm == "feb":
		today = str(random.choice(range(1,28))) + " " + rm
	if rm in month30 :
		today = str(random.choice(range(1,30))) + " " + rm
	if rm in month31 : 
		today = str(random.choice(range(1,31))) + " " + rm
else: 
	if args.date is not None :
        	today = args.date
	else :
        	today = time.strftime("%d" + " " + "%b").lower().lstrip("0")
print "Mannaggiament in progress for the day: " + today		#debug: display the selected day
#####search day line in db, split the santi e beati of the day in a list and delete the day from the list
for line in open(db):
	if today in line:
		santig = line
		break
santi = re.split('\:|\;|\.', santig)
del santi[0]

while True :
	randommannaggia = random.choice(santi)#.strip('\n')
	mannaggia =  "Mannaggia a" + randommannaggia		#builds the text of the mannaggia
	print mannaggia
	mannaggia_cmd = tts + ' ' + audiofile + ' ' + tts_opt + ' \" ' + mannaggia + '\" && ' + player +  ' ' + audiofile 
	subprocess.call(mannaggia_cmd, shell=True) 		#send command to os
#	os.remove(audiofile)					#
	time.sleep(args.wait)					#wait for the spcified time
