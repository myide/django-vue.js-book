#coding=utf8
import requests

# get token
tk = requests.post('http://127.0.0.1:200/api-token-auth/', {'username':'u1', 'password':'1111qqqq'})

#headers = {'Authorization':'Token 4c5e7d66ec22f2db33c29e6ea41f3e2913805eaa'}
headers = {'Authorization':'Token %s' % eval(tk.content)['token']}
url = 'http://127.0.0.1:200/myapp/testapi/'
data = {
        'name':'yuqiuyu2', 
        'note':'aaa', 
        'books':'["sanchongmen" ]',
        }

# add author
#ret = requests.post(url, data=data, headers=headers)
#print ret.content

# delete book
ret = requests.delete('http://127.0.0.1:200/myapp/book/20', data={}, headers=headers)
print ret.content

''' get token
res = requests.post('http://127.0.0.1:200/api-token-auth/', {'username':'admin', 'password':'1111qqqq'})
print res.content
'''

