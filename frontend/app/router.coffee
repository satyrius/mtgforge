require 'views'

class Forge.Router extends Backbone.Router
    constructor: (options) ->
        super(options)
        @searchView = new Forge.SearchView()
        @sidebarView = new Forge.SidebarView()
        Backbone.Mediator.subscribe('search:q', (query) =>
            query = $.unserialize(query) if typeof query == 'string'
            q = _.extend(@query, query);
            @navigate("search?#{$.serialize(q, true)}", {trigger: true})
        )

    query: {}

    routes:
        '': 'index'
        'search?:params' : 'search'

    index: () ->
        unless @indexView?
            @indexView = new Forge.IndexView()
        @indexView.render()

    search: (query) ->
        query = query
        unless @searchResultsView?
            @searchResultsView = new Forge.SearchResultsView()

        unless @spinnerView?
            @spinnerView = new Forge.SpinnerView()

        unless @cardsCollection?
            @cardsCollection = new Forge.CardsCollection()

        Backbone.Mediator.publish('cards:loading')
        @cardsCollection.fetch({
            data: query
        }).done(() =>
            Backbone.Mediator.publish('cards:fetched', @cardsCollection)
        )
        Backbone.Mediator.publish('search:confirm', query)
