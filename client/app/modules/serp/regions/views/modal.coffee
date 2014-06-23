Marionette = require 'backbone.marionette'
ModelNavRegion = require '../nav'

module.exports = class ModalView extends Marionette.Layout
  template: require './templates/modal'
  className: 'modal-dialog'

  regions:
    body: '.modal-body'
    prev:
      selector: '#td-nav-prev'
      regionType: ModelNavRegion
      template: require './templates/prev'
    next:
      selector: '#td-nav-next'
      regionType: ModelNavRegion
      template: require './templates/next'

  initialize: ->
    # TODO find a better way to access app instance
    @app = require '../../../../app'

  onShow: ->
    @body.on 'show', (view) =>
      next = @app.request 'next:card:entity', view.model
      if next
        next.set 'uri', (@app.request 'card:uri', next.id)
        @next.show next
      prev = @app.request 'prev:card:entity', view.model
      if prev
        prev.set 'uri', (@app.request 'card:uri', prev.id)
        @prev.show prev

  onClose: ->
    @app.execute 'last:search:navigate'
