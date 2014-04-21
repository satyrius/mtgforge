module.exports = class RowView extends Backbone.Marionette.CompositeView
  template: require './templates/row'
  itemViewContainer: '.col-products'
  itemView: require './ProductView'

  initialize: (opts) ->
    @year = opts.year
    @collection = opts.collection
