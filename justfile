alias help := list

# List available recipes
list:
	@just --list

# Install dependencies
install:
	@pipenv install

# Start development server
start:
	@FLASK_ENV=development pipenv run flask run
