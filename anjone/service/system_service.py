import psutil

from anjone.common import Response
from anjone.common.Constant import IP_DEV
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
    ip_data = get_ip(IP_DEV)
    address_data = {
        'mac': ip_data['mac'],
        'ipv4': ip_data['ipv4'],
        'ipv4_gateway': ip_data['ipv4_gateway'],
        'ipv4_dns': None,
        'ipv4_extract': None,
        'ipv6': ip_data['ipv6'],
        'ipv6_gateway': ip_data['ipv6_gateway'],
        'ipv6_dns': None,
        'ipv6_extract': None
    }
    return Response.create_success(address_data)


# 获取ipv4地址
def get_ip(adapter):
    dic = psutil.net_if_addrs()
    snicList = dic[adapter]
    mac = None
    ipv4 = None
    ipv4_mask = None
    ipv4_gateway = None
    ipv6 = None
    for snic in snicList:
        if snic.family.name in {'AF_LINK', 'AF_PACKET'}:
            mac = snic.address
        elif snic.family.name == 'AF_INET':
            ipv4 = snic.address
            ipv4_mask = snic.netmask
        elif snic.family.name == 'AF_INET6':
            ipv6 = snic.address
    if ipv4:
        index = ipv4.rfind(r'.')
        ipv4_gateway = ipv4[0:index] + '.1'
    return {
        'mac': mac,
        'ipv4': ipv4,
        'ipv4_gateway': ipv4_gateway,
        'ipv4_mask': ipv4_mask,
        'ipv6': ipv6,
        'ipv6_gateway': None,
    }
