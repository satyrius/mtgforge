CardSet = require '../models/card_set'

module.exports = class CardSetCollection extends Backbone.Deferred.Collection
  url: "/api/v1/card_sets/"
  model: CardSet

  comparator: (cs) ->
    return - new Date(cs.get "released_at")
