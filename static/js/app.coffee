class Batman.LolStorage extends Batman.RestStorage
    collectionJsonNamespace: ()->
        console.log(this, this.prototype)
        return "cards"

window.Forge = class Forge extends Batman.App
    Batman.ViewStore.prefix = 'static/views'
    
    @resources 'cards', 'index'
    @root 'index#index'
    @route '/search', 'cards#search', resource: 'cards', action: 'search'

$ ->
    Forge.run()
