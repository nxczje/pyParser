import requests
from urllib.parse import urlparse, urlencode,parse_qs,quote
from urllib3.exceptions import InsecureRequestWarning

debug = False
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

#sau dong dau tien
def parse_request(file_name):
	line = ""
	headers = {}
	post_data = ""
	header_collection_done = False
	file_object = open(file_name , "r")
	file_object.seek(0)
	file_object.readline()
	for line in file_object.readlines():
		if header_collection_done is False:
			if line.startswith("\n"):
				header_collection_done = True
			else:
				headers.update({
					line[0:line.find(":")].strip() : line[line.find(":")+1 :].strip()
				})
		else:
			post_data = post_data + line
	file_object.close()
	return (headers , post_data)

#dong dau tien
def get_method_and_resource(file_name):
	file_object = open(file_name , "r")
	request_line = file_object.readline()
	file_object.close()
	request_line = request_line.split(" ")
	method = request_line[0]
	path = urlparse(request_line[1]).path
	query_get = urlparse(request_line[1]).query
	return method , path , query_get

def gen_url(https = False,headers = None, resource_name = None , query_get = None):
	protocol = "https" if (https is True) else "http"
	if (query_get is not None) and (query_get != ""):
		query_get = "?" + query_get
	url = protocol + "://" + headers["Host"] + resource_name + query_get
	return url

# def parse_query_get(query_get):
# 	json_query_get = parse_qs(query_get)
# 	print(json_query_get)
# 	return {k:v[0] if v and len(v) == 1 else v for k,v in json_query_get.items()}


#send request get or post
def send(proxies = None, headers = None, post_data = None, method = None, url = None):
	if method.lower() == "get":
		temp = urlparse(url)
		temp_url = temp.scheme + "://" + temp.netloc + temp.path + "?" + quote(temp.query,safe="=%")
		response = requests.get(url = temp_url , headers = headers , proxies = proxies , verify = False)
	elif method.lower() == "post":
		response = requests.post(url = url , headers = headers , data = post_data , proxies = proxies , verify = False)
	return response