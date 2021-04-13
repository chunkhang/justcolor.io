SUPERVISOR_CONFIG := "supervisord.conf"
SUPERVISORD := "supervisord --configuration " + SUPERVISOR_CONFIG
SUPERVISORCTL := "supervisorctl --configuration " + SUPERVISOR_CONFIG

alias help := list

# List available recipes
list:
	@just --list

# Bootstrap project
bootstrap:
	#!/usr/bin/env bash
	set -xeuo pipefail
	python --version
	pipenv --version
	supervisord --version
	just --version
	pipenv check
	pipenv install

# Start development server
start:
	@FLASK_ENV=development pipenv run flask run

# Start production server
up:
	@{{SUPERVISORD}}

# Check production server status
status:
	@{{SUPERVISORCTL}} status

# Restart production server
restart:
	@{{SUPERVISORCTL}} restart all

# Stop production server
down:
	#!/usr/bin/env bash
	set -euo pipefail
	PID=$({{SUPERVISORCTL}} pid)
	kill "$PID"

# Deploy to live server
deploy:
	@git push live master
