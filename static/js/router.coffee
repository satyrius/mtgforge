class Forge.Router extends Backbone.Router
    routes:
        "" :          "index"
        "search/:q" : "search"

    index: () ->
        Forge.App.cardsView.$el.hide()
        Forge.App.indexView.$el.show()

    search: (query) ->
        Forge.App.indexView.$el.hide()
        Forge.App.cardsView.$el.show()
        Forge.App.searchView.searchModel.set "query", $.unserialize(query)
        console.log "qqq", Forge.App.searchView.searchModel.get("query")
        Forge.App.cardsView.cards.url = "api/v1/card/search/" + query
        Forge.App.cardsView.cards.fetch()
