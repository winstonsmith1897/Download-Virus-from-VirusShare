import requests
from bs4 import BeautifulSoup
from termcolor import colored
import subprocess

burp0_url = "https://virusshare.com:443/search"
burp0_cookies = {"SESSID": "session_cookie"}
burp0_headers = {"Cache-Control": "max-age=0", "Sec-Ch-Ua": "\"Not;A=Brand\";v=\"99\", \"Chromium\";v=\"106\"", "Sec-Ch-Ua-Mobile": "?0", "Sec-Ch-Ua-Platform": "\"Windows\"", "Upgrade-Insecure-Requests": "1", "Origin": "https://virusshare.com", "Content-Type": "application/x-www-form-urlencoded", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.5249.62 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Referer": "https://virusshare.com/", "Accept-Encoding": "gzip, deflate", "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7", "Connection": "close"}

print('Reading hashes... This could take few minutes.')
file = open('/mnt/d/VIRUS/virushashes.txt', 'r')
lines = file.readlines()

for hash in lines:
	print(colored('HASH ==> ' + hash, 'blue'))
	burp0_data = {"search": str(hash)}
	response = requests.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data)
	if b"apk" in response.content:
		print(colored("[OK] - " + str(hash), 'green'))
		text = response.content
		soup = BeautifulSoup(text, 'lxml')
		comp = soup.find_all('td')
		link = str(comp).split('align="center" valign="bottom" width="20%"><a href="download?', 1)[1].split('" title="Download file"><')[0]
		complete_link = "https://virusshare.com/download?" + link
		print(colored('LINK ==> ' + complete_link, 'yellow'))
		subprocess.run(["curl", "-v", "--cookie", "SESSID=session_cookie", complete_link])
	else :
		print(colored("[NO] - " + str(hash), 'red'))
