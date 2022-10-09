import asyncio
import json

import websockets
from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError

from notice.notice_type.Notice import Notice


def read_log(path):
    res = []
    for line in open(path, "r", encoding='UTF-8'):
        strs = line.split(' ')
        notice = Notice(title=strs[3], create_time=strs[1]+' '+strs[2], content=strs[4], type=strs[0])
        res.append(notice.to_json())
    return res


async def notice_service(websocket, path):
    while True:
        try:
            res = read_log('notice.log')
            await websocket.send(json.dumps(res))
        except ConnectionClosedError:
            pass
        except ConnectionClosedOK:
            pass
        finally:
            await asyncio.sleep(60)


start_server = websockets.serve(notice_service, '0.0.0.0', 8081)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
