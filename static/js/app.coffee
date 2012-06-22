window.Forge =
    Models: {}
    Collections: {}
    Views: {}

$ ->
    Forge.App = new Forge.Views.App()
    Backbone.history.start()
