Marionette = require 'backbone.marionette'

module.exports = class ProductView extends Marionette.ItemView
  tagName: 'h4'
  template: require './templates/product'

  initialize: ->
    # TODO find a fancy way to pass app to the view
    @app = require '../../../app'

  serializeData: () ->
    data = super
    data.spoilerUri = @app.reqres.request 'spoiler:uri', data.acronym
    return data
