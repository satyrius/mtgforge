module.exports = class MainView extends Backbone.Marionette.CompositeView
  template: require './templates/main'
  itemViewContainer: '#products-list'
  itemView: require './RowView'
  emptyView: require './EmptyView'

  onCompositeCollectionBeforeRender: () ->
    console.log 'before render', @collection

  # Group card sets collection by year and pass splits to the row view
  showCollection: () ->
    console.log 'show collection'
    _.each (@collection.groupBy (cs) -> cs.year), (sets, year) ->
      console.log 'split for', year, sets
      view = @getItemView
        year: year
        collection: sets
      @additemView view
