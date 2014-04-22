CardSet = require './models/CardSet'
CardSets = require './collections/CardSets'

API =
  getCardSets: ->
    sets = new CardSets()
    # Return defer
    return sets.fetch()

module.exports = class Entities extends Marionette.Module
  initialize: ->
    @app.reqres.setHandler 'cardset:entities', ->
      return API.getCardSets()
