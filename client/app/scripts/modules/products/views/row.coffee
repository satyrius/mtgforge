class ProductsView extends Backbone.Marionette.CollectionView
  itemView: require './product'

module.exports = class RowView extends Backbone.Marionette.Layout
  className: 'row'
  template: require './templates/row'
  regions:
    core: '.cs-core'
    block: '.cs-block'
    duel: '.cs-duel'
    other: '.cs-other'

  initialize: (opts) ->
    # This view initialized from composite MainView and only model option
    # passed, which is actially array of CardSet models (one of grouped by
    # year subsets). This is a nested collection views workaround.
    sortedSets = _.sortBy @model.attributes, (cs) -> cs.releasedAt
    @collection = new Backbone.Collection sortedSets
    # Use a model for common collection info, such as year
    @model = new Backbone.Model
      year: @collection.first().year

  onShow: ->
    grouped = @collection.groupBy (cs) -> cs.type
    _.each grouped, (sets, type) =>
      @getRegion(type).show new ProductsView
        collection: new Backbone.Collection(sets)
