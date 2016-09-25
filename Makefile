.PHONY: pip

pip:
	pip install -U pip setuptools pip-tools
	pip-compile requirements.in
	make pip-help


rm-pyc:
	find . -name '*.pyc' -delete


pip-help:
	sed -i '' '/gnureadline/d' requirements.txt # https://github.com/nvie/pip-tools/issues/333
	pip install ipdb pipdeptree

run:
	python manage.py runserver

import-data:
	python manage.py import_data
