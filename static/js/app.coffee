window.Forge =
    Models: {}
    Collections: {}
    Views: {}

$ ->
    Forge.App = new Forge.Views.AppView
    $(".check-toggles").button()
