class Forge.CardsController extends Batman.Controller
    routingKey: 'cards'

    cards: new Batman.Set
    meta: null
    index: (params) ->
        Forge.Card.load (err) -> throw err if err


    search: (params) ->
        @setQuery params
        Forge.Card.load {q: params.q, color: params.color, type: params.type}, (err, records, env) =>
            @set "cards", records
            @set "meta", env.json.meta

    loadNext: () ->
        params = @params
        meta = @get "meta"
        Forge.Card.load {q: params.q, color: params.color, type: params.type, limit: meta.limit, offset: meta.offset + meta.limit}, (err, records, env) => 
            @set "cards", Forge.Card.get('loaded')
            @set "meta", env.json.meta
        false
    
    setQuery: (params) ->
        if @get("query.q") != params.q
            @set "query.q", params.q

        if params.color && !@get("query.color").length
            console.log("params color:", params.color, "get color:", @get "query.color") 
            #color = @get("query.color")
            #color.clear()
            @set "query.color", params.color

        if params.type
            #type = @get("query.type")
            #type.clear()
            #type.add(params.type)
            @set "query.type", params.type

    advancedToggle: (element, event, context) =>
        if @get "advancedEnabled"
            @set "advancedEnabled", false
        else
            @set "advancedEnabled", true
        false

    submitSearch: (element, event, context) =>
        Batman.redirect "/search?#{@get("serializedQuery")}"
        #false

    query: Batman({
        q: ""
        color: new Batman.Set
        type: new Batman.Set
    })

    advancedEnabled: true

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
