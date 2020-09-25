
apt-get -y update

apt-get install -y libhdf5-serial-dev hdf5-tools libhdf5-dev zlib1g-dev zip libjpeg8-dev liblapack-dev libblas-dev libpq-dev gfortran
cd /opt/lpr/darknet/
make clean
make all

cd
apt-get install -y python3-pip
apt-get install -y wget
wget https://developer.download.nvidia.com/compute/redist/jp/v43/tensorflow/tensorflow-1.15.2+nv20.3-cp36-cp36m-linux_aarch64.whl
pip3 install cython
pip3 install flask
pip3 install tensorflow-1.15.2+nv20.3-cp36-cp36m-linux_aarch64.whl
pip3 install keras==2.3.1
