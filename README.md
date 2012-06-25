MTG Forge is a Magic Card Database and trading platform. It has been started under Ostrovok Lab Day initiative.

## Dev installation

Clone git repository with project, and configure your own `settings/local.py`:

    git clone git@github.com:ostrovok-team/mtgforge.git
    vim settings/local.py

Do not forget to install python packages:

    pip install -r requirements.txt

Standard way to setup database:

    ./manage.py syncdb
    ./manage.py migrate

Then load fixtures and get card sets list from Gatherer:

    ./manage.py loaddata data_provider
    ./manage.py fetch_sets -a

To fill cards database do the following:

    # To download all (not recommended)
    ./manage.py fetch_cards
    # Partial load. Get only particular set (e.g. Zendikar)
    ./manage.py fetch_cards zen

To build full text search engine do:
    ./manage.py build_fts_index
    ./manage.py build_sim_index

And a little bit happyness for frond-end developers. They say: "CoffeeScript is awesome!". So you have to install all stack including Node.js.

    brew install nodejs
    curl http://npmjs.org/install.sh | sh
    npm install -g coffee-script

And they like SASS too. Do not forget to include your gems binaries dir into PATH.

    gem install compass

Mediagenerator require ImageMagick.

    brew install imagemagick

## Tools

Projects ships with useful tolls. They are to fetch MTG set names, catds info and other stuff users want to see and use. In `dry run` mode they just prints what they can get and do not save it to the database. Use `-d` or `--dry-run` just to see.

### Card Sets

We use Wizards' official product page to get all valueable product releases (aka card sets). Additionally `-a` (`--fetch-acronyms`) option can be used to parse *magiccards.info* for pretty acronyms.

    ./manage.py fetch_sets -a

### Cards

Another major command `fetch_cards` loads cards details you want. It's output
depends on verbose mode `-v` (`--verbosity`): 1 is mimimal output, 2 shows
card details, 3 show card details with oracle rulings. Without argumetds it
fetches cards for all sets that database has. To limit grabber for particular
sets `-s` (`--set`) option may be used or argument to filter multiple sets.

    ./manage.py fetch_cards --set=isd
    ./manage.py fetch_cards isd dka avr

It is possible to update single cards, not whole set. You have to specify
card set filter in this case.

    ./manage.py fetch_cards -s avr 'Avacyn, Angel of Hope' 'Sigarda, Host of Herons'

The `--no-update` option skips updating card faces already saved

    ./manage.py fetch_cards -s chk --no-update

To skip card faces that cannot be found (parsed from) on card page you can pass `--skip-not-found`. This will catch *CardNotFound* exception.

    ./manage.py fetch_cards -s chk --skip-not-found

### Cards post processing

Loading cards' scans is a heavy pricess. It was introduces as separate management command.

    ./manage.py fetch_scans

MTG has a number of unordinary cards: splited, fliped and double-faced. To set right face type use next command:

    ./manage.py parse_face_type

To calculate color identity for card faces run following command:

    ./manage.py parse_colors

To fill card types table and link it with cards use command:

    ./manage.py parse_card_type
