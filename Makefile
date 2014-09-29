default: install

install: python-env node-env

python-env:
	[ -d pyenv ] || virtualenv pyenv
	. pyenv/bin/activate
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

node-env:
	npm install -g brunch bower
	cd frontend && npm install && bower install

test:
	./backend/manage.py test $(filter-out $@,$(MAKECMDGOALS))

run:
	ps ax | grep 'manage.py runserver' | grep -v grep |  awk '{print $$1}' | xargs kill
	# `honcho` is used to do not force developer to install `foreman`
	honcho start

build:
	docker build -t mtgforge_web .
