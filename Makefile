#.DEFAULT_GOAL := help
demo_path = ./tests/ugly/

help:
	@echo "make \t\t\t- print supported commands"
	@echo "make simulate_jenkins \t- install project"
	@echo "make install \t\t- install project"
	@echo "make black \t\t- run python black to improve code style."
	@echo "make isort \t\t- run python isort to improve code style."
	@echo "make flake8 \t\t- run python flake8 to show code warnings that cannot be fixed automatically."
	@echo "make code_style \t- run 'black', 'isort' and 'flake8' make commands all at once"

simulate_jenkins: install code_style

install:
	PIPENV_YES=true pipenv install

code_style: clean_before_analysis black isort flake8 maintainability_index execute_project_gorilla

clean_before_analysis:
	PIPENV_IGNORE_VIRTUALENVS=1 pipenv run python -c'import project_gorilla; project_gorilla.clean_before_test()'

execute_project_gorilla:
	PIPENV_IGNORE_VIRTUALENVS=1 pipenv run python -c'import project_gorilla; project_gorilla.check_quality()'

black:
	 PIPENV_IGNORE_VIRTUALENVS=1 pipenv run black $(demo_path)

isort:
	PIPENV_IGNORE_VIRTUALENVS=1 pipenv run isort $(demo_path)

flake8:
	PIPENV_IGNORE_VIRTUALENVS=1 pipenv run flake8 $(demo_path) --output-file=flake8.log --exit-zero

maintainability_index:
	PIPENV_IGNORE_VIRTUALENVS=1 pipenv run radon mi $(demo_path) --json --output-file=radon.log
