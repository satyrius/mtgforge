class Forge.SearchResultsView extends Backbone.View
    el: '#main'
    template: window.MEDIA.templates['templates/search/results.jst'].render

    subscriptions:
        'cards:fetched': 'render'

    render: (data) ->
        @$el.html(@template({cards: data}))
        #@$el.find('.card').popover({
            #title: 'lol'
            #content:'lol'
            #trigger: 'hover'
            #placement: 'top'
        #})
