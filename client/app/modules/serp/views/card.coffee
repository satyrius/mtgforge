Marionette = require 'backbone.marionette'

module.exports = class CardView extends Marionette.ItemView
  className: 'td-card'
  template: require './templates/card'

  initialize: ->
    # TODO find a fancy way to pass app to the view
    @app = require '../../../app'

  serializeData: () ->
    data = super
    data.uri = @app.reqres.request 'card:uri', data.id
    return data
