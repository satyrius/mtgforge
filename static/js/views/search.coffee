class Forge.Views.Search extends Backbone.View
    el: "#app-search"
    advancedEnabled: false
    events:
        "click .app-toggleAdvanced" : "toggleAdvancedEnabled"
        "submit .form-search" : "submitSearch"
    template: MEDIA.templates["templates/search/simple.jst"]
    initialize: () ->
        @searchModel = new Forge.Models.Search
        @searchModel.bind "change", () =>
            @render()
        @searchModel.set "query", ""

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
        event.preventDefault()
        Forge.App.router.navigate("/search/?" + $(event.target).serialize(), { trigger: true })
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
        input = @$el.find("input[name='color']")
        color = $(event.target).closest("button").attr("id").replace("mana-toggle-", "")
        isEnabled = input.val().search(color) > -1

        if isEnabled
            console.log "enabled", input.val(), input.val().replace(color, "")
            input.val(input.val().replace(color, ""))
        else
            console.log "disabled", input.val(), input.val() + color
            input.val(input.val() + color)
