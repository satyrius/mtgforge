Marionette = require 'backbone.marionette'
CardSetCollection = require './collections/card_set'

API =
  getCardSets: ->
    return new CardSetCollection()

module.exports = class Entities extends Marionette.Module
  initialize: ->
    @app.reqres.setHandler 'cardset:entities', ->
      return API.getCardSets()
