sudo yum install -y oracle-softwarecollection-release-el7
sudo yum -y install scl-utils rh-python38
sudo yum install git


scl enable rh-python38 bash

git --version
python -V
pip -V

pip install psycopg2