Backbone = require 'backbone'

module.exports = class BaseView extends Backbone.View
	initialize: (options) ->
		@app = options.app if options?.app?
