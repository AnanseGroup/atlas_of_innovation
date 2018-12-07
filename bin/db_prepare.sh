#!/usr/bin/env bash

###
# Creates and loads the `atlas` database
prepare_database() {
  python /vagrant/manage.py migrate
  python /vagrant/manage.py loaddata governance_options ownership_options initial_database
}

prepare_database "$@"
