window.Forge = class Forge extends Batman.App
    Batman.ViewStore.prefix = 'static/views'
    
    @root "cards#index"
    @resources "cards"

    @on "ready", () ->
        console.log "Ready."

$ ->
    Forge.run()
    $(".check-toggles").button()
