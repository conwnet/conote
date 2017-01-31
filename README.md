# conote

[![Build Status](https://travis-ci.org/springhack/conote.svg?branch=master)](https://travis-ci.org/springhack/conote)

## Online Note Application

### API Lists

所有的请求和回应都应该是 Json 格式的。
返回的 Json 中，如果 error 的值是 null，说明请求正常，否则请求出错。

#### 注册

- URL: /user
- Type: POST
- Content-Type: application/json
- 请求示例:
~~~
{
	"username": "netcon",
	"password": "123456",
	"email": "netcon@live.com",
	"verify_code": "0000"
}
~~~
- 应答示例:
~~~
{
  "error": null
}
~~~
- 其它: 若 error 不为 null，则注册失败。


## 登录

- URL: /login
- Type: POST
- Content-Type: application/json
- 请求示例:
~~~
{
	"username": "netcon",
	"password": "123456"
}
~~~
- 应答示例:
~~~
{
  "error": null
}
~~~
- 其它: 若 error 不为 null，则注册失败。


#### 根据 id/username 获取用户信息

- URL:
 - /user/id/{id}
 - /user/username/{username}
- Type: GET
- 应答示例:
~~~
{
  "error": null,
  "user": {
    "id": "75cb3c8ce47611e69ade6817294b73a4",
    "username": "netcon"
  }
}
~~~


#### 添加/更新 note

- URL: /note
- Type: POST
- Content-Type: application/json
- 请求示例:
 - 增加 note
~~~
{
    "id": "happy new year.",
	"title": "日记 2017-01-27",
	"content": "今天过年了，我还在苦逼的写代码。",
	"public": 7
}
~~~
 - 更新 note：
~~~
{
    "id": "f6d30c76e47b11e699156817294b73a4",
	"title": "日记 2017-01-27",
	"content": "今天过年了，虽然我在写代码，但是我一点都不觉得苦逼。",
	"public": 7
}
~~~
- 应答示例:
~~~
{
  "error": null
}
~~~
- 其它：
~~~
public 是 note 的对于其它用户的权限
4 - 其他人可读
2 - 其他人可以修改
1 - 其他人可以删除
~~~

### 获取本人所有 note

- URL: /note
- Type: GET
- Content-Type: application/json
- 请求示例:
~~~
http://localhost:9000/note
~~~
- 应答示例
~~~
{
  "error": null,
  "notes": {
    "f6d30c76e47b11e699156817294b73a4": {
      "title: ": "日记 2017-01-27"
    }
  }
}
~~~~


#### 根据 id 查询 note
- URL: /note/id/{id}
- Type: GET
- Content-Type: application/json
- 请求示例:
~~~
http://localhost:9000/note/id/f6d30c76e47b11e699156817294b73a4
~~~
- 应答示例:
~~~
{
  "error": null,
  "note": {
    "id": "f6d30c76e47b11e699156817294b73a4",
    "title": "日记 2017-01-27",
    "author_id": "75cb3c8ce47611e69ade6817294b73a4",
    "content": "今天过年了，我还在苦逼的写代码。",
    "public": 7,
    "create_at": 1485511209.00486
  }
}
~~~
