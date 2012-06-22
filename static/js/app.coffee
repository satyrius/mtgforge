class Forge extends Batman.App
    Batman.ViewStore.prefix = 'static/views'
    
    @root "cards#index"
    @resources "cards"

    @set "advanced", false
    lol: () ->
        console.log "test"

class Forge.Card extends Batman.Model
    @persist Batman.LocalStorage
    @encode 'name', 'cmc'
    @resourceName: "cards"
    @storageKey: 'ads'

    name: ''
    cmc: 0


class Forge.CardsController extends Batman.Controller
    routingKey: "cards"
    cards: null
    index: ->
        Forge.Card.load (err, cards) ->
            if not cards.length
                new Forge.Card(name: "Jace", cmc: 4).save()
                new Forge.Card(name: "Ornithopter", cmc: 0).save()
                new Forge.Card(name: "Daze", cmc: 2).save()
        @set "cards", Forge.Card.get('all')

    show: (params) ->
        Forge.Card.find parseInt(params.id, 10), (err, card) ->
            console.log card.get "name"
        @set "card", Forge.Card.find parseInt(params.id, 10), (err) ->
            throw err if err

    lol: () ->
        console.log "test"

window.lol = () ->
    console.log "test"
$ ->
    Forge.run()
    $(".check-toggles").button()
