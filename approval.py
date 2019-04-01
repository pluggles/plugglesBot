#!/usr/bin/env python
import os
import subprocess

'''custom approve
upload specific phots for know users
default photo for unknow
give option to uplaod your own image'''
def approves(userID):
	EnsureDirExists('images')
	if EnsureFileExists('images/approval_' + str(userID) + '.jpg'):
		return 'images/approval_' + str(userID) + '.jpg'
	else:
		return 'images/approval_default'
		#check if userID has a picuture
		#is so send that picture back
		#else send default pictte
	#return p

def EnsureDirExists(path):
    if not os.path.exists(path):
        os.mkdir(path)

def EnsureFileExists(filename):
    if not os.path.exists(filename):
        return False
    return True
def deleteApprovalPhoto(userID):
	if os.path.exists('images/approval_' + str(userID) + '.jpg'):
		os.remove('images/approval_' + str(userID) + '.jpg')
		return "your photo has been removed with extreme prejudice"
	return "you don't have any approval photos added, you can add one with /approvalphoto"
def main():
	print approves("0001")
  

if __name__ == '__main__':
    main()