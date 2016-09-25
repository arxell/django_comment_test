.PHONY: pip

rm-pyc:
	find . -name '*.pyc' -delete

virtualenv:
	virtualenv -p python3 venv3

pip:
	pip install --upgrade pip
	pip install -U pip setuptools pip-tools
	pip-compile requirements.in
	make pip-help

pip-help:
	sed -i '' '/gnureadline/d' requirements.txt # https://github.com/nvie/pip-tools/issues/333
	pip install ipdb pipdeptree

run:
	python manage.py runserver

import-data:
	python manage.py import_data

