import requests
from urllib.parse import urlparse,parse_qs,quote
from urllib3.exceptions import InsecureRequestWarning
import json
import concurrent.futures
import copy

debug = False
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

#sau dong dau tien
def parse_request(file_name):
	line = ""
	headers = {}
	post_data_temp = ""
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
			post_data_temp = post_data_temp + line
	file_object.close()
	if post_data_temp != "":
		if post_data_temp.startswith("{"):
			post_data = json.loads(post_data_temp)
		else:
			post_data = parse_qs(post_data_temp)
	else:
		post_data = post_data_temp
	return (headers , post_data)

#dong dau tien
def get_method_and_resource(file_name):
	file_object = open(file_name , "r")
	request_line = file_object.readline()
	file_object.close()
	request_line = request_line.split(" ")
	method = request_line[0]
	path = urlparse(request_line[1]).path
	query_get = parse_qs(urlparse(request_line[1]).query)
	return method , path , query_get

def gen_url(https = False,headers = None, resource_name = None , query_get = None):
	protocol = "https" if (https is True) else "http"
	temp = ""
	if (query_get is not None) and (query_get != ""):
		for key in query_get:
			value = query_get[key]	
			temp = "?" + key + "=" + value
	url = protocol + "://" + headers["Host"] + resource_name + temp
	return url

# def parse_query_get(query_get):
# 	json_query_get = parse_qs(query_get)
# 	print(json_query_get)
# 	return {k:v[0] if v and len(v) == 1 else v for k,v in json_query_get.items()}


#send request get or post
def send(proxies = None, headers = None, post_data = None, method = None, url = None,s=None):
	if s is None:
		s = requests.Session()
	if method.lower() == "get":
		temp = urlparse(url)
		temp_url = temp.scheme + "://" + temp.netloc + temp.path + "?" + quote(temp.query,safe="=%")
		response = s.get(url = temp_url , headers = headers , proxies = proxies , verify = False)
	elif method.lower() == "post":
		if post_data.startswith("{"):
			post_data = json.dumps(post_data)
		response = s.post(url = url , headers = headers , data = post_data , proxies = proxies , verify = False)
	return response

#generate list task
tasks = []
def put(method,url,headers,proxy=None,post_data=None):
	try:
		new_post_data = copy.deepcopy([method,url,headers,proxy,post_data])
		tasks.append(new_post_data)
	except:
		print("Error in Put function")

#multi thread
def sends():
	s = requests.Session()
	futures = []
	result = []
	with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
		for task in tasks:
			futures.append(executor.submit(send,proxies=task[3],headers=task[2],post_data=task[4],method=task[0],url=task[1],s=s))
		for future in concurrent.futures.as_completed(futures):
			result.append(future.result())
		tasks.clear()
	return result
