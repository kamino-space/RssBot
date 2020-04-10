from .bot import QQBot
from .config import Config
from .rss import FeedWatcher
from .tool import Tool

import logging
logging.basicConfig(level=logging.DEBUG,
                    format="[%(levelname)s] [%(asctime)s] %(message)s",
                    datefmt='%Y-%m-%d %H:%M:%S'
                    )
