# Moguding

<p align="center">
    <img src="images/Logo.png" alt="Logo" heghit=30% width=30%>
</p>

<p align="center">
    <h1 align="center">蘑菇丁自动签到</h1>
</p>

## 🔥 特性
- ✅自动 `上班/下班` 签到

## ❗注意
* 上班签到时间 `8:30` 下班签到时间 `17:30`
* `Github Actions` 运行期间如果打开App上线，会导致签到失败


## ⚙ 部署
### 1. Fork 仓库

* 项目地址：[github/Moguding](https://github.com/Chiai/Moguding)
* 点击右上角 `Fork` 到自己的账号下
> ![Fork][Fork-screenshot]


### 2. 添加 参数 至 Secrets

* 回到项目页面，依次点击 `Settings` --> `Secrets` --> `New secret`
> ![Setting.png][Settings-screenshot]
* 示例：
* 创建一个名为 `Phone` 的 secret，值为 `蘑菇钉账号`，最后点击`Add secret`
> ![Secret][Secret-screenshot]


🛠 参数： \
共需要创建3个 `secret`， 分别为 `Phone`，`Pasword`，`Address`，否者会报错，参照上面 `示例` 添加步骤,以下是参数介绍

```
    Phone           # 账号
    Password        # 账号密码
    Address         # 签到地址
```


### 3. 启用 Actions

返回项目主页面，点击上方的 `Actions`，这时候会提示 `Workflows` 在 `Fork` 的仓库中无法运行”，接下来点击 `I understand my workflows. go ahead and enable them` 确认开启 `Workflows`
> ![Actions][Actions-screenshot]

至此，部署完毕。


## 🔍结果
* `START Type` 为上班签到
* `End Type` 为下班签到

当你完成上述流程，可以在Actions页面点击 [`START Type` | `End Type`] --> `build` --> `Run sign` 查看结果。\
如果成功，会输出类似'msg': 'Success'的信息：
```
    2021-05-09 19:20:54 INFO sleep for 0 seconds ...        
    2021-05-09 19:20:56 INFO {'code': 200, 'msg': 'success'}
    2021-05-09 19:20:54 INFO 上班打卡成功.
```

如果失败，会输出 `Plase check username or password.`




## ☑️ Todo
- 自动定期提交 `周报` 


[Fork-screenshot]: images/Fork.png
[Settings-screenshot]: images/Settings.png
[Secret-screenshot]: images/Secret.png
[Actions-screenshot]: images/Actions.png