# 本地
# NOTICE_LOG = 'D:\\github\\flask_project\\notice\\notice.log'
# AVATAR_PATH = 'D:\\github\\flask_project\\avatarfile\\'
# UPLOAD_AVATAR_PATH = 'D:\\github\\flask_project\\avatarfile\\'
# MUSIC_IMAGE_PATH = 'D:\\github\\flask_project\\media_image\\music\\'
# VIDEO_IMAGE_PATH = 'D:\\github\\flask_project\\media_image\\video\\'
#
# AVATAR_URL = 'http://localhost:5000/file/avatar/'
# MUSIC_IMAGE_URL = 'http://localhost:5000/file/music/'
# VIDEO_IMAGE_URL = 'http://localhost:5000/file/video/'
# ENTER_FILE_URL = 'http://localhost:5000/samb/enter_media_file/'

# 服务器
NOTICE_LOG = '/root/anjone-api/anjone-api/notice/notice.log'
AVATAR_PATH = '/root/anjone-api/anjone-api/avatarfile/'
UPLOAD_AVATAR_PATH = '/root/anjone-api/anjone-api/avatarfile/'
MUSIC_IMAGE_PATH = '/root/anjone-api/anjone-api/media_image/music/'
VIDEO_IMAGE_PATH = '/root/anjone-api/anjone-api/media_image/video/'
#
AVATAR_URL = 'http://120.78.235.195:5000/file/avatar/'
MUSIC_IMAGE_URL = 'http://120.78.235.195:5000/file/music/'
VIDEO_IMAGE_URL = 'http://120.78.235.195:5000/file/video/'
ENTER_FILE_URL = 'http://120.78.235.195:5000/samb/enter_media_file/'

# 板子
# NOTICE_LOG = '/home/firefly/project/anjone-api/anjone-api/notice/notice.log'
# AVATAR_PATH = '/home/firefly/project/anjone-api/anjone-api/avatarfile/'
# UPLOAD_AVATAR_PATH = '/home/firefly/project/anjone-api/anjone-api/avatarfile/'

# AVATAR_URL = 'http://47.98.34.218:5000/file/avatar/'

# IP_DEV = 'wlan0'
IP_DEV = 'eth0'

default_admin_name = 'admin'
root_username = 'root'
default_avatar = 'default.png'

default_samba_pwd = '123456'
# default_samba_ip = '192.168.10.24'
default_samba_ip = 'localhost'

# samba_shell = '/home/firefly/project/anjone-api/anjone-api/shell/samba_user.sh'
# samba_shell = 'D:\\github\\flask_project\\shell\\samba_user.sh'
samba_shell = '/root/anjone-api/anjone-api/shell/samba_user.sh'


class DEV_TYPE:
    WINDOWS = 'windows PC电脑'
    MAC_OS = 'mac os PC电脑'
    LINUX = 'linux PC电脑'
