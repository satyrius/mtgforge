class Forge.Views.Search extends Backbone.View
    el: "#app-search"
    advancedEnabled: false
    events:
        "click .app-toggleAdvanced" : "toggleAdvancedEnabled"
        "submit .form-search" : "submitSearch"
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

    submitSearch: (event) ->
        Forge.App.router.navigate("/search/?" + $(event.target).serialize())
        #Forge.App.cards.url = "api/v1/card/search/?" + $(event.target).serialize()
        #Forge.App.cards.reset()
        #Forge.App.cards.fetch()
        console.log "from search cards url:", Forge.App.cards.url, "meta", Forge.App.cards.meta
        false

class Forge.Views.AdvancedSearch extends Backbone.View
    el: "#app-advanced-search"
    events:
        "click .app-mana-toggles button" : "manaToggle"
    template: MEDIA.templates["templates/search/advanced.jst"]
    initialize: () ->
        @render()

    render: () ->
        @$el.html @template.render(this)
        $(".check-toggles").button()

    manaToggle: (event) ->
        input = $(event.target).closest("button").find("input")
        oldValue = parseInt input.val(), 10
        console.log "click",  input, oldValue

        if oldValue
            input.val(0)
        else
            console.log "turn on"
            input.val(1)