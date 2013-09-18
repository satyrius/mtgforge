MTG Forge is a Magic Card Database and trading platform. It has been started under Ostrovok Lab Day initiative.

## Installation (dev)

Clone git repository with project:

    git clone git@github.com:satyrius/mtgforge.git
    
Following installation is for `Mac OS X` users.
    
Backend monastery:
	
    # Gevent requires libevent library
    brew install libevent
    export CFLAGS=-I/brew/include
    # Python requirements
    pip install -r requirements.txt
	
Frontend monastery:

    brew install nodejs
    curl https://npmjs.org/install.sh | sh
	npm install -g bower
	npm install -g brunch
	cd ~/Projects/mtgforge/frontend
    npm install
    bower install
    
## Deploy (prod)

We use `Ubuntu` on production. Unless deb-packaging is ready we are deploy using `fabric`.

### Before first release

SSH to the production server and clone latest master:

	cd /var/www/
    sudo git clone git@github.com:satyrius/mtgforge.git
    
Create directories for static and media:
	
	cd /var/www/
	sudo mkdir mtgforge-static
	sudo mkdir mtgforge-media
	sudo chown www-data:www-data mtgforge-static mtgforge-media
	
Create `virtualenv` and install python packages' dependencies:

	sudo mkdir /var/virtualenv
	sudo virtualenv /var/virtualenv/mtgforge
	
	# Required for psycopg2
	sudo apt-get install postgresql-server-dev-9.3
	
	# Required for gevent
	sudo apt-get install libevent-dev
	
Install `Brunch` using npm:

	sudo add-apt-repository ppa:chris-lea/node.js
	sudo apt-get update
	sudo apt-get install nodejs
	sudo npm install -g bower
	sudo npm install -g brunch
	
### Database
	
Install postgresql on server you want, use [official instructions](https://wiki.postgresql.org/wiki/Apt) or following code:

	curl 'http://anonscm.debian.org/loggerhead/pkg-postgresql/postgresql-common/trunk/download/head:/apt.postgresql.org.s-20130224224205-px3qyst90b3xp8zj-1/apt.postgresql.org.sh' | /bin/sh
	sudo apt-get update
	sudo apt-get install postgres-9.3
	sudo apt-get install postgres-contrib-9.3
	sudo -u postgres createdb mtgforge
	
Modify postgresql access config:

	sudo vim /etc/postgresql/9.3/main/pg_hba.conf

	local   all             postgres                                trust
	host    all             postgres        127.0.0.1/32            trust
	
	sudo service postgresql restart

Do not forget to configure database connection for `Django`:

	sudo vim /var/www/mtgforge/backend/settings/local.py
	
### Fabric

You can deploy latest `master` using fabric. Change directory to your local working copy, activate virtualenv and run:

	fab deploy


## Configure

MTGForge project has several config modules for any purpose. `settings.dev` for developments, `settings.test` to run unit tests and `settings.prod` for production server. They all use default project settings from `settings.common`, but override some optins to bring something to the environment. You can pass the comfic explicitly using `DJANGO_SETTINGS_MODULE` environment variable. For example to run server with production config use following:

	DJANGO_SETTINGS_MODULE=settings.prod ./runserver.sh

But there is easy way for developers, `settings` module has a liitle magic to choose which config to use. If it founds `test` in `sys.argv` it uses `settings.test`, then it checks `sys.platform` to match *darwin* (because our developers use MacOS) and use `settings.dev` if it is, otherwise the `settings.prod` will be imorted.

Be careful on production server, pass `settings.prod` config explicitly to prevent running your app in dev mode for your real customers.

There is separate config for *mediagenerator* bundles, it is `settings.media`. This setting has beed moved to separate module to make it easier for frontand devepers to modify it and do not care about damaging `settings.common` module.

Both development and production environments usually has database settings that differs the one from `settings.common`.  There is `settings.local` module to deal with it. You can define `DATABASES` setting in this module and it will be imported to `settings.common`, otherwise default projects `DATABASES` settings will be used. For only development local settings there is `settings.dev_local` module, you can use it to switch on some specific things like *Django Debug Toolbar*. Note that `settings/*local.py` is ignored by git.

One more settings trick. You can set `DEBUG_DB` to true when `settings.dev` is used to start log database queries to the console output.

	DEBUG_DB=1 ./runserver.sh

## Data

Configure your own `DATABASES` settings:

	vim settings/local.py

Create the database:

	createdb mtgforge
    ./dj.sh syncdb
    ./dj.sh migrate

Then load fixtures and get card sets list from Gatherer:

    ./dj.sh loaddata data_provider
    ./dj.sh fetch_sets -a

To fill cards database do the following:

    # To download all (not recommended)
    ./dj.sh fetch_gatherer
    # Partial load. Get only particular set (e.g. Zendikar)
    ./dj.sh fetch_gatherer zen

Then run some postprocessing. *It is optional but adviced if you want to all go faster.*

    ./dj.sh fetch_scans
    ./dj.sh generate_thumbnails

To build full text search engine do:

    ./dj.sh build_fts_index
    ./dj.sh build_sim_index
    ./dj.sh build_suggest

## Test

We use nose with django-nose 1.1 to run unit tests, so you can reuse DB to save several seconds at the beginning and end of your test suite.

    REUSE_DB=1 ./dj.sh test

The project provides custom settings for test environment. It is strictly adviced to use `settings.test` module for tests, this module is used by default when you run `test` command. But if you want to run tests with another settings you can do it explicitly, using `DJANGO_SETTINGS_MODULE` environment variable.

    DJANGO_SETTINGS_MODULE=settings.foo ./dj.sh test

## Tools

Projects ships with useful tolls. They are to fetch MTG set names, catds info and other stuff users want to see and use. In `dry run` mode they just prints what they can get and do not save it to the database. Use `-d` or `--dry-run` just to see.

### Card Sets

We use Wizards' official product page to get all valueable product releases (aka card sets). Additionally `-a` (`--fetch-acronyms`) option can be used to parse *magiccards.info* for pretty acronyms.

    ./dj.sh fetch_sets -a

### Cards

Another major command `fetch_gatherer` loads cards details you want. It's output
depends on verbose mode `-v` (`--verbosity`): 1 is mimimal output, 2 shows
card details, 3 show card details with oracle rulings. Without argumetds it
fetches cards for all sets that database has. To limit grabber for particular
sets `-s` (`--set`) option may be used or argument to filter multiple sets.

    ./dj.sh fetch_gatherer --set=isd
    ./dj.sh fetch_gatherer isd dka avr

It is possible to update single cards, not whole set. You have to specify
card set filter in this case.

    ./dj.sh fetch_gatherer -s avr 'Avacyn, Angel of Hope' 'Sigarda, Host of Herons'

The `--no-update` option skips updating card faces already saved

    ./dj.sh fetch_gatherer -s chk --no-update

To skip card faces that cannot be found (parsed from) on card page you can pass `--skip-not-found`. This will catch *CardNotFound* exception.

    ./dj.sh fetch_gatherer -s chk --skip-not-found

### Cards post processing

#### fetch_scans

Loading cards' scans is a heavy pricess. It was introduces as separate management command.

    ./dj.sh fetch_scans

#### generate_thumbnails

It is enought to show fetched scans on SERP as is, but it would be better to use *progressive jpeg* compression to make them smaller. Use `generate_thumbnails` command to create all thumbnails we need. You can pass additional `--quality` option to set jpeg quality. This command do not update existing thumbs by default, but if you want to refresh thumbnails pass `--refresh` option.

    ./dj.sh generate_thumbnails
