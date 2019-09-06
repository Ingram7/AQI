import execjs
import json
import requests

# Init environment
# 通过 execjs（即 PyExecJS）的 get() 方法声明一个运行环境
node = execjs.get()

# Params
# 换成'GETCITYWEATHER'获取温度，风向等数据
# method = 'GETDETAIL'  获取aqi，pm2.5等数据
method = 'GETCITYWEATHER'
city = '重庆'
type = 'HOUR'
start_time = '2019-09-06 00:00:00'
end_time = '2019-09-06 12:00:00'

# Compile javascript
file = 'encryption.js'
# 调用 compile() 方法来执行刚才保存下来的加密库 encryption.js，执行一遍才能调用
with open(file, encoding=('utf-8')) as f:
    ctx = node.compile(f.read())

# Get params
# 调用一下 JavaScript 中的 getEncryptedData() 方法即可实现加密
# 通过 eval() 方法来模拟执行，得到的结果赋值为 params，这个就是 POST Data 的加密数据
js = 'getEncryptedData("{0}", "{1}", "{2}", "{3}", "{4}")'.format(method, city, type, start_time, end_time)
params = ctx.eval(js)

# Get encrypted response text
url = 'https://www.aqistudy.cn/apinew/aqistudyapi.php'
response = requests.post(url, data={'d': params})

# Decode data
# 调用一下 JavaScript 中的 decodeData() 方法即可实现解密
js = 'decodeData("{0}")'.format(response.text)
decrypted_data = ctx.eval(js)

data = json.loads(decrypted_data)
res = data.get('result').get('data').get('rows')
for i in res:
    print(i)