MTG Forge is a Magic Card Database and trading platform. It has been started under Ostrovok Lab Day initiative.

## Installation

Clone git repository with project:

    git clone git@github.com:ostrovok-team/mtgforge.git

You should intall some system requirements (Mac OS X dependent):

    # CoffeeScript (as Node.js module)
    brew install nodejs
    curl http://npmjs.org/install.sh | sh
    npm install -g coffee-script

    # SASS (as Ruby gem)
    gem install compass

    # ImageMagick for sprites
    brew install imagemagick

    # Gevent requires libevent library
    brew install libevent
    export CFLAGS=-I/brew/include

Next step is to install python packages:

    pip install -r requirements.txt

## Configure

MTGForge project has several config modules for any purpose. `settings.dev` for developments, `settings.test` to run unit tests and `settings.prod` for production server. They all use default project settings from `settings.common`, but override some optins to bring something to the environment. You can pass the comfic explicitly using `DJANGO_SETTINGS_MODULE` environment variable. For example to run server with production config use following:

	DJANGO_SETTINGS_MODULE=settings.prod ./manage.py runserver

But there is easy way for developers, `settings` module has a liitle magic to choose which config to use. If it founds `test` in `sys.argv` it uses `settings.test` otherwise `settings.dev`.

Be careful on production server, pass `settings.prod` config explicitly to prevent running your app in dev mode for your real customers.

There is separate comfig for *mediagenerator* bundles, it is `settings.media`. This setting has beed moved to separate module to make it easier for frontand devepers to modify it and do not care about damaging `settings.common` module.

Both development and production environments usually has database settings that differs the one from `settings.common`.  There is `settings.local` module to deal with it. You can define `DATABASES` setting in this module and it will be imported to `settings.common`, otherwise default projects `DATABASES` settings will be used. Note that `settings/local.py` is ignored by git.

One more settings trick. You can set `DEBUG_DB` to true when `settings.dev` is used to start log database queries to the console output.

	DEBUG_DB=1 ./manage.py runserver

## Data

Configure your own `DATABASES` settings:

	vim settings/local.py

Create the database:

	createdb mtgforge
    ./manage.py syncdb
    ./manage.py migrate

Then load fixtures and get card sets list from Gatherer:

    ./manage.py loaddata data_provider
    ./manage.py fetch_sets -a

To fill cards database do the following:

    # To download all (not recommended)
    ./manage.py fetch_gatherer
    # Partial load. Get only particular set (e.g. Zendikar)
    ./manage.py fetch_gatherer zen
    
Then run some postprocessing. *It is optional but adviced if you want to all go faster.*

    ./manage.py fetch_scans
    ./manage.py generate_thumbnails

To build full text search engine do:

    ./manage.py build_fts_index
    ./manage.py build_sim_index

## Test

We use nose with django-nose 1.1 to run unit tests, so you can reuse DB to save several seconds at the beginning and end of your test suite.

    REUSE_DB=1 ./manage.py test

The project provides custom settings for test environment. It is strictly adviced to use `settings.test` module for tests, this module is used by default when you run `test` command. But if you want to run tests with another settings you can do it explicitly, using `DJANGO_SETTINGS_MODULE` environment variable.

    DJANGO_SETTINGS_MODULE=settings.foo ./manage.py test

## Tools

Projects ships with useful tolls. They are to fetch MTG set names, catds info and other stuff users want to see and use. In `dry run` mode they just prints what they can get and do not save it to the database. Use `-d` or `--dry-run` just to see.

### Card Sets

We use Wizards' official product page to get all valueable product releases (aka card sets). Additionally `-a` (`--fetch-acronyms`) option can be used to parse *magiccards.info* for pretty acronyms.

    ./manage.py fetch_sets -a

### Cards

Another major command `fetch_gatherer` loads cards details you want. It's output
depends on verbose mode `-v` (`--verbosity`): 1 is mimimal output, 2 shows
card details, 3 show card details with oracle rulings. Without argumetds it
fetches cards for all sets that database has. To limit grabber for particular
sets `-s` (`--set`) option may be used or argument to filter multiple sets.

    ./manage.py fetch_gatherer --set=isd
    ./manage.py fetch_gatherer isd dka avr

It is possible to update single cards, not whole set. You have to specify
card set filter in this case.

    ./manage.py fetch_gatherer -s avr 'Avacyn, Angel of Hope' 'Sigarda, Host of Herons'

The `--no-update` option skips updating card faces already saved

    ./manage.py fetch_gatherer -s chk --no-update

To skip card faces that cannot be found (parsed from) on card page you can pass `--skip-not-found`. This will catch *CardNotFound* exception.

    ./manage.py fetch_gatherer -s chk --skip-not-found

### Cards post processing

#### fetch_scans

Loading cards' scans is a heavy pricess. It was introduces as separate management command.

    ./manage.py fetch_scans

#### generate_thumbnails
    
It is enought to show fetched scans on SERP as is, but it would be better to use *progressive jpeg* compression to make them smaller. Use `generate_thumbnails` command to create all thumbnails we need. You can pass additional `--quality` option to set jpeg quality. This command do not update existing thumbs by default, but if you want to refresh thumbnails pass `--refresh` option.

    ./manage.py generate_thumbnails