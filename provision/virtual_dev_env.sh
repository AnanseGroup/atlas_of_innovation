#!/usr/bin/env bash

###
# Update system packages
system_update() {
  echo "Updating box software ************************************************ "
  sudo apt-get update && sudo apt-get upgrade -y
  sudo apt-get install -y tree
}

###
# Set vagrant user settings
set_user_conf() {
  echo "Setting vagrant user configuration *********************************** "
  # Generate language files
  sudo locale-gen en_US.UTF-8
  sudo update-locale LANG=en_US.UTF-8

  # Set language with env variables
  echo -e '\n# Set locale configuration' >> ~/.profile
  echo 'export LC_ALL=en_US.UTF-8' >> ~/.profile
  echo 'export LANG=en_US.UTF-8' >> ~/.profile
  echo -e 'export LANGUAGE=en_US.UTF-8\n' >> ~/.profile

  # Move to the sync folder at login
  echo -e '\n# Move to /vagrant at login' >> ~/.profile
  echo -e 'cd /vagrant\n' >> ~/.profile
}

###
# Install and configure PostgreSQL database manager
install_postgres() {
  echo "Installing PostgreSQL database manager ******************************* "
  sudo apt-get install -y postgresql postgresql-contrib

  echo "Setting up user"
  sudo -u postgres bash -c "psql -c \"CREATE USER ubuntu WITH PASSWORD 'ubuntu';\""
  sudo -u postgres bash -c "psql -c \"ALTER USER ubuntu WITH SUPERUSER;\""

  echo "Setting up extensions to all schemas"
  sudo -u postgres bash -c "psql -c \"CREATE EXTENSION unaccent SCHEMA pg_catalog;\""
  sudo -u postgres bash -c "psql -c \"CREATE EXTENSION pg_trgm SCHEMA pg_catalog;\""

  echo " Starting Postgres server "
  sudo service postgresql start
}

###
# Create database for the application
create_database() {
  echo "Creating application database **************************************** "
  sudo -u postgres bash -c "psql -c \"CREATE DATABASE atlas;\""
}

###
# Install Python dependencies
install_python_deps() {
  echo "Installing Python dependencies *************************************** "
  sudo apt-get install -y build-essential \
    python3-dev \
    python3-pip \
    libffi-dev
}

###
# Define a Python virtual environment
set_virtual_env(){
  echo "Setting Python virtual enviroment ************************************ "
  sudo -H pip3 install -U pip
  sudo -H pip3 install virtualenv virtualenvwrapper

  mkdir ~/Env

  echo -e "\n# Set environment root directory" >> ~/.profile
  echo "export WORKON_HOME=~/Env" >> ~/.profile
  echo "export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3" >> ~/.profile
  echo "export DJANGO_SETTINGS_MODULE=atlas_of_innovation.settings.development" >> ~/.profile
  echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.profile

  source ~/.profile
}

###
# Install app dependencies with pip
install_app_deps() {
  echo "Installing app pip dependencies ************************************** "
  source /usr/local/bin/virtualenvwrapper.sh
  mkvirtualenv -a /vagrant -r /vagrant/requirements.txt atlas

  echo -e "\n# Load Python environment for Atlas" >> ~/.profile
  echo "workon atlas" >> ~/.profile
}

###
# Install AWS EB CLI
install_awsebcli() {
  echo "Installing CLI for Elastic Beanstalk ********************************* "
  source /usr/local/bin/virtualenvwrapper.sh
  workon atlas
  pip install awsebcli --upgrade
}

###
# Install DirEnv env values manager
install_direnv() {
  echo "Installing DirEnv **************************************************** "
  mkdir ~/bin
  curl -sSL https://github.com/direnv/direnv/releases/download/v2.18.2/direnv.linux-amd64 > ~/bin/direnv
  chmod +x ~/bin/direnv
  echo -e "\n#Hook direnv environment switcher"  >> ~/.profile
  echo -e "eval \"\$(direnv hook bash)\"\n" >> ~/.profile
}

###
# Fetch basic environment values
fetch_env_files() {
  echo 'Fetching basic environment values ************************************ '
  curl -sSL curl -sSL https://gist.githubusercontent.com/MakerNetwork/e97b2019bc11224441a98bc9e9424ad4/raw/e1404ee40e67f393dbd450d8e46b857908aa8b81/.envrc > ~/.envrc
  sudo mv ~/.envrc /vagrant/.envrc
}

###
# Include some alias to work with Atlas
add_command_alias() {
  echo "Include alias to manage Atlas **************************************** "
  echo -e "\n# Commands to help with Atlas management"
  echo "alias atlas_run='python /vagrant/manage.py runserver 0.0.0.0:8000' " >> ~/.profile
  echo "alias atlas_db_migrate='python /vagrant/manage.py migrate'" >> ~/.profile
  echo "alias atlas_db_load='python /vagrant/manage.py loaddata governance_options ownership_options initial_database'" >> ~/.profile
  echo "alias atlas_db_prepare='/vagrant/bin/db_prepare.sh'" >> ~/.profile
  echo "alias atlas_db_reset='/vagrant/bin/db_reset.sh'" >> ~/.profile
}

###
# Remove unused and transient software
cleanup() {
  sudo apt-get -y autoremove && sudo apt-get autoclean
}

###
# Main function
setup(){
  system_update
  set_user_conf
  install_postgres
  create_database
  install_python_deps
  set_virtual_env
  install_app_deps
  install_awsebcli
  install_direnv
  add_command_alias
  cleanup
}

setup "$@"
echo "The virtual environment has been provisioned. Run 'vagrant reload'."
