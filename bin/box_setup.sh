#!/usr/bin/env bash

update() {
  echo "Updating box software"
  sudo apt-get update && sudo apt-get upgrade -y
  sudo apt-get install -y tree
}

# Language configuration
lang_conf(){
  if [[ -z "${LC_ALL}" ]]; then
    echo -e "\n# Set locale configuration" >> ~/.bashrc
    echo "export LC_ALL=en_US.UTF-8" >> ~/.bashrc
    echo "export LANG=en_US.UTF-8" >> ~/.bashrc
    echo -e "export LANGUAGE=en_US.UTF-8\n" >> ~/.bashrc
  fi
}

# Postgres installation
postgres() {

  echo "Installing PostgreSQL database manager"
  if ! command -v psql; then
    sudo apt-get update
    sudo apt-get install -y postgresql postgresql-contrib
    echo "Setting up user"
    sudo -u postgres bash -c "psql -c \"CREATE USER ubuntu WITH PASSWORD 'ubuntu';\""
    sudo -u postgres bash -c "psql -c \"ALTER USER ubuntu WITH SUPERUSER;\""

    echo "Setting up extensions to all schemas"
    sudo -u postgres bash -c "psql -c \"CREATE EXTENSION unaccent SCHEMA pg_catalog;\""
    sudo -u postgres bash -c "psql -c \"CREATE EXTENSION pg_trgm SCHEMA pg_catalog;\""

    echo "Creating atlas database"
    sudo -u postgres bash -c "psql -c \"CREATE DATABASE atlas;\""
    sudo -u postgres bash -c "psql -c \"GRANT ALL ON DATABASE atlas to ubuntu;\""
    sudo -u postgres bash -c "psql -c \"ALTER DATABASE atlas owner to ubuntu;\""

    echo " Restarting Postgres server"
    sudo service postgresql restart
  fi
}

python_deps() {
  echo "Installing Python dependencies"
  if ! command -v pip3; then
    sudo apt-get install -y python3-pip python3-dev nginx build-essential libffi-dev
  fi
}

app_deps() {
  echo "Installing app pip dependencies"
  if ! command -v virtualenv; then
    sudo -H pip3 install -U pip
    sudo -H pip3 install virtualenv virtualenvwrapper
  fi
}

set_virtual_env(){
  echo "Setting Virtual enviroment"
  if [[ ! -d ~/Env ]]; then
    mkdir ~/Env
  fi

  if ! grep -q "export WORKON_HOME=~/Env" ~/.bashrc; then

    echo -e "\n# Set environment root directory" >> ~/.bashrc
    sudo echo "export WORKON_HOME=~/Env" >> ~/.bashrc
    sudo echo "export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3" >> ~/.bashrc
    sudo echo "export DJANGO_SETTINGS_MODULE=atlas_of_innovation.settings.development" >> ~/.bashrc
    sudo echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc

    echo "Set configuration for virtual environment variables"
    source $HOME/.bashrc
    export WORKON_HOME=~/Env
    export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
    source /usr/local/bin/virtualenvwrapper.sh

    echo "Running project requirements"
    mkvirtualenv -a /vagrant -r /vagrant/requirements.txt atlas
    cd /vagrant

    echo "Set alias to run atlas"
    echo "alias run_atlas='python3 manage.py runserver 0.0.0.0:8000' " >> ~/.bashrc
    echo "alias migrate_atlas='python3 manage.py migrate'" >> ~/.bashrc
    echo "alias load_data='python3 manage.py loaddata governance_options ownership_options initial_database'" >> ~/.bashrc

    alias run_atlas='python3 manage.py runserver 0.0.0.0:8000'
    alias migrate_atlas='python3 manage.py migrate'
    alias load_data='python3 manage.py loaddata governance_options ownership_options initial_database'

    echo "Done"
 fi
}

cleanup() {
  sudo apt-get -y autoremove && sudo apt-get autoclean
}

finalized(){
  echo "cd /vagrant" >> ~/.bashrc
}

setup(){
  update
  lang_conf
  postgres
  python_deps
  app_deps
  set_virtual_env
  finalized
  cleanup
}

setup "$@"
