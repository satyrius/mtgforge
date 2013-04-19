MEDIA_BUNDLES = (
    ( 'libs.css',
        'bootstrap/css/bootstrap.css',
        'bootstrap/css/bootstrap-responsive.css',
    ),
    ( 'common.css',
        'css/normalize.css',
        'css/main.sass',
        'css/ambilight.sass',
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
        #'js/lib/bootstrap-typeahead.custom.js',
    ),
    ( 'app.js',
        #TEMPLATES
        'templates/index.jst',
        'templates/sidebar.jst',
        'templates/search/form.jst',
        'templates/search/results.jst',
        'templates/search/new_card.jst',
        'templates/search/new_row.jst',
        'templates/search/card_info.jst',
 
        #INIT
        'js/init.coffee',

        #ROUTER
        'js/router.coffee',

        #MODELS
        'js/models/card.coffee',

        #COLLECTIONS
        'js/collections/cards.coffee',

        #VIEWS
        'js/views/index.coffee',
        'js/views/sidebar.coffee',
        'js/views/search.coffee',
        'js/views/search_results.coffee',
    ),
)
