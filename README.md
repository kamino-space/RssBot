# RSSBOT
订阅rsshub并使用coolq推送

## 使用方法
1. 编辑 config.yml
```
config:
  CQAPI: http://172.17.0.2:5700 #cqhttp地址
  REDIS_HOST: 127.0.0.1 #redis 服务器地址
  REDIS_PORT: 6379 #redis 端口
  ADMIN: 1111 #管理员QQ
  PROXY: http://10.8.0.1:8118 #代理
rsshub:
 #对应task中的platform
```
2. 编辑 tasks.json
```
{
    "title": "yande.re",  //任务名称
    "platform": "default",  //用于选择rsshub服务
    "url": "/yande.re/post/popular_recent",  //订阅地址
    "proxy": true,  //使用代理下载资源
    "translate": false,  //翻译文本
    "activate": true,  //激活状态
    "subscriber": { //订阅
        "private": [],  //个人号
        "group": []  //群组号
    }
}
```
3. 安装依赖
```
pip install feedparser redis pyyaml cqhttp
```
4. 运行
```
python run.py
```

## LICENSE
PROHIBITION OF ILLEGAL USE LICENSE