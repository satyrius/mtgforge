CardSet = require '../models/CardSet'

module.exports = class CardSets extends Backbone.Deferred.Collection
  url: "/api/v1/card_sets/"
  model: CardSet

  comparator: (cs) ->
    return - new Date(cs.get "released_at")
