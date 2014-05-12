CardSetCollection = require './collections/card_set'

API =
  getCardSets: ->
    sets = new CardSetCollection()
    # Return defer
    return sets.fetch()

module.exports = class Entities extends Marionette.Module
  initialize: ->
    @app.reqres.setHandler 'cardset:entities', ->
      return API.getCardSets()
