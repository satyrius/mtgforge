$ = require 'jquery'
Marionette = require 'backbone.marionette'

module.exports = class MainView extends Marionette.ItemView
  template: require './templates/main'

  ui:
    input: 'form input'

  events:
    'submit form': 'handleSubmit'

  handleSubmit: ->
    @trigger 'search', @ui.input.val()
    return false
