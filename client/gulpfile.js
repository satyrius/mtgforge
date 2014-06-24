var gulp = require('gulp'),
    plumber = require('gulp-plumber'),
    debug = require('gulp-debug'),
    streamqueue = require('streamqueue'),
    path = require('path'),
    concat = require('gulp-concat'),
    clean = require('gulp-clean'),
    browserify = require('gulp-browserify'),
    jade = require('gulp-jade'),
    stylus = require('gulp-stylus'),
    less = require('gulp-less'),
    uglify = require('gulp-uglify'),
    minify = require('gulp-minify-css'),
    replace = require('gulp-replace');

var twbs_path = path.join(__dirname, 'node_modules', 'twitter-bootstrap-3.0.0')

var environment = 'dev',
    verbose = false,
    paths = {
      dest: './public/',
      vendor: './vendor/',
      index: './app/index.jade',
      scripts: {
        index: './app/index.coffee',
        all: [
          './app/**/*.coffee',
          './app/**/*.jade'
        ]
      },
      bootstrap: {
        styles: './vendor/styles/bootstrap.less',
        fonts: [
          path.join(twbs_path, 'fonts', '*.eot'),
          path.join(twbs_path, 'fonts', '*.svg'),
          path.join(twbs_path, 'fonts', '*.ttf'),
          path.join(twbs_path, 'fonts', '*.woff')
        ]
      },
      styles: './app/**/*.styl'
    }

gulp.task('set-prod', function() {
  environment = 'prod';
});

gulp.task('clean', function() {
  return gulp.src(paths.dest + '**/*', {read: false})
    .pipe(clean());
});

gulp.task('bootstrap', function () {
  var stream = gulp.src(paths.bootstrap.styles)
    .pipe(less({
      paths: [path.join(twbs_path, 'less')]
    }))
    .pipe(concat('vendor.css'));

  if (environment == 'prod') {
    stream.pipe(minify())
  }

  stream.pipe(gulp.dest(paths.dest + 'css'))

  // Also copy fonts
  gulp.src(paths.bootstrap.fonts)
    .pipe(gulp.dest(paths.dest + 'fonts'))
});

gulp.task('styles', function () {
  var stream = gulp.src(paths.styles)
    .pipe(plumber())
    //.pipe(debug({verbose: verbose}))
    .pipe(stylus({use: ['nib']}))
    .pipe(concat('app.css'));

  if (environment == 'prod') {
    stream.pipe(minify())
  }

  stream.pipe(gulp.dest(paths.dest + 'css'));
});

gulp.task('scripts', function() {
  host = process.env.API_HOST
  host = host ? 'http://' + host : ''

  stream = gulp.src(paths.scripts.index, { read: false })
    .pipe(plumber())
    .pipe(browserify({
      debug: environment == 'dev',
      transform: ['coffeeify', 'jadeify'],
      extensions: ['.coffee', '.jade']
    }))
    .pipe(replace('$API_HOST', host))
    .pipe(concat('app.js'))

  if (environment == 'prod') {
    stream.pipe(uglify())
  }

  stream.pipe(gulp.dest(paths.dest + 'js'))
});

gulp.task('index', function() {
  gulp.src(paths.index)
    .pipe(plumber())
    .pipe(jade({
      pretty: environment == 'dev'
    }))
    .pipe(gulp.dest(paths.dest))
});

gulp.task('watch', ['default'], function () {
  gulp.watch(paths.scripts.all, ['scripts']);
  gulp.watch(paths.styles, ['styles']);
  gulp.watch(paths.index, ['index']);
});

gulp.task('compile', ['index', 'styles', 'scripts']);

gulp.task('default', ['clean', 'bootstrap', 'compile']);
gulp.task('prod', ['set-prod', 'default']);
