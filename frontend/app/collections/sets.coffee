require 'models/set'

class Forge.CardSetsCollection extends Backbone.Collection
    url: "api/v1/card_sets/"
    model: Forge.CardSet

    comparator: (cs) ->
        return - new Date(cs.get "released_at")
