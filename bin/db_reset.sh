#!/usr/bin/env bash

###
# Drops, recreates and loads the `atlas` database
reset_database() {
  sudo -u postgres bash -c "psql -c \"DROP DATABASE atlas;\""
  sudo -u postgres bash -c "psql -c \"CREATE DATABASE atlas;\""
  python /vagrant/manage.py migrate
  python /vagrant/manage.py loaddata governance_options ownership_options initial_database
}

reset_database "$@"
