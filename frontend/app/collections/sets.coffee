Backbone = require 'backbone'
CardSet = require '../models/set'

module.exports = class CardSetsCollection extends Backbone.Collection
    url: "api/v1/card_sets/"
    model: CardSet

    comparator: (cs) ->
        return - new Date(cs.get "released_at")
