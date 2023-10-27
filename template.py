import requests
import string
import sys
sys.path.append('../')
import ParserBurp.parser as parser

FILE = "lab3.txt"
requests.packages.urllib3.disable_warnings() #disable warning cert ssl
char = ''.join(string.ascii_lowercase+string.digits+string.ascii_uppercase)
proxy={"https":"http://localhost:8080"} 
data = []

def run():
    # work somethings
    method , path , query_get = parser.get_method_and_resource(FILE)
    headers , post_data = parser.parse_request(FILE)
    url = parser.gen_url(https=True, headers = headers , resource_name = path , query_get = query_get)
    parser.put(method,url,headers,proxy)
    result = parser.sends()


if __name__ == '__main__':
    run()
