userdel -r $1 > /dev/null

# shellcheck disable=SC2115
rm -rf /home/$1

pdbedit -x $1
