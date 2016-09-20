# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
	config.vm.define "virtualbox" do |vbox|
		vbox.vm.box = "centos_6.5"
		vbox.vm.network "forwarded_port", guest: 80, host: 8080
		vbox.vm.network "forwarded_port", guest: 8000, host: 9000

		vbox.vm.provision :shell, path: "scripts/install.sh"
		vbox.vm.provision :shell, path: "scripts/install_python.sh"
		vbox.vm.provision :shell, path: "scripts/start_oe.sh"
	end

	config.vm.define "openstack", autostart: false do |osConfig|
		require 'vagrant-openstack-plugin'

		osConfig.ssh.private_key_path = "/Users/dreed/draper/xdata/code/logging_server/vagrant/user-ale-logger-vagrant.cer"

		osConfig.vm.box = "dummy"
		osConfig.vm.box_url = "https://github.com/cloudbau/vagrant-openstack-plugin/raw/master/dummy.box"

		osConfig.vm.provider :openstack do |os|
			os.username     = "#{ENV['OS_USERNAME']}"
			os.api_key      = "#{ENV['OS_PASSWORD']}"
			os.flavor       = /m1.small/                # Regex or String
			os.image        = /xdata-centos-base/                 # Regex or String
			os.endpoint     = "#{ENV['OS_AUTH_URL']}/tokens"
			os.keypair_name = "User-ALE-logger-vagrant"      # as stored in Nova
			os.ssh_username = "cloud-user"           # login for the VM
			os.floating_ip = "10.1.93.171"
			os.networks = []
			os.server_name = "oe_vagrant_test"
		end

		osConfig.ssh.pty = true

		config.vm.provision :shell, path: "scripts/install.sh"
		config.vm.provision :shell, path: "scripts/setup_iptables.sh"
		config.vm.provision :shell, path: "scripts/install_python.sh"
		config.vm.provision :shell, path: "scripts/start_oe.sh"
	end

	config.vm.define "aws", autostart: false do |aws|   #install on ubuntu image
		require 'vagrant-aws'

		aws.vm.box = "dummy"
		aws.vm.box_url = "https://github.com/mitchellh/vagrant-aws/raw/master/dummy.box"

		aws.ssh.username = "ubuntu"
		aws.ssh.private_key_path = "PATH_TO_YOUR_KEY_FILE.pem"

		aws.vm.provider :aws do |ec2, override|
			ec2.access_key_id = "YOUR_ACCESS_KEY"
			ec2.secret_access_key = "YOUR_SECRET"
			ec2.keypair_name = "KEYPAIR_NAME"
			ec2.instance_type = "m1.medium"
			ec2.region = "us-east-1"
			ec2.security_groups = ["neon-vagrant"]
			ec2.tags = {
			'project' => 'neon'
			}
			ec2.block_device_mapping = [{ :DeviceName => "/dev/sda1", 'Ebs.VolumeSize' => 20, 'Ebs.DeleteOnTermination' => true }]
			ec2.ami = "ami-d805f4b0" #"ami-018c9568" #the ami for the image to install
			override.ssh.pty = true
		end

		aws.vm.synced_folder ".", "/vagrant", disabled: true

		aws.vm.synced_folder "./puppet/", "/puppet"

		aws.vm.provision "shell",
		inline: "echo \"Applying puppet\" &&  puppet apply /puppet/ubuntu.pp"

		aws.vm.network "forwarded_port", host: 4567, guest: 8080
	end
end