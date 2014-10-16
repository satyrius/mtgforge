_ = require 'underscore'
Marionette = require 'backbone.marionette'
ModalView = require './views/modal'

module.exports = class ModalRegion extends Marionette.Region
  show: (view, options) ->
    # Wrap view into layout modal view and delegate 'show' call
    if not @currentView or @currentView.isClosed
      super new ModalView
    @currentView.body.show view, options

  onShow: (view) ->
    @$el.addClass 'modal'
    @$el.attr 'tabIndex', '-1'
    @$el.modal 'show'
    @$el.on 'hidden.bs.modal', (_.bind @close, @)
    @navOn()

  onClose: ->
    @navOff()
    @$el.off 'hidden.bs.modal'
    @$el.modal 'hide'

  navOn: ->
    @$el.on 'keydown.next', (e) =>
      if e.which == 39
        @currentView.trigger 'next'
    @$el.on 'keydown.prev', (e) =>
      if e.which == 37
        @currentView.trigger 'prev'

  navOff: ->
    @$el.off 'keydown.next'
    @$el.off 'keydown.prev'
