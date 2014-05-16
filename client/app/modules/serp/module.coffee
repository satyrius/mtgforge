BaseModule = require '../base'

module.exports = class SerpModule extends BaseModule
  Controller: require './controller'
  Router: require './router'
