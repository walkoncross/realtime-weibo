from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from scrapy import Selector
import time
import re
import os
import os.path
import requests

UID = os.getenv("UID", "5353213269")

IMAGE_DIR = "imgs/"


def get_driver():
    driver = webdriver.PhantomJS()
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
    #dcap["phantomjs.page.settings.resourceTimeout"] = ("1000")
    driver = webdriver.PhantomJS(
        service_args=['--load-images=no'], desired_capabilities=dcap)
    return driver


def get_weibo(driver, uid):
    driver.get("https://m.weibo.cn/u/" + uid)
    for i in range(100):
        if driver.page_source.find("加载中") != -1:
            time.sleep(0.1)
        else:
            break
    text = driver.page_source
    sel = Selector(text=text)
    weibos = sel.css(".card9 .weibo-media img::attr(src)").extract()
    weibos = [i for i in weibos if i.find("thumbnail") == -1]
    return weibos


def get_filename(s):
    r = re.search(r'[0-9a-zA-Z]{20,40}.*', s)
    if r:
        return r.group()
    return str(time.time()) + '.jpg'


def write_file(url):
    img = requests.get(url).content
    with open(IMAGE_DIR + get_filename(url), 'wb') as f:
        f.write(img)


def write_files(urls):
    imgs = set(os.listdir(IMAGE_DIR))
    for url in urls:
        if get_filename(url) in imgs:
            continue
        print('write file', url)
        write_file(url)


def auto_create():
    if not os.path.isdir(IMAGE_DIR):
        os.makedirs(IMAGE_DIR)


def main():
    auto_create()
    uid = UID
    driver = get_driver()
    while True:
        imgs = get_weibo(driver, uid)
        write_files(imgs)
        print('loop', time.time())
        time.sleep(3)


if __name__ == '__main__':
    while True:
        try:
            main()
        except Exception as e:
            print(e)
        time.sleep(10)
