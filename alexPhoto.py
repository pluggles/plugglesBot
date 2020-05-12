#!/usr/bin/env python
import os
import random
import subprocess


'''custom approve
upload specific phots for know users
default photo for unknow
give option to uplaod your own image'''
ImgPath = "AlexPhotos"
def Alex():
	EnsureDirExists(ImgPath)
	if os.listdir(ImgPath) == []:
		return 'No Photos Exist'
	else:
		return random.choice(os.listdir(ImgPath))
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

def deleteDisapprovalPhoto(userID):
	if os.path.exists('images/disapproval_' + str(userID) + '.jpg'):
		os.remove('images/disapproval_' + str(userID) + '.jpg')
		return "your photo has been removed with extreme prejudice"
	return "you don't have any disapproval photos added, you can add one with /disapprovalphoto"
def main():
	print Alex()
  

if __name__ == '__main__':
    main()