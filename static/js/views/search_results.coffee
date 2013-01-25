class Forge.SearchResultsView extends Backbone.View
    el: '#main'
    template: window.MEDIA.templates['templates/search/results.jst'].render

    subscriptions:
        'cards:fetched': 'render'

    events:
        'click .card img' : 'showCard'

    render: (data) ->
        @$el.html(@template({cards: data}))

    showCard: (event) ->
        $(event.target).animate({
            'padding-top': '200px'
        }, 300)
