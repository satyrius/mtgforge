class Forge.Views.App extends Backbone.View
    el: "#app-main"
    template: MEDIA.templates["templates/app.jst"]
    initialize: () ->
        @cards = new Forge.Collections.Cards
        @cards.fetch()
        @cards.bind "reset", () =>
            @render()

    render: () ->
        $(@el).html(@template.render(this))
