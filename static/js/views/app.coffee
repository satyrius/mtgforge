class Forge.Views.AppView extends Backbone.View
    el: "#app"
    template: MEDIA.templates["templates/app.js"]
    initialize: () ->
        @cards = new Forge.Collections.Cards
        @cards.fetch()
        @cards.bind "reset", () =>
            @render()

    render: () ->
        $(el).html(@template)
