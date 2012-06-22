class Forge.Views.Search extends Backbone.View
    el: "#app-search"
    advancedEnabled: false
    events:
        "click .app-toggleAdvanced" : "toggleAdvancedEnabled"
    template: MEDIA.templates["templates/search/simple.jst"]
    initialize: () ->
        @render()

    render: () ->
        @$el.html @template.render(this)
        @advancedSearchView = new Forge.Views.AdvancedSearch

    toggleAdvancedEnabled: () ->
        if @advancedEnabled
            @advancedEnabled = false
            @advancedSearchView.$el.hide()
        else
            @advancedEnabled = true
            @advancedSearchView.$el.show()
        false

class Forge.Views.AdvancedSearch extends Backbone.View
    el: "#app-advanced-search"
    template: MEDIA.templates["templates/search/advanced.jst"]
    initialize: () ->
        @render()

    render: () ->
        @$el.html @template.render(this)
        $(".check-toggles").button()
