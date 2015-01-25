gpioweb
=======
sudo apt-get update

sudo apt-get install python-pip

sudo pip install flask

sudo pip install flask-bootstrap

sudo git clone https://github.com/lucamiravalle/gpioweb.git

execute server on boot:

cd

cd gpioweb

sudo chmod 755 launcher.sh

cd 

sudo mkdir logs

sudo crontab -e

paste at the end of file:

@reboot sh /home/pi/gpioweb/launcher.sh >/home/pi/logs/cronlog 2>&1

save and close

sudo reboot