_ = require 'underscore'
Marionette = require 'backbone.marionette'
ModalView = require './view'

module.exports = class ModalRegion extends Marionette.Region
  show: (view, options) ->
    # Wrap view into layout modal view and delegate 'show' call
    layout = new ModalView
    super layout
    layout.body.show view, options

  getEl: (selector) ->
    $el = Marionette.$ selector
    # Close region if modal element was hidden
    $el.on 'hidden.bs.modal', (_.bind @close, @)
    return $el

  onShow: (view) ->
    @$el.addClass 'modal'
    @$el.attr 'tabIndex', '-1'
    @$el.modal 'show'

  onClose: ->
    @$el.modal 'hide'
