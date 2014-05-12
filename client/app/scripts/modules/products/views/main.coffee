module.exports = class MainView extends Backbone.Marionette.CompositeView
  template: require './templates/main'
  itemViewContainer: '#products-list'
  itemView: require './row'
  emptyView: require './empty'

  initialize: ->
    byYear = @collection.groupBy (cs) -> cs.year
    @collection = new Backbone.Collection (_.toArray byYear).reverse()
