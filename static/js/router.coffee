class Forge.Router extends Backbone.Router
    constructor: (options) ->
        super(options)
        @searchView = new Forge.SearchView()
        @sidebarView = new Forge.SidebarView()
        Backbone.Mediator.subscribe('search:q', (query) =>
            @navigate("search?#{query}", {trigger: true})
        )

    routes:
        '': 'index'
        'search?:params' : 'search'

    index: () ->
        unless @indexView?
            @indexView = new Forge.IndexView()
        @indexView.render()

    search: (query) ->
        unless @searchResultsView?
            @searchResultsView = new Forge.SearchResultsView()

        unless @cardsCollection?
            @cardsCollection = new Forge.CardsCollection()
        
        @cardsCollection.fetch({
            data: query
        }).done(() =>
            Backbone.Mediator.publish('cards:fetched', @cardsCollection.toJSON())
        )
        Backbone.Mediator.publish('search:confirm', query) 
