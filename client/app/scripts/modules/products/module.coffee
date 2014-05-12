BaseModule = require '../base'

module.exports = class ProductsModule extends BaseModule
  Controller: require './controller'
  Router: require './router'
