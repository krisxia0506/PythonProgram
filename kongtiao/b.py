import asyncio
import datetime
import json
import re

import aiohttp
import os
# from tortoise import Tortoise
# import dormitory_electricity_record
import peewee

from db import *
import random

loop = asyncio.get_event_loop()

# PROXY_IP="103.103.3.6:8080"
# PROXY_IP = "127.0.0.1:7891"

headers = {
    "Host": "h5cloud.17wanxiao.com:8080",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Wanxiao/5.6.1 CCBSDK/2.4.0",
    "Accept-Language": "en-US,en;q=0.9",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "http://h5cloud.17wanxiao.com:8080/CloudPayment/bill/selectPayProject.do?txcode=2&interurl=substituted_pay&payProId=2124&amtflag=0&payamt=0&payproname=%E8%B4%AD%E7%94%B5&img=http://cloud.17wanxiao.com:8080/CapecYunPay/images/project/img-nav_3.png&subPayProId=",

}


class wan_xiao_exception(Exception):
    pass


class q_weather_exception(Exception):
    pass


class wan_xiao:
    def __init__(self):
        self.client = aiohttp.ClientSession()

        self.OK = True

    def __del__(self):
        asyncio.run(self.client.close())

    async def getSession(self):
        async with self.client.get(
                "http://h5cloud.17wanxiao.com:8080/CloudPayment/user/pay.do?versioncode=10563102&systemType=IOS&UAinfo=wanxiao&token=488cb59c-30af-4523-8b7b-3604a4c59f1f&customerId=104",
                headers=headers) as resp:
            print(resp.status)

    async def send_get_room_request(self, op_type=0, area_id=0, build_id=0, level_id=0):
        async with self.client.get(
                r'http://h5cloud.17wanxiao.com:8080/CloudPayment/user/getRoom.do?'
                r'payProId=2124'
                r'&schoolcode=104'
                f'&optype={op_type}'
                f'&areaid={area_id}'
                f'&buildid={build_id}'
                r'&unitid=0'
                f'&levelid={level_id}'
                r'&businesstype=2', headers=headers) as resp:
            await asyncio.sleep(random.randint(100, 500) / 1000)
            if resp.status != 200:
                raise wan_xiao_exception(f'&optype={op_type}'
                                         f'&areaid={area_id}'
                                         f'&buildid={build_id}'
                                         f'获取失败！')
            text = await resp.text()
            data = await resp.json()
            if data['code'] != 'SUCCESS':
                raise wan_xiao_exception(data, "获取失败！")
            else:
                for element in data['roomlist']:
                    yield element

    async def get_area(self):
        async for area in self.send_get_room_request(op_type=1):
            yield area  # {"id":"1","name":"主分区","factorycode":null}

    async def get_build(self, area_id):
        async for area in self.send_get_room_request(op_type=2, area_id=area_id):
            print(area['name'])
            yield area  # {"id":"5","name":"八号公寓空调","factorycode":null}

    async def get_floor(self, area_id, build_id):
        async for area in self.send_get_room_request(op_type=3, area_id=area_id, build_id=build_id):
            yield area  # {"id":"10","name":"一号公寓1层","factorycode":null}

    async def get_room(self, area_id, build_id, level_id):
        async for area in self.send_get_room_request(op_type=4, area_id=area_id, build_id=build_id, level_id=level_id):
            yield area  # {"id":"1-9--10-101","name":"101","factorycode":null}

    async def get_room_power(self, room_id):
        url = f'http://h5cloud.17wanxiao.com:8080/CloudPayment/user/getRoomState.do?' \
              f'payProId=2124&schoolcode=104&businesstype=2&roomverify={room_id}'
        async with self.client.get(url, headers=headers) as resp:
            await asyncio.sleep(random.randint(1000, 3000) / 1000)
            if resp.status != 200:
                raise wan_xiao_exception(f'room_id={room_id}'
                                         f'获取失败！')
            data = await resp.json()
            if data['returnmsg'] != 'SUCCESS':
                raise wan_xiao_exception(data, "获取失败！")
            return data
            # {"returncode":"100","returnmsg":"SUCCESS","quantity":"14.40"
            # ,"quantityunit":"度","canbuy":"true","description":"101","custparams":null}

    async def fetch_row(self):
        history_file_path = f"ac_power_history/{datetime.date.today().strftime('%Y%m%d')}.json"
        history = set()
        if os.path.exists(history_file_path):
            with open(history_file_path) as f:
                for line in f:
                    history.add(line[:-1].strip())
        else:
            with open(history_file_path, 'w+') as f:
                pass
        async for area in self.get_area():
            async for build in self.get_build(area['id']):
                async for floor in self.get_floor(area['id'], build['id']):
                    async for room in self.get_room(area['id'], build['id'], floor['id']):
                        try:
                            if room['id'] in history: continue
                            try:
                                power = await self.get_room_power(room['id'])
                                yield (area, build, room, floor, power)
                                history.add(room['id'])
                                with open(history_file_path, 'a') as f:
                                    f.write(room['id'])
                                    f.write('\n')
                            except:
                                print('fetch', area, build, room,floor,'fail')
                            await asyncio.sleep(random.randint(500, 3000) / 1000)
                        except wan_xiao_exception as e:
                            self.OK = False
                            print((area, build, room, floor), e)

    def parse_room_id(self, d_num, b_num):
        match = re.search(r'([零一二三四五六七八九十]+)号.*?(\d+)', (b_num + d_num).replace('研究生楼', '九十九号'))
        bn = cn_number_to_int(match.group(1))

        key = f'{bn}-{match.group(2)}'
        if key.startswith('8-'):
            bId = 8
            s = key.split('-')[1]
            floor = ord(s[1]) - ord('0')
            area = ord(s[0]) - ord('0')
            roomId = int(s[2:])
            inBuildingId = area * 1000 + roomId
        else:
            s = key.split('-')
            bId = int(s[0])
            floor = ord(s[1][0]) - ord('0')
            roomId = int(s[1][1:])
            area = 0
            inBuildingId = area * 1000 + roomId
        return bId, floor, inBuildingId

    def room_id_to_mysql_id(self, bId, floor, inBuildingId):
        try:
            r = Rooms.select(Rooms.id, Rooms.楼内宿舍号, Rooms.楼号, Rooms.楼层).where(
                (Rooms.楼内宿舍号 == inBuildingId) & (Rooms.楼号 == bId) & (Rooms.楼层 == floor)).get()
            return r.id
        except:
            max_rid = Rooms.select(peewee.fn.max(Rooms.id)).scalar()
            Rooms.create(id=max_rid + 1, 楼内宿舍号=inBuildingId, 楼号=bId, 楼层=floor)
            return max_rid + 1
        # return (bId * 100 + floor) * 10000 + inBuildingId

    async def fetch_to_mysql(self):
        self.OK = True
        async for area, build, room, floor, power in self.fetch_row():
            bId, floor, inBuildingId = self.parse_room_id(room['name'], build['name'])
            id = self.room_id_to_mysql_id(bId, floor, inBuildingId)
            record = RoomRemainElectricity.create(宿舍=id, 当前剩余电量=float(power['quantity']),
                                                  日期=datetime.datetime.now())
            # record = RoomRemainElectricity()
            # record.宿舍 = id
            # record.当前剩余电量 = float(power['quantity'])
            # record.日期 = datetime.datetime.now()
            record.save()
            print(datetime.datetime.now().isoformat(), record)
            try:
                yesterday = RoomRemainElectricity.select(RoomRemainElectricity.当前剩余电量,RoomRemainElectricity.日期).where(
                    (RoomRemainElectricity.宿舍 == id) & (
                            RoomRemainElectricity.日期 == datetime.datetime.now() - datetime.timedelta(
                        days=1))
                ).get()
                RoomRemainUsage.create(宿舍=id,
                                       当前剩余电量=yesterday.当前剩余电量,
                                       日期=yesterday.日期,
                                       当日用电量=yesterday.当前剩余电量 - float(power['quantity']),
                                       预测值=0
                                       )
            except:
                pass

def cn_number_to_int(s: str):
    if (s == ""):
        return 0
    if (s[0] == '零'): s = s[1:]
    if (s[0] == '十'): s = "一" + s;
    t = " 一二三四五六七八九"
    if len(s) < 2:
        return t.index(s)
    else:
        if s[1] == '百':
            mul = 100
        else:
            mul = 10
        return t.index(s[0]) * mul + cn_number_to_int(s[2:])

class q_weather:
    key = '1a7f40a601254d55bc36ec9164c91dd1'
    ckey = '8aaf438168124082afb74bb8344611e9'

    def __init__(self):
        self.client = aiohttp.ClientSession()
        self.ok = False

    def __del__(self):
        asyncio.run(self.client.close())

    async def get_location_id(self):
        async with self.client.get(
                r'https://geoapi.qweather.com/v2/city/lookup/'
                r'?location=116.800636,39.951965'
                f'&key={self.key}') as resp:
            if resp.status != 200:
                raise q_weather_exception(f'location id获取失败！')
            data = await resp.json()
            if data['code'] != '200':
                raise q_weather_exception(data, f'location id获取失败！')
            else:
                return data['location'][0]['id']

    async def get_history_weather(self, date: datetime.date, location):
        if (datetime.date.today() - date) > datetime.timedelta(days=10):
            return
        async with self.client.get(r'https://datasetapi.qweather.com/v7/historical/weather'
                                   f'?location={location}'
                                   f'&date={date.strftime("%Y%m%d")}'
                                   f'&key={self.ckey}') as resp:
            if resp.status != 200:
                raise q_weather_exception(f'历史天气获取失败！')
            data = await resp.json()
            if data['code'] != '200':
                raise q_weather_exception(data, f'历史天气-{location}-获取失败！')
            else:
                return data

    async def fetch_to_file(self):
        history_file_path = f"weather_file.jsonl"
        geted = set()
        if os.path.exists(history_file_path):
            with open(history_file_path) as f:
                for l in f:
                    geted.add(l.split('###')[0])

        td = datetime.date.today()
        for x in range(-10, 0):
            target_date = td + datetime.timedelta(days=x)
            if target_date.isoformat() in geted:
                continue
            data = await self.get_history_weather(target_date, await self.get_location_id())

            with open(history_file_path, 'a') as f:
                f.write(f"{target_date.isoformat()}###{json.dumps(data, ensure_ascii=False)}\n")
            Weathers.create(日期=target_date, 湿度=data['weatherDaily']['humidity'],
                            最高温=data['weatherDaily']['tempMax'],
                            最低温=data['weatherDaily']['tempMin'], 降水量=data['weatherDaily']['precip'])
            geted.add(target_date.isoformat())
        print("天气数据获取完毕")
        self.OK = True

# async def init():
#     # Here we connect to a SQLite DB file.
#     # also specify the app name of "models"
#     # which contain models from "app.models"
#     await Tortoise.init(
#         db_url='mysql://root:@127.0.0.1:3306/test',
#         modules={'models': ['dormitory_electricity_record']}
#     )
#     # Generate the schema
#     # await Tortoise.generate_schemas()

async def fetch():
    wx = wan_xiao()
    await wx.getSession()
    qw = q_weather()
    while 1:
        try:
            await qw.fetch_to_file()
            if not qw.OK:
                continue
            await wx.fetch_to_mysql()
            if qw.OK and wx.OK:
                print(datetime.datetime.now().isoformat(), "both ok!")
                await asyncio.sleep(60 * 60 * 1)
        except Exception as e:
            print(e)
        finally:
            print(datetime.datetime.now().isoformat(), "error wait 120s!")
            await asyncio.sleep(120)

# loop.run_until_complete(init())

loop.run_until_complete(fetch())
