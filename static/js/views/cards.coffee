class Forge.Views.Cards extends Backbone.View
    el: "#app-cards"
    template: MEDIA.templates["templates/cards.jst"]
    events:
        "click .app-load-next" : "loadNext"
    initialize: () ->
        @cards = new Forge.Collections.Cards
        @cards.bind "reset", () =>
            @render()

        @cards.bind "add", () =>
            @render()

    render: () ->
        @$el.html @template.render(this)

    loadNext: () ->
        @$el.find(".next-cards").hide()
        @$el.find(".next-spinner").show()
        tmpCardsCollection = new Forge.Collections.Cards
        tmpCardsCollection.url = @cards.meta.next || "api/v1/card/"
        tmpCardsCollection.fetch
            success: (cards, response) =>
                if cards.length
                    @cards.add cards.toJSON()
                if response.meta
                    @cards.meta = _.clone response.meta
                @$el.find(".next-cards").show()
                @$el.find(".next-spinner").hide()

        false

