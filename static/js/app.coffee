window.Forge = class Forge extends Batman.App
    Batman.config.viewPrefix = '/static/views/'
    @resources 'cards', 'index', 'decks'
    @root 'index#index'
    @route '/search', 'cards#search'#, resource: 'cards', action: 'search'

$ ->
    Forge.run()
