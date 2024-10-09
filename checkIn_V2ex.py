# 青龙签到
'''
new Env('v2ex 自动签到')
cron: 0 9 * * *

添加cookies，名字 V2EX_COOKIE

'''



import os
import sys
import requests
import re
from bs4 import BeautifulSoup
from utils.notify import send  # 导入消息通知模块

def extract_single_quotes_content(string):
    # 使用正则表达式匹配单引号中的内容
    match = re.findall(r"'(.*?)'", string)
    return match

def parse_cookie_string(cookie_string):
    # 移除字符串两端的空格，并按 `;` 分割
    cookie_list = cookie_string.strip().split(';')
    
    # 创建字典存储键值对
    cookie_dict = {}
    
    for cookie in cookie_list:
        # 再按 `=` 分割键和值
        if '=' in cookie:
            key, value = cookie.split('=', 1)
            cookie_dict[key.strip()] = value.strip()  # 去掉两端的空格
            
    return cookie_dict

cookies_str=os.environ.get('V2EX_COOKIE')

# 自定义的 Cookies
cookies = parse_cookie_string(cookies_str)

print(cookies)


# 获取网页HTML
url = 'https://v2ex.com/mission/daily'
response = requests.get(url, cookies=cookies)
html_content = response.text

# 使用BeautifulSoup解析HTML
soup = BeautifulSoup(html_content, 'html.parser')

# 查找class为'button'的input元素
button_input = soup.find('input', {'class': 'button'})

# 获取input元素的跳转地址
if button_input and 'onclick' in button_input.attrs:
    # 假设跳转地址在onclick属性中
    onclick_value = button_input['onclick']
    path = extract_single_quotes_content(onclick_value)[0]
    day_url = "https://v2ex.com" + path
    print(f"跳转地址: {day_url}")
    response = requests.get(day_url, cookies=cookies)
    
    # 输出返回结果
#   print(response.status_code)  # 输出响应状态码
#   print(response.text)  # 输出响应内容
    
    # 使用BeautifulSoup解析HTML
    soup_response = BeautifulSoup(response.text, 'html.parser')
    # 查找class为'cell'的div元素
    cell_divs = soup.find_all('div', {'class': 'cell'})
    div_list = []
    for i, div in enumerate(cell_divs):
        print(f"第 {i+1} 个div元素:")
        # 输出div的文本内容
        div_content = div.get_text(strip=True)  # strip=True移除多余的空白字符
        div_list.append(div_content)
        print(div_content)
        
    if 200 == response.status_code:
        print("签到ok")
        msg = "签到成功:" + div_list.pop()
        send("v2ex签到", msg)

else:
    print("没有找到class为'button'的input元素或onclick属性")
