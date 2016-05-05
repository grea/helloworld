# -*- coding: utf-8 -*-

# Scrapy settings for helloworld project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'helloworld'

SPIDER_MODULES = ['helloworld.spiders']
NEWSPIDER_MODULE = 'helloworld.spiders'
#COOKIES_ENABLED=False
DOWNLOAD_DELAY = 8
DOWNLOADER_MIDDLEWARES = {
   # "helloworld.middleware.UserAgentMiddleware": 401,
    "helloworld.middleware.CookiesMiddleware": 402,
   "helloworld.misc.middleware.CustomUserAgentMiddleware": 401
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'helloworld (+http://www.yourdomain.com)'
