var gulp = require('gulp'),
    plumber = require('gulp-plumber'),
    debug = require('gulp-debug'),
    streamqueue = require('streamqueue'),
    concat = require('gulp-concat'),
    clean = require('gulp-clean'),
    browserify = require('gulp-browserify'),
    jade = require('gulp-jade'),
    stylus = require('gulp-stylus'),
    uglify = require('gulp-uglify'),
    minify = require('gulp-minify-css'),
    livereload = require('gulp-livereload');

var environment = 'dev',
    verbose = false,
    paths = {
      src: './app/',
      dest: './public/',
      vendor: './vendor/',
      assets: './assets/',
      scripts: './app/scripts/index.coffee',
      styles: {
        vendor: [
          './vendor/styles/bootstrap.css',
          './vendor/styles/bootstrap-theme.css'
        ],
        app: [
          './app/styles/*.styl'
        ]
      }
    }

gulp.task('set-prod', function() {
  environment = 'prod';
});

gulp.task('clean', function() {
  return gulp.src(paths.dest + '**/*', {read: false})
    .pipe(clean());
});

gulp.task('assets', function() {
 gulp.src(paths.assets + '**')
    .pipe(plumber())
    .pipe(gulp.dest(paths.dest));
});

gulp.task('styles', function () {
  var stream = gulp.src(paths.styles.app)
    .pipe(plumber())
    //.pipe(debug({verbose: verbose}))
    .pipe(stylus())
    .pipe(concat('app.css'));

  if (environment == 'prod') {
    stream.pipe(minify())
  }

  stream.pipe(gulp.dest(paths.dest + 'css/'))
});

gulp.task('vendor-styles', function () {
  var stream = gulp.src(paths.styles.vendor)
    .pipe(concat('vendor.css'));

  if (environment == 'prod') {
    stream.pipe(minify())
  }

  stream.pipe(gulp.dest(paths.dest + 'css/'))
});

gulp.task('scripts', function() {
  stream = gulp.src(paths.scripts, { read: false })
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

gulp.task('watch', ['default'], function () {
  var server = livereload();

  gulp.watch(paths.src + 'scripts/**', ['scripts']);
  gulp.watch(paths.styles.app, ['styles']);
  gulp.watch(paths.src + 'index.jade', ['templates']);

  gulp.watch(paths.dest + '/**').on('change', function(file) {
      server.changed(file.path);
    });
});

gulp.task('compile', ['templates', 'styles', 'scripts']);

gulp.task('default', ['clean', 'assets', 'vendor-styles', 'compile']);
gulp.task('prod', ['set-prod', 'default']);
