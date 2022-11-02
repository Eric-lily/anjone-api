sudo useradd -m -s /sbin/nologin $1
sudo rm -rf /home/$1
# shellcheck disable=SC2115
sudo mkdir -p /home/$1
sudo mkdir -p /home/$1/我的文档
sudo mkdir -p /home/$1/我的音乐
sudo mkdir -p /home/$1/我的图片
sudo mkdir -p /home/$1/我的影视
sudo chmod 777 /home/$1
sudo chmod 777 /home/$1/我的文档
sudo chmod 777 /home/$1/我的音乐
sudo chmod 777 /home/$1/我的图片
sudo chmod 777 /home/$1/我的影视

(echo 123456; echo 123456) |sudo smbpasswd -a $1

echo -e "[$1]\n  comment=samba folder\n  path=/home/$1\n  browseable=yes\n  writable=yes\n  valid users=$1\n  avaliable=yes\n  pubilc=yes\n" >> /etc/samba/smb.conf

sudo systemctl reload smbd
