[TOC]

# 亿方云Python SDK

亿方云Python版本SDK，集成亿方云V1系列API，具有强大的文件管理能力。该SDK可以运行在Python2.7和Python3的各个版之上。

## 安装

方法一：通过pip命令进行安装，请确保本地正常安装有Python和pip，并在命令行中输入如下命令：

> $ pip install fangcloud

方法二：通过源码安装，将源码克隆到本地，运行install命令

> $ git clone {git-url}
>
> $ cd {clone-path}
>
> $ python setup.py install

通过以上两种方法安装完成之后，通过python脚本检测是否成功安装。

> import fangcloud



## 创建应用

## 授权流程

亿方云开放平台API采用OAuth2.0协议进行授权。在SDK中提供了丰富的接口和简单的使用示例，方便开发者对接亿方云的OAuth流程。详细API说明，请参考[亿方云文档](https://open.fangcloud.com/wiki/#OAuth2)。

对接的Demo位于example/web-demo中，运行其中的main.py即可启动web服务。在浏览器中输入 "[http://localhost:8088](http://localhost:8088)" 进入demo流程。在使用之前请确保本地8088端口未被占用。web-demo使用tornado框架进行搭建，需在使用之前预先安装好。

### 获取授权链接

授权的第一步是获取授权链接，示例如下代码实现：

```python
from fangcloud.oauth import FangcloudOAuth2FlowBase
from fangcloud.yifangyun import YfyInit
YfyInit.init_system("YOUR_CLIENT_ID", "YOUR_CLIENT_SECRET")
state = utils.generate_new_state()
oauth = FangcloudOAuth2FlowBase()
authorize_url = oauth.get_authorize_url("YOUR_REDIRECT_URL", state)
```

其中需要输入在应用申请中获得的client id，client secret以及回调url。client id和client secret都为字符串，用以唯一表示一个应用；回调url是在授权过程中，传输授权码的渠道，由第三方开发者提供web服务。需要注意的是，在使用亿方云SDK之前，必须先调用YfyInit.init_system做初始化。

web-demo中提供了实现类：

```python
class AuthStartHandler(BasicHandler):

    def post(self, *args, **kwargs):
        username = self.get_login_user()
        user = self.__database__.get_user(username)
	    #check user login
        if user is None:
            response_page = utils.build_page("Error", "Nobody is logged in.")
            self.write(response_page)
            return

        # create a random stats, used for CSRF or remember web service current stats
        state = utils.generate_new_state()
        # the state can be stored in session
        self.set_state(state)
        # use SDK to fetch authorized url
        authorize_url = self.__oauth__.get_authorize_url(Config.redirect_url, state)
        self.redirect(authorize_url)
```

### 获取OAuth Token / Refresh Token

如果提供的回调url准确，授权流程最终会回调第三方提供的url ([http://YOUR_REDIRECT_URL?code=YOUR_AUTH_CODE](http://YOUR_REDIRECT_URL?code=YOUR_AUTH_CODE)）以完成授权码的传递。收到授权码之后，就可以利用授权码换取oauth token和refresh token。SDK中提供了简单的方法以供调用：

```python
oauth.FangcloudOAuth2FlowBase()
result = oauth.authenticate('YOUR_AUTH_CODE')
access_token, refresh_token = result.access_token, result.refresh_token
```

web-demo中提供了实现类：

```python
class AuthFinishHandler(BasicHandler):

    def get(self):
        code = self.get_argument("code", None)
        state = self.get_argument("state", None)
        username = self.get_login_user()
        user = self.__database__.get_user(username)
        if user is None:
            response_page = utils.build_page("Error", "Nobody is logged in.")
            self.write(response_page)
            return

        # check state
        state_in_session = self.get_state()
        if state != state_in_session:
            self.send_error(400, reason="Wrong state received")
        try:
            result = self.__oauth__.authenticate(code, Config.redirect_url)
        except OAuthCodeParamError:
            self.send_error(400, reason="Wrong oauth code to fetch oauth token")
            return
        except OAuthRedirectParamError:
            self.send_error(400, reason="Wrong oauth redirect url to fetch oauth")
            return
        self.write(str(result))
```

## 使用方法

亿方云提供开放平台V1版本的API，详细说明文档请参阅[API文档](https://open.fangcloud.com/wiki/#接口列表)。

一旦获取得到OAuth Token和Refresh Tokken就可以正常调用亿方云开放平台的API，首先需要公国SDK提供的工厂类方法，获取一个亿方云的client。同样，不要忘记先做init_system初始化。

```python
from fangcloud.yifangyun import YfyClientFactory
YfyInit.init_system("YOUR_CLIENT_ID", "YOUR_CLIENT_SECRET")
yfy_client = YfyClientFactory.get_client_instance("YOUR-USER-ID", access_token, refresh_token)
```

该工厂方法可以复用同一个用户的token，在第一次传入的时候需要指定OAuth Token和Refresh Tokken，后续可以通过用户ID直接获取：

```python
yfy_client = YfyClientFactory.get_client_instance("YOUR-USER-ID")
```

### 获取文件信息

```python
file_info = yfy_client.file().get_file_info(file_id)
print('file_name: '+file_info['name'])
```



## 测试

亿方云Python SDK采用[tox](https://tox.readthedocs.io/en/latest/)作为测试工具，兼容python2和python3版本，可以通过```pip install tox```命令来安装tox。要用tox来测试亿方云Python SDK，需要有OAuth Token，可以在tox命令之前加环境变量YFY_TOKEN将token传输进去：

> $ YFY_TOKEN=... tox

如果使用IDE，例如PyCharm或者Eclipse等IDE，来运行tox，请在IDE中进行配置运行时环境变量，或者在系统中配置环境变量，环境变量包括：

> * YFY_TOKEN
> * YFY_REFRESH_TOKEN
> * YFY_CLIENT_ID
> * YFY_CLIENT_SECRET

tox会自动读取环境变量，初始化测试例，执行测试代码。



## 技术支持

如有任何技术疑问，请联系亿方云开放平台管理员(email：[support@yifangyun.com](support@yifangyun.com))，我们会第一时间回复。