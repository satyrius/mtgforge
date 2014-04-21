CardSet = require './models/CardSet'
CardSets = require './collections/CardSets'

API =
  getCardSets: ->
    sets = new CardSets()
    sets.fetch()
    return sets

module.exports = class Entities extends Marionette.Module
  initialize: ->
    @app.reqres.setHandler 'cardset:entities', ->
      return API.getCardSets()
