# Using
Add import to this file python
```
sys.path.append('../')
import ParserBurp.parser as parser
```

Save request in folder python file

![](Screenshot%202023-10-18%20174344.png)

# Features
[x] send() => get or post request
```
requests.get(url = temp_url , headers = headers , proxies = proxies , verify = False)
---------------------------
requests.post(url = url , headers = headers , data = post_data , proxies = proxies , verify = False)
```
[x] gen_url() => url in requests

[x] get_method_and_resource() => method and source path and query value

[x] parse_request() => json header and json post data request
