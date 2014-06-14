Marionette = require 'backbone.marionette'

module.exports = class ModalView extends Marionette.Layout
  template: require './template'
  className: 'modal-dialog'

  regions:
    body: '.modal-body'
