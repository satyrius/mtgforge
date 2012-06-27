window.Forge = class Forge extends Batman.App
    Batman.ViewStore.prefix = 'static/views'
    
    #Batman.config =
        #pathPrefix: "/"
        #usePushState: true
    @resources 'cards', 'index'
    @root 'index#index'
    @route '/search', 'cards#search'#, resource: 'cards', action: 'search'

$ ->
    Forge.run()
