Backbone = require 'backbone'
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

  navigate: (uri) ->
    Backbone.history.navigate uri, trigger: true

  onShow: ->
    @body.on 'show', (view) =>
      next = @app.request 'next:card:entity', view.model
      @off 'next'
      if next
        next.set 'uri', (@app.request 'card:uri', next.id)
        @next.show next
        @on 'next', =>
          @navigate next.get 'uri'
      else
        @next.close()

      prev = @app.request 'prev:card:entity', view.model
      @off 'prev'
      if prev
        prev.set 'uri', (@app.request 'card:uri', prev.id)
        @prev.show prev
        @on 'prev', =>
          @navigate prev.get 'uri'
      else
        @prev.close()

  onClose: ->
    @app.execute 'last:search:navigate'
