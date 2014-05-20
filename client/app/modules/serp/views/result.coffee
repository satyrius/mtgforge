Marionette = require 'backbone.marionette'

module.exports = class ResultView extends Marionette.CollectionView
  itemView: require './card'
