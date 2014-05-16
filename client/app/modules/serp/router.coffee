Router = require '../../lib/router'

module.exports = class SerpRouter extends Router
  appRoutes:
    'search?:params': 'listCards'
