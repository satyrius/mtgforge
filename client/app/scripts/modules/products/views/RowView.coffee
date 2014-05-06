module.exports = class RowView extends Backbone.Marionette.CompositeView
  template: require './templates/row'
  itemViewContainer: '.col-products'
  itemView: require './ProductView'

  initialize: (opts) ->
    @collection = new Backbone.Collection (_.toArray @model.attributes)
    @model = new Backbone.Model
      year: @collection.first().year
