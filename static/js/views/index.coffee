class Forge.IndexView extends Backbone.View
    el: "#td-main"
    template: window.MEDIA.templates['templates/index.jst'].render

    render: () ->
        unless @csCollection?
            @csCollection = new Forge.CardSetsCollection()
            @csCollection.fetch().done () =>
                @_renderSets()
        else
            @_renderSets()

    _renderSets: () ->
        @$el.html(@template({card_sets: @csCollection.groupBy "year"}))
