FROM chenzhaoyu94/chatgpt-web

WORKDIR /root

ADD requirements.txt *.py ./

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories && \
    apk add --no-cache python3 python3-dev && \
    wget -O /tmp/get-pip.py https://bootstrap.pypa.io/get-pip.py && \
    python /tmp/get-pip.py && \
    pip --no-cache-dir install -r requirements.txt

EXPOSE 3002

CMD ["python","./chatgpt_login.py"]




