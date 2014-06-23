_ = require 'underscore'
Marionette = require 'backbone.marionette'
ModalView = require './views/modal'

module.exports = class ModalRegion extends Marionette.Region
  show: (view, options) ->
    # Wrap view into layout modal view and delegate 'show' call
    if not @currentView or @currentView.isClosed
      super new ModalView
    @currentView.body.show view, options

  setPrev: (model) ->
    @currentView.prev.show model

  setNext: (model) ->
    @currentView.next.show model

  onShow: (view) ->
    @$el.addClass 'modal'
    @$el.attr 'tabIndex', '-1'
    @$el.modal 'show'
    @$el.on 'hidden.bs.modal', (_.bind @close, @)

  onClose: ->
    @$el.off 'hidden.bs.modal'
    @$el.modal 'hide'
