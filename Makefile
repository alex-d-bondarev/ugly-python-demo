#.DEFAULT_GOAL := help
demo_path = ./tests/ugly/

help:
	@echo "make \t\t\t- print supported commands"
	@echo "make simulate_jenkins \t- install project"
	@echo "make install \t\t- install project"
	@echo "make try_improve_code \t- run 'black', 'isort' and 'flake8' make commands all at once"

simulate_jenkins: install try_improve_code

install:
	PIPENV_YES=true pipenv install

try_improve_code:
	PIPENV_IGNORE_VIRTUALENVS=1 pipenv run python -c'import try_improve.code as tic;tic.run_all("'$(demo_path)'")'
