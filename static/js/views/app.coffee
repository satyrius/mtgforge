class Forge.Views.App extends Backbone.View
    el: "#app-main"
    template: MEDIA.templates["templates/app.jst"]
    meta: {}
    events:
        "click .app-load-next" : "loadNext"
    initialize: () ->
        @cards = new Forge.Collections.Cards
        @cards.fetch
            success: (cards, response) =>
                if response.meta
                    @meta = response.meta
        
        @cards.bind "reset", () =>
            @render()

        @cards.bind "add", () =>
            console.log "add triggered"
            @render()

    render: () ->
        @$el.html @template.render(this)

    loadNext: () ->
        tmpCardsCollection = new Forge.Collections.Cards
        tmpCardsCollection.url = @meta.next
        tmpCardsCollection.fetch
            success: (cards, response) =>
                if cards.length
                    @cards.add cards.toJSON()
                if response.meta
                    @meta = response.meta

