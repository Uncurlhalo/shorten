/*global module:false*/
module.exports = function (grunt) {

  'use strict';

  // Project configuration.
  grunt.initConfig({
    lint: {
      files: ['grunt.js', 'app.js']
    },
    watch: {
      files: '<config:lint.files>',
      tasks: 'lint min'
    },
    jshint: {
      options: {
        curly: true,
        eqeqeq: true,
        forin: true,
        immed: true,
        indent: 2,
        latedef: true,
        newcap: true,
        noarg: true,
        noempty: true,
        nonew: true,
        quotmark: 'single',
        undef: true,
        unused: true,
        strict: true,
        trailing: true,
        maxdepth: 5,
        /* relaxing options */
        node: true,
        es5: true
      },
      globals: {
        jQuery: true
      }
    },
    min: {
      dist: {
        src: ['app.js'],
        dest: 'app.min.js'
      }
    }
  });

  // Default task.
  grunt.registerTask('default', ['lint', 'min']);

};
