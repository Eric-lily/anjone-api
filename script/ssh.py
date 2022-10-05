import paramiko


# ssh连接
import psutil as psutil


def connect(hostname, port, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostname, port=port, username=username, password=password)
    return ssh


# 关闭ssh连接
def close(ssh):
    ssh.close()


if __name__ == '__main__':
    ssh = connect('114.55.85.213', 22, 'root', 'Yr011005')
    stdin, stdout, stderr = ssh.exec_command('ls -l')
    stdin.flush()
    print(psutil.cpu_percent(interval=1, percpu=True))

    res, err = stdout.read(), stderr.read()
    result = res if res else err
    res = result.decode("utf-8")
    print(res)

    close(ssh)

