Marionette = require 'backbone.marionette'

module.exports = class ModalView extends Marionette.Layout
  template: require './template'

  regions:
    body: '.modal-body'
