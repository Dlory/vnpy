#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
下载K线数据脚本
从Jupyter notebook转换而来
"""

# 忽略各模块的警告信息
import warnings
warnings.filterwarnings("ignore")

# 加载所需使用的模块
from datetime import datetime

from vnpy.trader.datafeed import get_datafeed
from vnpy.trader.database import get_database, DB_TZ
from vnpy.trader.constant import Interval
from vnpy.trader.object import BarData, HistoryRequest
from vnpy.trader.utility import extract_vt_symbol
from vnpy.trader.setting import SETTINGS

def main():
    """主函数"""
    # 配置数据服务
    SETTINGS["datafeed.name"] = "rqdata"            # 可以根据自己的需求选择数据服务：rqdata/xt/wind等
    SETTINGS["datafeed.username"] = "license"       # RQData的用户名统一为"license"这个字符串
    SETTINGS["datafeed.password"] = "IwLPSCK0_2l4xfnvvb0ZUF4f4kGp3PgU2Snm8HpSuaCO6iYFLhCj0rZE6Gdajg5qi3mb0aROENazkirOaT6MS5AffPpSL8d-00QqYocWOCSsWXsLDGuZM-7vtbOkv0W0EFPnoAsJoJjWN-AVMD5o25YpiasZqrX_ywVvjkS2Dkg=Ca-CIKurp3fktuCGeocgdPHJCMAedVP4wZnb0-nxqENCN3Mdl-15FggJ_yuve8qbGEiBUp4fpvfjDM9jEdKKAzDtzCDDY9pCh8DyNc6ruyG5m5p_AfzgY7v-y3vVAXGDGI1G1hLOv4DT_AVogMbHfxXw-QAfEKrRx8OlhWNHios="        # 这里需要替换为你购买或者申请试用的RQData数据license

    # 配置数据库
    SETTINGS["database.name"] = "mysql"              # 可以根据自己的需求选择数据库，这里使用的是TDengine
    SETTINGS["database.database"] = "vnpy"
    SETTINGS["database.host"] = "127.0.0.1"
    SETTINGS["database.port"] = 3306
    SETTINGS["database.user"] = "root"
    SETTINGS["database.password"] = "123456"

    # 创建对象实例
    datafeed = get_datafeed()
    database = get_database()

    # 要下载数据的合约代码
    vt_symbols = [
        "jm2601.DCE",
    ]

    # 要下载数据的起止时间
    start = datetime(2025, 6, 18, tzinfo=DB_TZ)
    end = datetime(2025, 8, 6, tzinfo=DB_TZ)

    # 遍历列表执行下载
    for vt_symbol in vt_symbols:
        # 拆分合约代码和交易所
        symbol, exchange = extract_vt_symbol(vt_symbol)

        # 创建历史数据请求对象
        req: HistoryRequest = HistoryRequest(
            symbol=symbol,
            exchange=exchange,
            start=start,
            end=end,
            interval=Interval.MINUTE        # 这里下载最常用的1分钟K线
        )

        # 从数据服务下载数据
        bars: list[BarData] = datafeed.query_bar_history(req)

        # 如果下载成功则保存
        if bars:
            database.save_bar_data(bars)
            print(f"下载数据成功：{vt_symbol}，总数据量：{len(bars)}")
        # 否则失败则打印信息
        else:
            print(f"下载数据失败：{vt_symbol}")

if __name__ == "__main__":
    main() 