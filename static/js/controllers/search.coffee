class Forge.SearchController extends Batman.Controller
    constructor: () ->
        super
        Forge.on "CardsSearch", (params) ->
            console.log("ololo event", this)
            @set("query.q", params.q)


    routingKey: ""
    advancedToggle: (element, event, context) =>
        if @get "advancedEnabled"
            @set "advancedEnabled", false
        else
            @set "advancedEnabled", true
        false

    submitSearch: (element, event, context) =>
        @redirect "/search?#{@get("serializedQuery")}"
        false

    query: Batman({
        q: ""
        color: new Batman.Set
        type: new Batman.Set
    })

    advancedEnabled: false

    @accessor "serializedQuery",
        get: () ->
            query = @get("query").toJSON()
            console.log(query, @get("query"))
            for key, param of query
                if !param.length
                    delete query[key]
            $.param(query)
        cache: false

    toggle: (element, event, context) =>
        typeAndValue = $(event.target).closest("button").attr("id").split("-toggle-")
        type = typeAndValue[0]
        value = typeAndValue[1]
        query = @get "query.#{type}"
        isEnabled = query.has(value)

        if isEnabled
            query.remove(value)
        else
            query.add(value)
