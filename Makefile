#.DEFAULT_GOAL := help

help:
	@echo "make \t\t\t- print supported commands"
	@echo "make black \t\t- run python black to improve code style."
	@echo "make isort \t\t- run python isort to improve code style."
	@echo "make flake8 \t\t- run python flake8 to show code warnings that cannot be fixed automatically."
	@echo "make code_style \t- run 'black', 'isort' and 'flake8' make commands all at once"

code_style: black isort flake8

black:
	PIPENV_IGNORE_VIRTUALENVS=1 pipenv run black .

isort:
	PIPENV_IGNORE_VIRTUALENVS=1 pipenv run isort .

flake8:
	PIPENV_IGNORE_VIRTUALENVS=1 pipenv run flake8 .
