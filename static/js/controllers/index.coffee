class Forge.IndexController extends Batman.Controller
    routingKey: 'index'
    index: (params) ->
        console.log "render index#index"
        @render()
