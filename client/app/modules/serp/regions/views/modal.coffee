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
      @showRelated view.model, 'next'
      @showRelated view.model, 'prev'

  showRelated: (current, wanted) ->
    event = regionName = wanted
    # NOTE `wanted` should be a string (e.g. next, prev)
    deferred = @app.request "#{wanted}:card:entity", current
    region = @getRegion regionName
    @off event
    deferred.done (model) =>
      if not model
        region.close()
        return
      model.set 'uri', (@app.request 'card:uri', model.id)
      region.show model
      @on event, =>
        @navigate model.get 'uri'

  onClose: ->
    @app.execute 'last:search:navigate'
