class Forge.IndexView extends Backbone.View
    el: "#td-main"
    template: window.MEDIA.templates['templates/index.jst'].render
    events:
        "click .card-set" : "handleCardSetClick"

    render: () ->
        unless @csCollection?
            @csCollection = new Forge.CardSetsCollection()
            @csCollection.fetch().done () =>
                @_renderSets()
        else
            @_renderSets()

    _renderSets: () ->
        @$el.html(@template({card_sets: @csCollection.toJSON()}))

    handleCardSetClick: (event) ->
        _.defer(@_handleCardSetClick, event)

    _handleCardSetClick: (event) ->
        cs_acronym  = $(event.target).data("acronym")
        Backbone.Mediator.publish("search:q", {set: cs_acronym})
