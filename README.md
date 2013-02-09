MTG Forge is a Magic Card Database and trading platform. It has been started under Ostrovok Lab Day initiative.

## Dev installation

Clone git repository with project, and configure your own `settings/local.py`:

    git clone git@github.com:ostrovok-team/mtgforge.git
    vim settings/local.py

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

Standard way to setup database:

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
    # Then run some postprocessing
    ./manage.py parse_face_type
    ./manage.py parse_card_type

To build full text search engine do:

    ./manage.py build_fts_index
    ./manage.py build_sim_index

## Test

We use nose with django-nose 1.1 to run unit tests, so you can reuse DB to save several seconds at the beginning and end of your test suite.

    REUSE_DB=1 ./manage.py test

The project provides custom settings for test environment. It is strictly adviced to use `settings.test` module for tests when you run and test on the same machine.

    DJANGO_SETTINGS_MODULE=settings.test ./manage.py test

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

Loading cards' scans is a heavy pricess. It was introduces as separate management command.

    ./manage.py fetch_scans

MTG has a number of unordinary cards: splited, fliped and double-faced. To set right face type use next command:

    ./manage.py parse_face_type

To calculate color identity for card faces run following command:

    ./manage.py parse_colors

To fill card types table and link it with cards use command:

    ./manage.py parse_card_type
