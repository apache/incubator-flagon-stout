# cd /vagrant

mkdir staging
cd staging

sudo yum -y install wget
wget http://repo.continuum.io/miniconda/Miniconda-3.5.5-Linux-x86_64.sh

sh Miniconda-3.5.5-Linux-x86_64.sh -b

source ~/.bashrc
conda update conda

sudo yum -y install python-setuptools

sudo easy_install pip

sudo pip install django