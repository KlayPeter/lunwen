# 后端测试截图命令

本文档整理的是“能直接在终端输出结果、适合截图取证”的后端测试命令。  
运行这些命令时，必须先切到你**实际项目目录**，不要在当前论文目录直接执行。

## 一、先启动后端

先开一个 PowerShell 窗口，进入项目根目录并启动后端：

```powershell
cd F:\你的项目根目录
node .\server\server.js
```

这一个窗口不要关闭，后续可以截图以下信息：

- 服务启动成功
- 监听端口 `3000`
- 数据库连接成功
- 后端收到请求后的日志输出

## 二、烟雾测试

再开第二个 PowerShell 窗口，执行：

```powershell
curl.exe -i http://localhost:3000/api/user/test
```

这个命令适合截图以下信息：

- 请求地址是 `http://localhost:3000/api/user/test`
- 返回状态码 `200`
- 返回的测试 JSON 内容

## 三、确认 3000 端口真的在监听

```powershell
netstat -ano | findstr :3000
```

这个命令适合截图以下信息：

- 本机 `3000` 端口处于监听状态
- 证明后端进程已经实际启动

## 四、登录接口测试

如果你的登录接口是论文里写的 `/api/user/login-email`，可以执行：

```powershell
$body = @{ email = "你的测试邮箱"; password = "你的密码" } | ConvertTo-Json
$login = Invoke-RestMethod -Method Post -Uri "http://localhost:3000/api/user/login-email" -ContentType "application/json" -Body $body
$login | ConvertTo-Json -Depth 6
$token = $login.token
```

这个命令适合截图以下信息：

- 登录接口地址
- 返回成功结果
- 返回的 `token`
- 返回的用户对象

如果你的项目登录字段不是 `email` 和 `password`，就把上面的字段名改成你项目真实使用的字段名。

## 五、用户信息接口测试

拿到 `token` 之后执行：

```powershell
curl.exe -i http://localhost:3000/api/user/info -H "Authorization: Bearer $token"
```

这个命令适合截图以下信息：

- 请求头里带了 `Bearer Token`
- 返回状态码 `200`
- 返回当前用户的昵称、邮箱、头像或用户 ID

## 六、无效 Token 拦截测试

```powershell
curl.exe -i http://localhost:3000/api/user/info -H "Authorization: Bearer fake_token"
```

这个命令适合截图以下信息：

- 同一个接口地址
- 无效令牌被拦截
- 返回 `401`、`403` 或未授权提示

这张图很适合证明后端权限校验确实生效。

## 七、附带耗时的接口输出

如果你想把“响应时间”也一起截图，可以执行：

```powershell
curl.exe -o NUL -s -w "status=%{http_code} time=%{time_total}s`n" http://localhost:3000/api/user/test
```

如果要测用户信息接口：

```powershell
curl.exe -o NUL -s -w "status=%{http_code} time=%{time_total}s`n" http://localhost:3000/api/user/info -H "Authorization: Bearer $token"
```

这个命令适合截图以下信息：

- 状态码
- 总耗时

## 八、如果项目里有 AI 测试脚本

你的论文正文里写到了两个脚本：

- `server/test-ai-quick.js`
- `server/test-chatroom-ai.js`

如果这两个脚本在你的真实项目目录里存在，可以执行：

```powershell
cd F:\你的项目根目录\server
node .\test-ai-quick.js
node .\test-chatroom-ai.js
```

这两个命令适合截图以下信息：

- AI 请求是否执行成功
- 返回内容是否正常
- 耗时是否正常
- 聊天室 AI 链路是否跑通

## 九、最推荐的截图组合

为了让老师一眼看出“这是后端测试证据”，建议这样拍：

1. 左侧窗口保留 `node .\server\server.js` 的运行日志。
2. 右侧窗口执行 `curl.exe -i ...` 或 `node .\test-ai-quick.js`。
3. 截图时保留以下锚点信息：

- `localhost:3000`
- 测试账号
- 测试房间名
- 状态码
- 时间或耗时

## 十、建议直接截图的四类命令

如果你时间不多，优先截图这四组：

```powershell
curl.exe -i http://localhost:3000/api/user/test
```

```powershell
$body = @{ email = "你的测试邮箱"; password = "你的密码" } | ConvertTo-Json
$login = Invoke-RestMethod -Method Post -Uri "http://localhost:3000/api/user/login-email" -ContentType "application/json" -Body $body
$login | ConvertTo-Json -Depth 6
$token = $login.token
```

```powershell
curl.exe -i http://localhost:3000/api/user/info -H "Authorization: Bearer $token"
```

```powershell
curl.exe -i http://localhost:3000/api/user/info -H "Authorization: Bearer fake_token"
```

这四张图基本就能支撑：

- 服务可用
- 登录成功
- 鉴权成功
- 鉴权拦截生效

如果你后面把真实项目目录告诉我，我可以继续把这份命令改成“完全按你项目接口字段名和路径写死”的版本。
