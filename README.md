## 亿方云Python SDK

亿方云Python版本SDK，集成亿方云V1系列API，具有强大的文件管理能力。该SDK可以运行在Python2.7和Python3的各个版之上。

### 安装

方法一：通过pip命令进行安装，请确保本地正常安装有Python和pip，并在命令行中输入如下命令：

> $ pip install yifangyun

方法二：通过源码安装，将源码克隆到本地，运行install命令

> $ git clone
>
> $ cd path
>
> $ python setup.py install

通过以上两种方法安装完成之后，通过python脚本检测是否成功安装。

> import yifangyun



### 创建应用





### 授权流程

亿方云开放平台API采用OAuth2.0协议进行授权。在SDK中提供了丰富的接口和简单的使用示例，方便开发者对接亿方云的OAuth流程。详细API说明，请参考[亿方云文档](https://open.fangcloud.com/wiki/#OAuth2)。

对接的Demo位于example/web-demo中，运行其中的main.py即可启动web服务。在浏览器中输入"http://localhost:8088"进入demo流程。在使用之前请确保本地8088端口未被占用。web-demo使用tornado框架进行搭建，需在使用之前预先安装好。

#### 获取授权链接

授权的第一步是获取授权链接，示例如下代码实现：

```python
from fangcloud.oauth import FangcloudOAuth2FlowBase
# create a random stats, used for CSRF or remember web service current stats
# the state can be stored in session
state = utils.generate_new_state()
# use SDK to fetch authorized url
oauth = FangcloudOAuth2FlowBase("YOUR_CLIENT_ID", "YOUR_CLIENT_SECRET")
oauth.get_authorize_url("YOUR_REDIRECT_URL", state)
# rediret to authorized url
redirect(authorize_url)
```

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





### 使用方法

亿方云提供开放平台V1版本的API，详细说明文档请参阅[API文档](https://open.fangcloud.com/wiki/#接口列表)。



