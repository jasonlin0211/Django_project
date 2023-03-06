#!/usr/bin/env bash

echo 'Start!'

sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.6 2

cd /vagrant

sudo apt-get update
sudo apt-get install tree

# install mysql8
if ! [ -e /vagrant/mysql-apt-config_0.8.24-1_all.deb ]; then
  wget -c https://dev.mysql.com/get/mysql-apt-config_0.8.24-1_all.deb
fi

sudo su -
sudo dpkg -i mysql-apt-config_0.8.24-1_all.deb
sudo DEBIAN_FRONTEND=noninteractivate
sudo apt-get install -y mysql-server
sudo apt-get install -y libmysqlclient-dev

if [ ! -f "/usr/bin/pip" ]; then
  sudo apt-get install -y python3-pip
  sudo apt-get install -y python-setuptools
  sudo ln -s /usr/bin/pip3 /usr/bin/pip
else
  echo "pip3 is installed"
fi

pip install --upgrade setuptools -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install --ignore-installed wrapt -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install -U pip -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

sudo mysql -u root << EOF
  ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'tel26338612';
  flush privileges;
  show databases;
  CREATE DATABASE IF NOT EXISTS twitter;
EOF
# fi

echo 'All Done!'