# -*- coding:utf-8 -*-
__Author__ = "KrianJ wj_19"
__Time__ = "2020/8/21 9:47"
__doc__ = """ 运行/调试项目"""

from scrapy import cmdline

if __name__ == '__main__':
    # cmdline.execute(['scrapy', 'crawl', 'live_info'])
    cmdline.execute(['scrapy', 'crawl', 'channel'])
