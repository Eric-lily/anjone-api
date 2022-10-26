sudo useradd -m -s /sbin/nologin $1
sudo chmod 777 /home/$1

sudo smbpasswd -a $1
(echo compede; echo compede) |sudo smbpasswd -a $1

echo "[$1]\n  comment=samba folder/n  path=/home/$1\n  browseable=yes\n  writable=yes\n  valid users=$1\n  avaliable=yes\n  pubilc=yes" >> /etc/samba/smb.conf

sudo service smbd restart