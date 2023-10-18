import requests
import string
import sys
sys.path.append('../')
import ParserBurp.parser as parser

FILE = "req3.txt"
requests.packages.urllib3.disable_warnings() #disable warning cert ssl
char = ''.join(string.ascii_lowercase+string.digits+"."+":")
proxy={"https":"http://localhost:8080"} 
data = []
def run():
    s = requests.Session()
    # work somethings
    method , path , query_get = parser.get_method_and_resource(FILE)
    headers , post_data = parser.parse_request(FILE)
    test = "test"
    url = parser.gen_url(https=True, headers = headers , resource_name = path , query_get = test)
    res = parser.send(method = method, url = url, headers=headers, proxies=proxy)
    print(res.text)
    

if __name__ == '__main__':
    run()
