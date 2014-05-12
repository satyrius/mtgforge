module.exports = class Roouter extends Marionette.AppRouter
  routes:
    '': 'index'
    'search?:params' : 'search'

  index: ->
    console.log 'its index'

  search: (query) ->
    console.log "its a search for #{query}"
