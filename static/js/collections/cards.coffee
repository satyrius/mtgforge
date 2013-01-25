class Forge.CardsCollection extends Backbone.Collection
    url: "api/v1/cards/search"
    model: Forge.Card
    initialize: () ->
        @bind('reset', () ->
            Backbone.Mediator.publish('cardsCollection:reset')
        )
