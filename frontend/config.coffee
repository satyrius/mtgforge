exports.config =
  # See http://brunch.io/#documentation for docs.
  files:
    javascripts:
      joinTo: 'js/app.js'
      order: [
        'bower_components/backbone/backbone.js',
        'vendor/scripts/backbone.meta.js'
      ]
    stylesheets:
      joinTo: 'css/app.css'
    templates:
      defaultExtension: 'hbs'
      joinTo: 'js/app.js'

  framework: 'backbone'
