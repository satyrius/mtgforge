$ = require 'jquery'
Backbone = require 'backbone'
Card = require '../models/card'

module.exports = class CardsCollection extends Backbone.Collection
  url: '/api/v1/cards/search'
  model: Card

  initialize: (models, options) ->
    @deferred = @fetch
      data: @makeQuery options

  makeQuery: (options) ->
    set: options.set
