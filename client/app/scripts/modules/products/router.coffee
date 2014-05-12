module.exports = class Router extends Marionette.AppRouter
  appRoutes:
    '': 'listProducts'

  routes:
    'search?:params' : 'search'

  search: (query) ->
    console.log "its a search for #{query}"
