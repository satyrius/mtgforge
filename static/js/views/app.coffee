class Forge.Views.App extends Backbone.View
    el: "#app"
    initialize: () ->
        @cardsView = new Forge.Views.Cards
        @searchView = new Forge.Views.Search
        @indexView = new Forge.Views.Index
        @router = new Forge.Router
