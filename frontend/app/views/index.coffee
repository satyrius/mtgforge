class Forge.IndexView extends Backbone.View
    el: "#td-main"
    template: window.MEDIA.templates['templates/index.jst'].render
    csListTemplate: window.MEDIA.templates['templates/cs_links.jst'].render

    render: () ->
        # Fetch card set collection or use cached
        unless @csCollection?
            @csCollection = new Forge.CardSetsCollection()
            @csCollection.fetch().done () =>
                @_renderSets()
        else
            @_renderSets()

        # Reset search input and filters
        Backbone.Mediator.publish('search:reset')

    _renderSets: () ->
        # Group card sets collection by year it was released, then group
        # each subset by card set type (e.g. core set, duel deck, etc.)
        grouped = @csCollection.groupBy (cs) -> cs.year
        _.each grouped, (sets, year) ->
            grouped[year] = _.groupBy sets, (cs) ->
                cs.type

        @$el.html(@template({
            cardSets: grouped,
            listTemplate: @csListTemplate
        }))
