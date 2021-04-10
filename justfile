alias help := list

# List available recipes
list:
	@just --list

# Bootstrap dependencies
bootstrap:
	@pipenv install
	@mkdir -p log

# Start development server
start:
	@FLASK_ENV=development pipenv run flask run

# Start production server
up:
	@supervisord --configuration supervisord.conf

# Check production server status
status:
	@supervisorctl --configuration supervisord.conf status

# Restart production server
restart:
	@supervisorctl --configuration supervisord.conf restart all

# Stop production server
down:
	@pkill -F supervisord.pid
