_ = require 'underscore'
Marionette = require 'backbone.marionette'

module.exports = class ModalRegion extends Marionette.Region
  getEl: (selector) ->
    $el = Marionette.$ selector
    # Close region if modal element was hidden
    $el.on 'hidden.bs.modal', _.bind(@close, @)
    return $el

  onShow: (view) ->
    @$el.modal 'show'
