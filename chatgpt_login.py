import logging
import os
import random
import time
import subprocess
import select

import OpenAIAuth
import yaml
from yaml.loader import FullLoader

CONFIG_PATH = 'config.yaml'

log = logging.basicConfig(level=logging.INFO,
                          format="%(asctime)s-%(name)s-%(levelname)s-%(message)s")
# 定义随机时间范围
min_time = 0.1 * 60  # 最小等待时间（分钟）
max_time = 0.5 * 60  # 最大等待时间（分钟）


# 配置文件
class Config:
    def __init__(self, email: str, password: str, proxy: str = None, wait_time: str = None):
        self.email = email
        self.password = password
        self.proxy = proxy
        self.wait_time = wait_time


# 导入配置文件
def import_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, encoding='utf-8') as f:
            config = yaml.load(f, Loader=FullLoader)
    else:
        config = {"email": os.getenv("CONFIG_EMAIL"),
                  "password": os.getenv("CONFIG_PASSWORD"),
                  "proxy": os.getenv("CONFIG_PROXY"),
                  "wait_time": os.getenv("CONFIG_WAIT_TIME")}
    if not config.get("email"):
        raise RuntimeError("please set email")
    if not config.get("password"):
        raise RuntimeError("please set password")
    if config.get("proxy") and str.strip(config["proxy"]) == "":
        config["proxy"] = None
    if config.get("wait_time") and str.strip(config["wait_time"]) == "":
        config["wait_time"] = None
    return Config(email=config.get('email'),
                  password=config.get('password'),
                  proxy=config.get('proxy'),
                  wait_time=config.get('wait_time'))


if __name__ == '__main__':
    logging.info("开始获取配置")
    config = import_config()
    openAIAuth = OpenAIAuth.Authenticator(email_address=config.email, password=config.password,
                                          proxy=config.proxy)
    error_count = 0
    # 循环执行
    while True:
        try:
            logging.info("开始获取token")
            openAIAuth.begin()
            token = openAIAuth.get_access_token()
            logging.info('token:%s' % token)
            os.environ['OPENAI_ACCESS_TOKEN'] = token
            process = subprocess.Popen(['pnpm', 'run', 'start'], cwd="/app", stdout=subprocess.PIPE)
            # 随机等待一段时间
            wait_time = config.wait_time if config.wait_time else random.randint(min_time, max_time)
            logging.info(f"等待 {wait_time} 分钟后更新token")
            start_time = time.time()
            end_time = start_time + wait_time
            while True:
                # 等待输出流可读或超时
                ready = select.select([process.stdout], [], [], 1)
                if ready[0]:
                    # 读取一行输出结果并处理
                    output = process.stdout.readline().decode('utf-8')
                    # 如果程序不再运行则跳出，重新获取token
                    if output == '' and process.poll() is not None:
                        logging.info("已关闭系统")
                        process.kill()
                        time.sleep(30)
                        break
                    if output:
                        logging.info(output.strip())
                # 超过定时时间后，关闭当前nodejs并执行下一轮
                if time.time() > end_time:
                    logging.info("关闭系统")
                    process.kill()
                    time.sleep(30)
                    break
        except Exception as e:
            logging.exception(e)
            error_count = error_count + 1
            if error_count > 5:
                break
