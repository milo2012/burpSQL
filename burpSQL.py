#!/usr/bin/python
import gds.pub.burp
import os,sys
from optparse import OptionParser
from pprint import pprint

sqlmapPath="/pentest/database/sqlmap/sqlmap.py"

dbms=""
cookie=""
filename=""
auto=""
urls={}

parser = OptionParser()
parser.add_option("-f", "--file", dest="filename",
                  help="Burp proxy logfile", metavar="burpProxyFile")
parser.add_option("-c", "--cookie", dest="cookie",
                  help="Cookie to use", metavar="cookieString")
parser.add_option("-d", "--dbms", dest="dbms",
                  help="Backend database", metavar="database")
parser.add_option("--domain", dest="domain",
                  help="Domain name", metavar="domainName")
parser.add_option("-a", "--auto",
                  action="store_true", dest="auto", default=False,
                  help="Answer 'Yes' to all sqlmap questions")

(options, args) = parser.parse_args()

if options.filename==None:
	print "[!] Please use -f or --filename and select a burp proxy file"
	sys.exit(0)

if options.auto!=False:
	auto="yes | "
else:
	auto=""

try:
   with open(options.filename) as f: pass
except IOError as e:
   print '[!] Problem opening burp proxy logfile: '+str(e)	
   sys.exit(0)
except NameError as e:
   print '[!] Problem opening burp proxy logfile: '+str(e)	
   sys.exit(0)

if options.dbms!=None:
	dbms=" --dbms="+options.dbms

proxylog = gds.pub.burp.parse(options.filename)
for i in proxylog:
	if(i.get_request_method()=='GET'):
		if options.domain!=None:
			if options.domain.lower() in i.host.lower():
				if options.cookie==None:
					cookie=i.get_request_header('Cookie')
				else:
					cookie=options.cookie
				url = i.host+i.get_request_path()
				if(len(i.get_request_body())>0):
					if i.get_request_body() not in urls:
						urls[i.get_request_body()]=cookie
		else:
			if options.cookie==None:
				cookie=i.get_request_header('Cookie')
			else:
				cookie=options.cookie
			url = i.host+i.get_request_path()
			if(len(i.get_request_body())>0):
				if i.get_request_body() not in urls:
					urls[i.get_request_body()]=cookie
	if(i.get_request_method()=='POST'):	
		if options.domain!=None:
			if options.domain.lower() in i.host.lower():
				if options.cookie==None:
					cookie=i.get_request_header('Cookie')
				else:
					cookie=options.cookie
				url = i.host+i.get_request_path()
				if(len(i.get_request_body())>0):
					if i.get_request_body() not in urls:
						urls[i.get_request_body()]=cookie
		else:
			if options.cookie==None:
				cookie=i.get_request_header('Cookie')
			else:
				cookie=options.cookie
			url = i.host+i.get_request_path()
			if(len(i.get_request_body())>0):
				if i.get_request_body() not in urls:
					urls[i.get_request_body()]=cookie

for k, v in sorted(urls.items()):	
	cmd = auto+"python "+sqlmapPath+" -u "+url+dbms+" --beep --data=\""+k+"\" --cookie=\""+v+"\""
	os.system(cmd)
