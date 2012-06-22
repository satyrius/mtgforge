class Forge.Views.App extends Backbone.View
    el: "#app-main"
    template: MEDIA.templates["templates/app.jst"]
    events:
        "click .app-load-next" : "loadNext"
    initialize: () ->
        @router = new Forge.Router
        @cards = new Forge.Collections.Cards
        @cards.fetch()
        
        @cards.bind "reset", () =>
            @render()

        @cards.bind "add", () =>
            console.log "add triggered"
            @render()

    render: () ->
        @$el.html @template.render(this)

    loadNext: () ->
        tmpCardsCollection = new Forge.Collections.Cards
        tmpCardsCollection.url = @cards.meta.next
        tmpCardsCollection.fetch
            success: (cards, response) =>
                if cards.length
                    @cards.add cards.toJSON()
                if response.meta
                    @cards.meta = _.clone response.meta
        false

