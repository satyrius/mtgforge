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
