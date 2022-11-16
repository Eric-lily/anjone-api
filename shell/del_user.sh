sudo userdel -r $1 > /dev/null

# shellcheck disable=SC2115
sudo rm -rf /home/$1

sudo pdbedit -x $1
