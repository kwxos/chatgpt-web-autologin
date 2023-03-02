# chatgpt-web-autologin
> 该项目可自动登录chatgpt并运行[chatgpt-web](https://github.com/Chanzhaoyu/chatgpt-web)项目

## 介绍
chatgpt-web项目提供了两种登录方式，一种是openAI的api接口方式，但是该方式使用的是gpt-3模型，
另一种是通过页面accessToken实现访问的，但是token仅有8小时有效性。

该项目是针对于第二种方式该项目通过[OpenAIAuth](https://github.com/acheong08/OpenAIAuth)项目实现了自动登录和刷新token

## 使用
### 直接运行
#### 环境配置
编辑`config.yaml`文件配置参数
```yaml
email: #登录邮箱
password: #密码
proxy: #代理
wait-time: #等待时间，默认不用写
```
#### 安装依赖
```shell script
# 安装依赖
pip install -r requirements.txt
```

#### 运行项目
```shell script
python ./chatgpt_login.py
```

### docker运行（推荐）
#### 配置compose
[镜像地址](https://hub.docker.com/r/superdk/chatgpt-web-autologin)
```yaml
version: '3'

services:
  app:
    image: superdk/chatgpt-web-autologin
    ports:
      - 3002:3002
    environment:
      CONFIG_EMAIL: # 登录邮箱
      CONFIG_PASSWORD: # 登录密码
      CONFIG_PROXY: # 网络代理
      CONFIG_WAIT_TIME: # 等待时间，默认为空
```


