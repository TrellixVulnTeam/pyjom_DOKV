from bilibili_api import sync, search

BSP = search.bilibiliSearchParams()

sync(search.search(keyword="汪汪",params = {BSP.all.tids.动物圈.tid}))