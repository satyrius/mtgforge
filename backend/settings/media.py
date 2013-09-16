MEDIA_BUNDLES = (
    ( 'libs.css',
        'bootstrap/css/bootstrap.css',
        'bootstrap/css/bootstrap-responsive.css',
    ),
    ( 'common.css',
        'css/main.sass',
        #'css/ambilight.sass',
        'css/sprites.css',
        'css/chosen.css',
    ),
    ( 'libs.js',
        'js/lib/jquery.js',
        'js/lib/jquery.unserialize.js',
        #'bootstrap/js/bootstrap.js',
        'js/lib/underscore.js',
        'js/lib/backbone.js',
        'js/lib/backbone.meta.js',
        'js/lib/backbone-mediator.js',
        'js/lib/chosen.jquery.min.js',
        'js/lib/spin.min.js',
        #'js/lib/bootstrap-typeahead.custom.js',
        'js/lib/user-voice.js',
    ),
    ( 'app.js',
        #TEMPLATES
        'templates/index.jst',
        'templates/cs_links.jst',
        'templates/sidebar.jst',
        'templates/search/form.jst',
        'templates/search/results.jst',
        'templates/search/new_card.jst',
        'templates/search/new_row.jst',
        'templates/search/card_info.jst',
        'templates/search/notfound.jst',

        #INIT
        'js/init.coffee',

        #ROUTER
        'js/router.coffee',

        #MODELS
        'js/models/card.coffee',
        'js/models/set.coffee',

        #COLLECTIONS
        'js/collections/cards.coffee',
        'js/collections/sets.coffee',

        #VIEWS
        'js/views/card_info.coffee',
        'js/views/index.coffee',
        'js/views/sidebar.coffee',
        'js/views/search.coffee',
        'js/views/search_results.coffee',
        'js/views/spinner.coffee',
    ),
)