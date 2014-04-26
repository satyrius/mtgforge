Backbone = require 'backbone'
CardSetsCollection = require '../collections/sets'
_ = require 'underscore'
Handlebars = require 'hbsfy/runtime'
require '../helpers'

Handlebars.registerPartial 'card_sets', require '../templates/cs_links'

module.exports = class IndexView extends Backbone.View
  el: '#td-main'
  template: require '../templates/index'

  render: ->
    # Fetch card set collection or use cached
    unless @csCollection?
      @csCollection = new CardSetsCollection()
      @csCollection.fetch().done =>
        @_renderSets()
    else
      @_renderSets()

    # Reset search input and filters
    Backbone.Mediator.publish('search:reset')

  _renderSets: ->
    # Group card sets collection by year it was released, then group
    # each subset by card set type (e.g. core set, duel deck, etc.)
    grouped = @csCollection.groupBy (cs) -> cs.year
    _.each grouped, (sets, year) ->
      grouped[year] = _.groupBy sets, (cs) -> cs.type
      grouped[year]['year'] = year

    @$el.html @template(cardSets: _.sortBy(grouped, (gr) -> -gr.year))
