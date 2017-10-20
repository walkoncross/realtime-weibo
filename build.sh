VERSION=3
docker build -t registry.cn-hangzhou.aliyuncs.com/wkc/realweibo:$VERSION .
docker push registry.cn-hangzhou.aliyuncs.com/wkc/realweibo:$VERSION
