# conote

## Online Note Application

### API Lists

所有的请求和回应都应该是 Json 格式的。

#### 注册

- URL: /user
- Type: POST
- Content-Type: application/json
- 请求示例:
~~~
{
	"username": "qhearting",
	"password": "qingr",
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
    "id": "40d8872ee44a11e69c646817294b73a4",
    "username": "qhearting",
    "email": "netcon@live.com"
  }
}
~~~

