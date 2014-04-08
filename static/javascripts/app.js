/*jslint es5: true, indent: 2, browser: true*/
/*global jQuery: true*/

(function ($) {
  'use strict';

  $(document).ready(function () {
    var onSuccess, onError, selectNode, displayTooltip;

    $('#url').focus();

    selectNode = function (el) {
      var range = $(document).get()[0].createRange(),
          selection = $(window).get()[0].getSelection();
      range.selectNodeContents(el);
      selection.removeAllRanges();
      selection.addRange(range);
    };

    displayTooltip = function (el) {
      var isMac = navigator.userAgent.match(/Mac/) !== null,
          title = isMac ? 'Press ⌘-C to copy' : 'Press Ctrl+C to copy';
      $(el).tooltip({
        placement: 'right',
        title: title,
        trigger: 'manual',
      }).tooltip('show');
    };

    onSuccess = function (data) {
      var absoluteUrl = $(location).attr('href') + data.short_id,
          shortUrl = $('#short-url'),
          shortUrlLink = shortUrl.find('a');

      $('#url').val(data.url);
      $('#error').hide();

      shortUrlLink
        .attr('href', data.short_id)
        .text(absoluteUrl);
      shortUrl.find('small')
        .text('Created at: ' + data.created_at);
      shortUrl.fadeIn();

      selectNode(shortUrlLink[0]);
      displayTooltip(shortUrlLink);
    };

    onError = function () {
      $('#short-url').hide();
      $('#error').fadeIn();
    };

    $('#shorten').on('submit', function (e) {
      e.preventDefault();
      var url = $('#url').val();
      $.ajax({
        url: '/l/',
        type: 'POST',
        data: {
          url: url
        },
        timeout: 10000,
        success: onSuccess,
        error: onError
      });
    });
  });

})(jQuery);
