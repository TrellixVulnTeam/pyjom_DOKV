# https://search.bilibili.com/all?keyword=%E9%A9%AC%E5%85%8B%E6%80%9D%E4%BD%A9%E6%81%A93&from_source=webtop_search&spm_id_from=333.1007&tids=36
# 综合排序
# https://search.bilibili.com/all?keyword=%E9%A9%AC%E5%85%8B%E6%80%9D%E4%BD%A9%E6%81%A93&from_source=webtop_search&spm_id_from=333.1007&tids=36&order=click
# 最多点击
# https://search.bilibili.com/all?keyword=%E9%A9%AC%E5%85%8B%E6%80%9D%E4%BD%A9%E6%81%A93&from_source=webtop_search&spm_id_from=333.1007&tids=36&order=pubdate
# 最新发布
# https://search.bilibili.com/all?keyword=%E9%A9%AC%E5%85%8B%E6%80%9D%E4%BD%A9%E6%81%A93&from_source=webtop_search&spm_id_from=333.1007&tids=36&order=dm
# 最多弹幕
# https://search.bilibili.com/all?keyword=%E9%A9%AC%E5%85%8B%E6%80%9D%E4%BD%A9%E6%81%A93&from_source=webtop_search&spm_id_from=333.1007&tids=36&order=stow
# 最多收藏

import enum

class order(enum.Enum):
   综合排序 = None
   最多点击 = 'click'
   最新发布 = 'pubdate'
   最多弹幕 = 'dm'
   最多收藏 = 'stow'

class bilibiliSearchParams:
    def __init__
    order = order