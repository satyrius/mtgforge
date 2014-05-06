module.exports = class MainView extends Backbone.Marionette.CompositeView
  template: require './templates/main'
  itemViewContainer: '#products-list'
  itemView: require './RowView'
  emptyView: require './EmptyView'

  initialize: ->
    byYear = @collection.groupBy (cs) -> cs.year
    @collection = new Backbone.Collection (_.toArray byYear).reverse()
