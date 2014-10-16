_ = require 'underscore'
Backbone = require 'backbone'
Marionette = require 'backbone.marionette'

module.exports = class MainView extends Marionette.CompositeView
  template: require './templates/main'
  itemViewContainer: '#td-products'
  itemView: require './row'
  emptyView: require './empty'

  initialize: ->
    byYear = @collection.groupBy (cs) -> cs.year
    @collection = new Backbone.Collection (_.toArray byYear).reverse()
