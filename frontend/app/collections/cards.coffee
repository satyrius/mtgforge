class Forge.CardsCollection extends Backbone.Collection
    url: "api/v1/cards/search"
    model: Forge.Card

    initialize: () ->
        @bind('reset', () ->
            Backbone.Mediator.publish('cardsCollection:reset')
        )

    loadNext: () ->
        oldUrl = @url
        @url = @meta.next
        @fetch({update: true, remove: false}).done( (resp, status, xhr)=>
            @url = oldUrl
            Backbone.Mediator.publish('cardsCollection:updated', resp.objects)
        )

