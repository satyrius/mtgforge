window.Forge = {}

require 'router'

$ ->
  Forge.app = new Forge.Router()
  Backbone.history.start()
