$ = require 'jquery'
Marionette = require 'backbone.marionette'

module.exports = class FeedbackModule extends Marionette.Module
  onStart: ->
    apiKey = 'JQfSXfyNsMd9hupTfhZRyQ'
    src = "//widget.uservoice.com/#{apiKey}.js"
    $.getScript src, ->
      console.log 'configure User Voice'
      UserVoice.push ['set',
        accent_color: '#448dd6'
        trigger_color: 'white'
        trigger_background_color: '#e23a39'
      ]
      UserVoice.push ['addTrigger',
        mode: 'contact',
        trigger_position: 'bottom-right'
      ]
