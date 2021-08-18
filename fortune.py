#!/usr/bin/env python
import os
import subprocess
def fortune(args):
	try:
		args = args.split( )
		cmd = []
		cmd.append('/usr/games/fortune')
		for arg in args:
			if arg.startswith("-"):
				arg = arg.replace('w', '')
				arg = arg.replace('m', '')
				arg = arg.replace('i', '')
				arg = arg.replace('n', '')
				if len(arg) == 1:
					arg = "-a"
			cmd.append(arg)
		p = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
		return p
	except subprocess.CalledProcessError as error:
		print error
		return "That was not a valid option for fortune."
	#return p
def fortuneHelp():
	return """print a random, hopefully interesting, adage
	usage: '/fortune <args> fileName'
	allowed flags are: -acefilosu 
	please note:
	[-n length] and [ -m pattern]
	DO NOT WORK"""

def cowsay(args):
	try:
		#print args
		cmd = []
		cmd.append('/usr/games/cowsay')
		cmd.append('-W 25')
		for arg in args:
			arg = arg.replace("-", "")
			cmd.append(arg)
		p = subprocess.check_output(cmd)
		return p

	except subprocess.CalledProcessError as error:
		#print error
		return "That was not a valid option for cowsay."
def madcow(args):
	try:
		#print args
		cmd = []
		cmd.append('/usr/games/cowsay')
		cmd.append('-d')
		cmd.append('-W 25')
		for arg in args:
			cmd.append(arg)
		p = subprocess.check_output(cmd)
		#print p
		return p

	except subprocess.CalledProcessError as error:
		print error
		return "That was not a valid option for fortune."
def main():

   p = fortune('-o')
   #print p
   p = cowsay(([p]))
   print p

if __name__ == '__main__':
    main()