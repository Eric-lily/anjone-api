import asyncio
import json
import queue

import psutil
import websockets
from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK

cpu_queue = queue.Queue(maxsize=14)
men_queue = queue.Queue(maxsize=14)
recv_q = queue.Queue(maxsize=14)
send_q = queue.Queue(maxsize=14)


# cpu使用率 长度为14的时间序列数组
async def cpu_usage():
	global cpu_queue
	while True:
		if cpu_queue.full():
			cpu_queue.get()
		cpu = psutil.cpu_percent(1)
		cpu_queue.put(cpu)
		await asyncio.sleep(3)


# 内存使用率，长度为14的时间序列数组
async def men_usage():
	global men_queue
	while True:
		if men_queue.full():
			men_queue.get()
		mem = psutil.virtual_memory()
		men_queue.put(mem[2])
		await asyncio.sleep(3)


# 测网速
async def net_io():
	global recv_q
	global send_q
	net = psutil.net_io_counters()
	before_recv = net.bytes_recv
	before_send = net.bytes_sent
	while True:
		if recv_q.full():
			recv_q.get()
			send_q.get()
		net = psutil.net_io_counters()
		delta_recv = (net.bytes_recv - before_recv)
		delta_send = (net.bytes_sent - before_send)
		before_recv = net.bytes_recv
		before_send = net.bytes_sent
		recv_q.put(delta_recv)
		send_q.put(delta_send)
		await asyncio.sleep(3)


async def system_data(websocket, path):
	while True:
		q1 = list(cpu_queue.queue)
		q2 = list(men_queue.queue)
		q3 = list(recv_q.queue)
		q4 = list(send_q.queue)
		result = {
			'cpu_q': q1,
			'men_q': q2,
			'recv_q': q3,
			'send_q': q4
		}
		try:
			await websocket.send(json.dumps(result))
		except ConnectionClosedError:
			pass
		except ConnectionClosedOK:
			pass
		finally:
			await asyncio.sleep(3)


start_server = websockets.serve(system_data, '0.0.0.0', 8080)

tasks = [
	cpu_usage(), men_usage(), net_io(), start_server
]

asyncio.get_event_loop().run_until_complete(asyncio.wait(tasks))
asyncio.get_event_loop().run_forever()
