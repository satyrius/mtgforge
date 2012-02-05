MTG Forge is a Magic Card Database and trading platform. It has been started under Ostrovok Lab Day initiative.

## Dev installation

Clone git repository with project, and configure your own `settings/local.py`:

    git clone git@github.com:ostrovok-team/mtgforge.git
    vim settings/local.py

Standard way to setup database:

    ./manage.py syncdb
    ./manage.py migrate

Then load fixtures and get card sets list from Gatherer:

    ./manage.py loaddata data_provider
    ./manage.py fetch_sets -a

## Tools

Projects ships with useful tolls. They are to fetch MTG set names, catds info and other stuff users want to see and use. In `dry run` mode they just prints what they can get and do not save it to the database. Use `-d` or `--dry-run` just to see.

### Card Sets

We use Wizards' official product page to get all valueable product releases (aka card sets). Additionally `-a` (`--fetch-acronyms`) option can be used to parse *magiccards.info* for pretty acronyms.

    ./manage.py fetch_sets -d
