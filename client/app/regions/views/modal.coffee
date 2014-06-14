Marionette = require 'backbone.marionette'

module.exports = class ModalView extends Marionette.Layout
  template: require './templates/modal'
  className: 'modal-dialog'

  regions:
    body: '.modal-body'
