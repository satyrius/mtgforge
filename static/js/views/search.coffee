#class Forge.Views.Search extends Backbone.View
    #el: "#app-search"
    #advancedEnabled: false
    #events:
        #"click .app-toggleAdvanced" : "toggleAdvancedEnabled"
        #"submit .form-search" : "submitSearch"
    #template: MEDIA.templates["templates/search/simple.jst"]
    #initialize: () ->
        #@searchModel = new Forge.Models.Search
        #@searchModel.bind "change", () =>
            #@render()
        #@searchModel.set "query", ""

    #render: () ->
        #@$el.html @template.render(this)
        #@advancedSearchView = new Forge.Views.AdvancedSearch
        #@advancedSearchView.searchModel = @searchModel

    #toggleAdvancedEnabled: () ->
        #if @advancedEnabled
            #@advancedEnabled = false
            #@advancedSearchView.$el.hide()
        #else
            #@advancedEnabled = true
            #@advancedSearchView.$el.show()
        #false

    #submitSearch: (event) ->
        #event.preventDefault()
        #serializedData = $(event.target).serializeArray()
        #_.each serializedData, (param, index) ->
            #if !param.value
                #serializedData.splice index, 1
            #if param.value.charAt(param.value.length - 1) == ","
                #param.value = param.value.substr(0, param.value.length - 1)
            #param.value = param.value.replace("\+", "")
        #Forge.App.router.navigate("/search/?" + $(event.target).serialize(), { trigger: true })
        #false

#class Forge.Views.AdvancedSearch extends Backbone.View
    #el: "#app-advanced-search"
    #events:
        #"click .app-mana-toggles button" : "manaToggle"
        #"click .app-cmc-toggles button" : "cmcToggle"
        #"click .app-type-toggles button" : "typeToggle"
    #template: MEDIA.templates["templates/search/advanced.jst"]
    #initialize: () ->
        #@sets = new Forge.Collections.Sets
        #@sets.bind "reset", () =>
            #@render()
        #@sets.fetch()

    #render: () ->
        #@$el.html @template.render(this)
        #$(".check-toggles").button()
        #sets = []
        #@sets.map (set) ->
            #sets.push
                #id: set.get('id')
                #name: set.get('name')
        #console.log "sets", sets
        #@$el.find("input[name='sets']").tokenInput sets, {theme: "facebook", minChars: 2, hintText: "Begin typing set name"}

    #manaToggle: (event) ->
        #input = @$el.find("input[name='color']")
        #color = $(event.target).closest("button").attr("id").replace("mana-toggle-", "")
        #isEnabled = input.val().search(color) > -1

        #if isEnabled
            #console.log "enabled", input.val(), input.val().replace(color, "")
            #input.val(input.val().replace(color, ""))
        #else
            #console.log "disabled", input.val(), input.val() + color
            #input.val(input.val() + color)

    #cmcToggle: (event) ->
        #input = @$el.find("input[name='cmc']")
        #cmc = $(event.target).closest("button").attr("id").replace("cmc-toggle-", "")
        #isEnabled = input.val().search(cmc) > -1

        #if isEnabled
            #input.val(input.val().replace(cmc, ""))
        #else
            #input.val(input.val() + cmc)

    #typeToggle: (event) ->
        #input = @$el.find("input[name='type']")
        #type = $(event.target).closest("button").attr("id").replace("type-toggle-", "")
        #isEnabled = input.val().search(type) > -1

        #if isEnabled
            #input.val(input.val().replace(type+",", ""))
        #else
            #input.val(input.val() + type + ",")
