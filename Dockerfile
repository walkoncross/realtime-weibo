FROM python:3
RUN export PHANTOM_JS="phantomjs-2.1.1-linux-x86_64" && \
    wget https://npm.taobao.org/mirrors/phantomjs/$PHANTOM_JS.tar.bz2 && \
    tar xvjf $PHANTOM_JS.tar.bz2 -C /usr/local/share/ && \
    ln -s /usr/local/share/$PHANTOM_JS/bin/phantomjs /usr/local/bin/
RUN pip3 install -i https://mirrors.aliyun.com/pypi/simple requests selenium scrapy
COPY /realweibo.py /src/realweibo.py
WORKDIR /src
CMD python3 /src/realweibo.py
