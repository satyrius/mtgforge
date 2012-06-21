class Forge extends Batman.App
    @root "index#index"


class Forge.Card extends Batman.Model
    @persist Batman.LocalStorage
    @encode 'name', 'cmc'
    @resourceName: "card"

    name: ''
    cmc: 0


class Forge.IndexController extends Batman.Controller
    routingKey: "index"
    index: ->
        @set "emptyCard", new Forge.Card

        Forge.Card.load (err, cards) ->
            if not cards.length
                new Forge.Card(name: "Jace", cmc: 4).save()
                new Forge.Card(name: "Ornithopter", cmc: 0).save()
                new Forge.Card(name: "Daze", cmc: 2).save()

        @render false

    create: =>
        @emptyCard.save =>
            @set 'emptyCard', new Card

$ ->
    Forge.run()
