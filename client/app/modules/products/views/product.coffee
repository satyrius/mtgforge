Marionette = require 'backbone.marionette'

module.exports = class ProductView extends Marionette.ItemView
  tagName: 'h4'
  template: require './templates/product'

  initialize: ->
    # TODO find a fancy way to pass app to the view
    app = require '../../../app'
    @reqres = app.reqres

  serializeData: () ->
    data = super()
    data.spoilerUri = @reqres.request 'spoiler:uri', data.acronym
    return data
