#! /usr/bin/env python

#description: --------------------------------------------------------------------
#this antistress tool was born after using LegolasTheElf's Automatic saint invocation 
#for depressed Veteran Unix Admins, called "mannaggia". 
#Since it uses www.santiebeati.it to get today's saints and Google's text to speech 
#for the voice part, basically it uses the cloud. 
#But we think the cloud would be utter shit, if it only existed. 
#This tool likes to be an off-the-(fucking-)cloud improved version of the original 
#mannaggia.


#import --------------------------------------------------------------------------
import re, random, time, argparse, subprocess, os

#var -----------------------------------------------------------------------------
imprecazione = "Mannaggia " 	#the imprecation to be used as standard
dbfolder = "db/"		#folder of the db files
dbfile = "db/santi_e_beati.txt"	#the santi e beati db
tts = "pico2wave -w"		#default text to speech software
tts_opt = "--lang=it-IT"	#default option for the text to speech software
audiofile = "mannaggia.wav"	#name of the audiofile that will be created
player = "aplay -q"		#default audio player
re_attribution = re.compile(r"\(.*\)$")	#regular expression to manage prcd db files

#months praparation---------------------------------------------------------------
months = ["jan","feb","mar","apr","may","jun","jul","ago","sep","oct","nov","dec"]
month31 = ["jan","mar","may","jul","ago","oct","dec"]
month30 = ["apr","jun","sep","nov"]

#argparse: -----------------------------------------------------------------------
parser = argparse.ArgumentParser(prog="mannaggia-nocloud")
parser = argparse.ArgumentParser(description='Mannaggiatore off-the-cloud, idea from github.com/LegolasTheElf/mannaggia')
#parser.add_argument('-n','--nofm', help='no fm streaming (mainly for raspberrys)', required=False,default=False)
parser.add_argument('-w','--wait', help='wait time in seconds between one amnnaggia and the other',required=False,default=3)
parser.add_argument('-d','--date', help='do the mannaggia for a specific date express like "1 jan" or 23 dec"',required=False)
parser.add_argument('-r','--random', help='random day for santi e beati', action="store_true", default=False, required=False)
parser.add_argument('-b', '--database', help='database file', default=dbfile, required=False)
args = parser.parse_args()

#random selection of month/day and manual selection of the day--------------------
db = args.database				#simplify the db variable reading from arguments
if "prcd" not in db:				#if the db is not a prcd the procedure to get the correct santi for the date is executed:
	if args.random :
        	rm = random.choice(months)	#if the random argument is selected, select a random month to mannaggiate
		if rm == "feb":
			today = str(random.choice(range(1,28))) + " " + rm
		if rm in month30 :
			today = str(random.choice(range(1,30))) + " " + rm
		if rm in month31 : 
			today = str(random.choice(range(1,31))) + " " + rm
	else: 
		if args.date is not None :	#if the date argument is selected set the date or if was not specified use system date to mannagiate today's santi
        		today = args.date
		else :
        		today = time.strftime("%d" + " " + "%b").lower().lstrip("0")
	print "Mannaggiament in progress for the day: " + today		#debug: display the selected day
	for line in open(db):						#create the list with the santi of the date selected
        	if today in line:
                	santig = line
                	break
	santi = re.split('\:|\;|\.', santig)
	del santi[0]
else:									#if the db is a prcd one create the list
	with open(db) as fd:						#open the file
		santi = fd.readlines()					#read the lines of the file creating a list
	santi = [re_attribution.sub("",x.lower()) for x in santi]	#for every line set all the text in lowercase and, with the regular expression, remove everything between "()"


#main loop: ----------------------------------------------------------------------
while True :
	randommannaggia = random.choice(santi)#.strip('\n') 	#check the first word of the random mannaggia and apply article accordingly
	if "madonna" in randommannaggia.split(' ', 1)[0]:
		articolo = "alla"
	elif "papa" in randommannaggia.split(' ', 1)[0]:
                articolo = "al"
	elif "vsf" in db:					#particular case for a db file of aphorisms, imprecazione not needed
		imprecazione = ""
		articolo = ""
	else:
		articolo = "a"
	mannaggia =  imprecazione + " " + articolo + " " + randommannaggia		#builds the text of the mannaggia
	print mannaggia
	mannaggia_cmd = tts + ' ' + audiofile + ' ' + tts_opt + ' \" ' + mannaggia + '\" && ' + player +  ' ' + audiofile 
	subprocess.call(mannaggia_cmd, shell=True) 		#send command to os
#	os.remove(audiofile)					#
	time.sleep(args.wait)					#wait for the spcified time
