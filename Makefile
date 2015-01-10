default: build

install: python-env node-env

python-env:
	[ -d env ] || virtualenv env
	./env/bin/pip install -r requirements-dev.txt

node-env:
	cd client && npm install

test:
	./backend/manage.py test $(filter-out $@,$(MAKECMDGOALS))

check:
	cd ./backend && scrapy check \
		-s HTTPCACHE_ENABLED=0 \
		-s SPIDER_MODULES=crawler.tests.gatherer_check,crawler.tests.l10n_check \
		$(filter-out $@,$(MAKECMDGOALS))

run:
	ps ax | grep 'manage.py runserver' | grep -v grep |  awk '{print $$1}' | xargs kill
	# `honcho` is used to do not force developer to install `foreman`
	honcho start

build:
	docker build -t mtgforge_web .

drun:
	fig stop
	fig up -d
	docker ps

.PHONY: install test check run build drun
