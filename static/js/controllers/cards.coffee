class Forge.CardsController extends Batman.Controller
    routingKey: "cards"
    cards: null
    index: ->
        Forge.Card.load (err, card, robj) =>
            throw err if err
            @set "cards", robj.data.objects

    show: (params) ->
        @set "card", Forge.Card.find parseInt(params.id, 10), (err) ->
            throw err if err
