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

And a little bit happyness for frond-end developers. They say: "CoffeeScript is awesome!". So you have to install all stack including Node.js.

    brew install nodejs
    curl http://npmjs.org/install.sh | sh
    npm install -g coffee-script

And they like SASS too. Do not forget to include your gems binaries dir into PATH.

    gem install compass

## Tools

Projects ships with useful tolls. They are to fetch MTG set names, catds info and other stuff users want to see and use. In `dry run` mode they just prints what they can get and do not save it to the database. Use `-d` or `--dry-run` just to see.

### Card Sets

We use Wizards' official product page to get all valueable product releases (aka card sets). Additionally `-a` (`--fetch-acronyms`) option can be used to parse *magiccards.info* for pretty acronyms.

    ./manage.py fetch_sets -d
