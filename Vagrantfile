# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure(2) do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://atlas.hashicorp.com/search.
  config.vm.box = "centos/7"
  config.vm.hostname = "kadbox"
  #config.vm.provision "shell", path: ""
  config.vm.define "kadbox" do |kadbox|
  end

  # Disable automatic box update checking. If you disable this, then
  # boxes will only be checked for updates when the user runs
  # `vagrant box outdated`. This is not recommended.
  # config.vm.box_check_update = false

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  #config.vm.network "forwarded_port", guest: 80, host: 8080
  config.vm.network "forwarded_port", guest: 3306, host: 33066

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  config.vm.network "private_network", ip: "192.168.33.10"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # config.vm.network "public_network"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  # config.vm.synced_folder "../data", "/vagrant_data"

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
  # config.vm.provider "virtualbox" do |vb|
  #   # Display the VirtualBox GUI when booting the machine
  #   vb.gui = true
  #
  #   # Customize the amount of memory on the VM:
  #   vb.memory = "1024"
  # end
  #
  # View the documentation for the provider you are using for more
  # information on available options.

  # Define a Vagrant Push strategy for pushing to Atlas. Other push strategies
  # such as FTP and Heroku are also available. See the documentation at
  # https://docs.vagrantup.com/v2/push/atlas.html for more information.
  # config.push.define "atlas" do |push|
  #   push.app = "YOUR_ATLAS_USERNAME/YOUR_APPLICATION_NAME"
  # end

  # Enable provisioning with a shell script. Additional provisioners such as
  # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
  # documentation for more information about their specific syntax and use.
  # config.vm.provision "file", source: "common.sql", destination: "common.sql"
  config.vm.provision "shell", inline: <<-SHELL
    sudo yum install -y wget
    wget https://dev.mysql.com/get/mysql57-community-release-el7-8.noarch.rpm
    sudo yum install -y mysql57-community-release-el7-8.noarch.rpm
    sudo yum -y update
    sudo yum -y install mysql-server
    sudo systemctl start mysqld
    sudo systemctl enable mysqld
    MYSQL_TEMP_PWD=`sudo cat /var/log/mysqld.log | grep 'A temporary password is generated' | awk -F'root@localhost: ' '{print $2}'`
    mysqladmin -u root -p`echo $MYSQL_TEMP_PWD` password 'Passw0rd!'
    sudo mysql -uroot -pPassw0rd! -e "CREATE DATABASE IF NOT EXISTS mpg;"
    sudo mysql -uroot -pPassw0rd! -D mpg -e "CREATE TABLE IF NOT EXISTS contacts (contact_id int(11) NOT NULL AUTO_INCREMENT,contact_name varchar(50) DEFAULT NULL,contact_age int(3) DEFAULT NULL,contact_dob date DEFAULT NULL,PRIMARY KEY (contact_id)) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;"
    sudo mysql -uroot -pPassw0rd! -e "GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'Passw0rd!' WITH GRANT OPTION;"
    sudo mysql -uroot -pPassw0rd! -e "FLUSH PRIVILEGES;"
    sudo systemctl restart mysqld
  SHELL
end
