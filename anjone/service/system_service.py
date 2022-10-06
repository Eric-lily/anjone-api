import psutil

from anjone.common import Response
from anjone.models.vo.DiskUsageVo import DiskUsage

G = 1024 * 1024 * 1024


def get_disk_usage():
    devs = psutil.disk_partitions()
    total = 0
    free = 0
    for dev in devs:
        disk = psutil.disk_usage(dev.mountpoint)
        total += disk.total
        free += disk.free
    disk_usage = DiskUsage(round(total/G, 2), round(free/G, 2), round(free/total, 4))
    return Response.create_success(disk_usage.to_json())
