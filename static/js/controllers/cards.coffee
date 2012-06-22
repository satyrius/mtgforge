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
