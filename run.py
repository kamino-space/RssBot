import rssbot

CQAPI = "http://172.17.0.2:5700"
REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379

if __name__ == "__main__":
    rb = rssbot.FeedWatcher()
    rb.run()