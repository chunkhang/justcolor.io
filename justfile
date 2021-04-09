alias help := list

# List available recipes
list:
	@just --list

# Install dependencies
install:
	pip3 install --upgrade pip setuptools wheel
	pip3 install --requirement requirements.txt
	pip3 install --requirement requirements.dev.txt

# Start development server
start:
	@FLASK_ENV=development flask run
