#! /usr/bin/env python
# Copyright 2014 Ouwen Zha
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# This is the code for CS410 Assignment1
#
# run: python server.py

# try: curl -v -X GET http://127.0.0.1:8080/


# name:               Ouwen Zha
# ONE Card number:    1278820
# Unix id:            ouwen
# lecture section:    A1
# instructor's name:  Abram Hindle
# lab section:        H01
# TA's name:          li Sajedi Badashian 
# Homework:           A1
# Date:               january 17, 2014
# Collaboration:      None
# External source:    None 
import socket
import os

# this is used to connect the server
def Main():
	# get the directory
	os.chdir("www")
	retval = os.getcwd()

	# create socket
	s = socket.socket()

	# get host name
	host = "127.0.0.1"
	# port number
	port = 8080
 	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	# bind socket
	s.bind((host, port))

	# listen socket
	s.listen(5)
 
	# connect with client
	while True:
		try:		
			# wait connection
    			con, addr = s.accept()

			# use request funnction to deal with client's request
			request(con,retval)	
		except:
   			print "accept error"
		
	# close socket
	s.close()

# this is used to hand the request    
def request(con,retval):
	# receive request
        request = con.recv(1024)
		
	# split request to some lines
	request = request.split('\r\n')

	# get the first line of request
	firstline = request[0]

	# split the first line into some words
	firstline_array = firstline.split(' ')

	# get the path of file which client want to view
	filename = firstline_array[1]

	# get the length of path
	filename_length = len(filename)

	# if the last word of path is /, we will show index.html in this forlder
	if filename[filename_length-1] is '/':
		# return the root 
		returndir(retval)
		filename = filename + 'index.html'
	filename = filename[1:]

	# detemine file type
	file_type = filename.split('.')
	lastword_number = len(file_type)-1
	# get file extension
	lastword = file_type[lastword_number]
	situation = 0
	if lastword == 'css':
		situation = 1
	elif lastword == 'html':
		situation = 2
	else: 
		situation = 3
		filename = filename + '/index.html'

	# get the file content
	file_content = readfile(filename,situation,retval)

	# send file content
       	con.send(file_content)

	# close connection    
    	con.close()

# this is used to detemine the file exists or not, and read it
def readfile(path,situation,retval):
	if situation == 1:
		# header for css file
		file_content = 'HTTP/1.1 200 OK\nContent-Type: text/css\n\n'
	else:
		# header for html file
		file_content = 'HTTP/1.1 200 OK\nContent-Type: text/html\n\n'
	try:
		# open file
		read = open(path)
		# read fil  
		line=read.readline() 
		while line:  
 			file_content = file_content + line  
        		line=read.readline()
		# close file
		read.close  
		# if the file path is folder without slash, we will go to this folder
		if situation == 3:
			path_length = len(path) - 11
			newpath = path[:path_length]
			os.chdir(newpath)
	except:
		returndir(retval)
		try:
			# read file again
			read = open(path)  
			line=read.readline() 
			while line:  
 				file_content = file_content + line  
        			line=read.readline()
			read.close  
		except:
			# if we cannot find file, we will return this header
			file_content = 'HTTP/1.1 404 Not Found\n\nnot found'
	return file_content

# this is used to return to the root direcoty
def returndir(retval):
	while os.getcwd() != retval:
		os.chdir(os.pardir)

if __name__ == '__main__':
    Main()
