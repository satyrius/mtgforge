var gulp = require('gulp'),
  browserify = require('gulp-browserify'),
  rename = require('gulp-rename'),
  clean = require('gulp-clean'),
  stylus = require('gulp-stylus'),
  concat = require('gulp-concat'),
  uglify = require('gulp-uglify'),
  minify = require('gulp-csso');

var paths = {
  app: [
    './app/init.coffee'
  ],
  styles: ['./vendor/styles/bootstrap.css', './app/styles/**/*.styl'],
  dist: './public/',
  assets: './app/assets/**/*'
};

var env = 'dev';

gulp.task('scripts', function() {
  var stream = gulp.src(paths.app, {read: false})
    .pipe(browserify({
      debug: env === 'dev',
      transform: ['coffeeify', 'hbsfy'],
      extensions: ['.coffee', '.hbs']
    }))
    .pipe(rename('app.js'));

  if (env === 'prod') {
    stream.pipe(uglify());
  }
    
  stream.pipe(gulp.dest(paths.dist + 'js/'));
});

gulp.task('w', function() {
  gulp.watch('./app/**/*.coffee', ['scripts']);
  gulp.watch(paths.styles, ['styles']);
})

gulp.task('clean', function() {
  return gulp.src(paths.dist + '**/*', {read: false})
    .pipe(clean());
})

gulp.task('styles', function () {
  var stream = gulp.src(paths.styles)
    .pipe(stylus())
    .pipe(concat('app.css'));

  if (env === 'prod') {
    stream.pipe(minify()); 
  }

  stream.pipe(gulp.dest(paths.dist + 'css/'))
});

gulp.task('assets', function() {
  gulp.src(paths.assets)
    .pipe(gulp.dest(paths.dist));
});

gulp.task('prod', function() {
  env = 'prod';
})

gulp.task('build:prod', ['prod', 'default']);

gulp.task('default', ['clean', 'scripts', 'styles', 'assets']);
