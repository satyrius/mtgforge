var gulp = require('gulp');
var jade = require('gulp-jade');
var livereload = require('gulp-livereload');
var plumber = require('gulp-plumber');
var stylus = require('gulp-stylus');
var browserify = require('gulp-browserify');
var concat = require('gulp-concat');
var uglify = require('gulp-uglify');
var minify = require('gulp-minify-css');

var environment = 'dev';
var paths = {
  src: './app/',
  dest: './public/',
  vendor: './vendor/',
  assets: './assets/'
}

gulp.task('set-prod', function() {
  environment = 'prod';
});

gulp.task('assets', function() {
 gulp.src(paths.assets + '**')
    .pipe(plumber())
    .pipe(gulp.dest(paths.dest));
});

gulp.task('vendor-styles', function() {
  stream = gulp.src([
      paths.vendor + 'styles/bootstrap.css',
      paths.vendor + 'styles/bootstrap-theme.css'
    ])
    .pipe(plumber())
    .pipe(concat('vendor.css'))

  if (environment == 'prod') {
    stream.pipe(minify())
  }

  stream.pipe(gulp.dest(paths.dest + 'css/'))
});

gulp.task('vendor-scripts', function() {
  stream = gulp.src([
      paths.vendor + 'scripts/jquery.js',
      paths.vendor + 'scripts/bootstrap.js',
      paths.vendor + 'scripts/underscore.js',
      paths.vendor + 'scripts/backbone.js',
      paths.vendor + 'scripts/backbone.defered.jquery.js',
      paths.vendor + 'scripts/backbone.syphon.js',
      paths.vendor + 'scripts/backbone.marionette.js',
      paths.vendor + 'scripts/backbone.tastypie.js'
    ])
    .pipe(plumber())
    .pipe(concat("vendor.js"))

  if (environment == 'prod') {
    stream.pipe(uglify())
  }

  stream.pipe(gulp.dest(paths.dest + 'js/'))
});

gulp.task('scripts', function() {
  stream = gulp.src(paths.src + 'scripts/index.coffee', { read: false })
    .pipe(plumber())
    .pipe(browserify({
      debug: environment == 'dev',
      transform: ['coffeeify', 'jadeify'],
      extensions: ['.coffee', '.jade']
    }))
    .pipe(concat('index.js'))

  if (environment == 'prod') {
    stream.pipe(uglify())
  }

  stream.pipe(gulp.dest(paths.dest + 'js/'))
});

gulp.task('templates', function() {
  gulp.src(paths.src + 'index.jade')
    .pipe(plumber())
    .pipe(jade({
      pretty: environment == 'dev'
    }))
    .pipe(gulp.dest(paths.dest))
});

gulp.task('styles', function () {
  stream = gulp.src(paths.src + 'styles/**/*.styl')
    .pipe(plumber())
    .pipe(stylus({ use: ['nib']}))
    .pipe(concat('main.css'))

  if (environment == 'prod') {
    stream.pipe(minify())
  }

  stream.pipe(gulp.dest(paths.dest + 'css/'))
});

gulp.task('watch', function () {
  var server = livereload();

  gulp.watch(paths.src + 'scripts/**', ['scripts']);
  gulp.watch(paths.src + 'styles/**/*.styl', ['styles']);
  gulp.watch(paths.vendor + 'scripts/**', ['vendor-scripts']);
  gulp.watch(paths.src + 'index.jade', ['templates']);

  gulp.watch(paths.dest + '/**').on('change', function(file) {
      server.changed(file.path);
    });
});

gulp.task('vendor', ['vendor-styles', 'vendor-scripts']);
gulp.task('compile', ['templates', 'styles', 'scripts']);

gulp.task('default', ['assets', 'vendor', 'compile']);
gulp.task('prod', ['set-prod', 'default']);
