import psutil

from anjone.common import Response
from anjone.database import db_session
from anjone.models.sqlite.DevInfo import DevInfo
from anjone.models.sqlite.VersionInfo import VersionInfo
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
    disk_usage = DiskUsage(round(total / G, 2), round(free / G, 2), round(free / total, 4))
    return Response.create_success(disk_usage.to_json())


def get_dev_info():
    # todo 从驱动层获得硬件信息
    dev_info = DevInfo.query.all()
    if len(dev_info) == 0:
        return Response.create_error('1', '设备信息暂无')
    return Response.create_success(dev_info[0].to_json())


def get_version():
    # todo 从驱动层获得版本
    version_info = VersionInfo.query.all()
    if len(version_info) == 0:
        return Response.create_error('1', '版本信息暂无')
    return Response.create_success(version_info[0].to_json())


def get_address():
    # todo 网络信息从驱动层获得
    address_data = {
        'mac': '50:E5:49:3A:EA:90',
        'ipv4': '192.168.100.107',
        'ipv4_gateway': '192.168.100.1',
        'ipv4_dns': '114.114.114.114',
        'ipv4_extract': '113.246.132.18',
        'ipv6': None,
        'ipv6_gateway': None,
        'ipv6_dns': None,
        'ipv6_extract': None
    }
    return Response.create_success(address_data)