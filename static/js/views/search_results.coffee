class Forge.SearchResultsView extends Backbone.View
    el: '#main'
    template: window.MEDIA.templates['templates/search/results.jst'].render

    subscriptions:
        'cards:fetched': 'render'
        'cardsCollection:updated': 'render'

    render: (data) ->
        @$el.html(@template({cards: data}))

