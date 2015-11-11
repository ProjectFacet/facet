(function(){
  'use strict';

  // lazy load images
  var WrapkitUtils = window.WrapkitUtils,
  imagesLoaded = window.imagesLoaded,
  imgLoad = imagesLoaded('.gallery-item');

  // prepare for load
  $('.gallery-item img').addClass('fade');
  // add loader to item container
  var loaderIndicator = $('<div/>'),
  indicator = '<div class="loader-inner ball-scale-multiple"><div class="bg-teal"></div><div class="bg-teal"></div><div class="bg-teal"></div></div>';

  loaderIndicator.addClass('gallery-loader')
  .html(indicator);

  $('.gallery-item > .thumbnail').append(loaderIndicator);

  imgLoad.on( 'progress', function(instance, image){
    var $img = $(image.img),
    $container = $img.closest('.gallery-item'),
    isLoaded = image.isLoaded;

    if(isLoaded){
      $container.find('.gallery-loader').remove();
      $img.addClass('in');
    }
  })
  .on( 'fail', function(instance){

    $.each(instance.images, function(i, image){
      var isLoaded = image.isLoaded,
      $container = $(instance.elements[i]);

      // append fail indocator and remove loader when img is broken
      if (!isLoaded) {
        var imgFail = $('<div/>');
        imgFail.addClass('img-fail')
        .attr('title', 'Image not loaded')
        .html('<i class="fa fa-chain-broken"></i>');

        $container.addClass('gallery-fail')
        .find('.thumbnail').append(imgFail);
        // remove loader
        $container.find('.gallery-loader').remove();
      }
    });
  });


  // mixitup
  $('#gallery').mixItUp();
  $('.gallery-col').addClass('filter-result');

  $(document).on( 'click', '[data-toggle="gallery-sort"]', function(e){
    e.preventDefault();

    var $this = $(this),
    data = $this.data();

    $('[data-toggle="gallery-sort"]').removeClass('focus');
    $this.addClass('focus');

    $('#gallery').mixItUp( 'sort', data.sort);
  })
  .on( 'keyup', '[data-toggle="gallery-filter"]', WrapkitUtils.debounce(function(){

    var $this = $(this),
    val = $this.val(),
    target = 'all';

    $('.gallery-col').removeClass('filter-result');
    $('.gallery-col:contains("'+ val +'")').addClass('filter-result');


    if($('.filter-result')){
      target = '.filter-result';
    } else{
      target = 'all';
    }

    $('#gallery').mixItUp('filter', target);
  }, 300))
  .on( 'click', '[data-toggle="gallery-layout"]', function(){
    var isGrid = $('#gallery').hasClass('gallery-grid');
    $('#gallery').toggleClass('gallery-grid gallery-list');

    if (isGrid) {
      $(this).children().attr('class', 'icon-grid');
    } else{
      $(this).children().attr('class', 'icon-list');
    }
  });




  // Photoswipe
  var PhotoSwipe = window.PhotoSwipe,
  PhotoSwipeUI_Default = window.PhotoSwipeUI_Default,
  classie = window.classie;

  var initPhotoSwipeFromDOM = function(gallerySelector) {
    // parse slide data (url, title, size ...) from DOM elements
    // (children of gallerySelector)
    var parseThumbnailElements = function(el) {
      var thumbElements = el.querySelectorAll('.gallery-col.filter-result'),
      numNodes = thumbElements.length,
      items = [],
      figureEl,
      linkEl,
      size,
      item;

      for (var i = 0; i < numNodes; i++) {

        figureEl = thumbElements[i]; // .gallery-col element

        // include only element nodes
        if (figureEl.nodeType !== 1) {
          continue;
        }

        linkEl = figureEl.querySelector('.thumbnail'); // .thumbnail element

        size = linkEl.getAttribute('data-size').split('x');

        // create slide object
        item = {
          src: linkEl.getAttribute('data-lref'), // get large href img
          w: parseInt(size[0], 10),
          h: parseInt(size[1], 10)
        };

        // .img-title content
        item.title = '<strong>' + figureEl.querySelector('.img-title').innerHTML + '</strong> - ' + figureEl.querySelector('.img-desc').innerHTML;

        // <img> thumbnail element, retrieving thumbnail url from .embed-responsive-item
        item.msrc = figureEl.querySelector('.embed-responsive-item').getAttribute('src');

        item.el = figureEl; // save link to element for getThumbBoundsFn
        items.push(item);
      }

      return items;
    };

    // find nearest parent element
    var closest = function closest(el, fn) {
      return el && (fn(el) ? el : closest(el.parentNode, fn));
    };

    // triggers when user clicks on thumbnail
    var onThumbnailsClick = function(e) {
      e = e || window.event;
      if (e.preventDefault) {
        e.preventDefault();
      } else {
        e.returnValue = false;
      }

      var eTarget = e.target || e.srcElement;

      // find root element of slide
      var clickedListItem = closest(eTarget, function(el) {
        return (classie.has(el, 'gallery-col'));
      });

      if (!clickedListItem) {
        return;
      }

      // find index of clicked item by looping through all child nodes
      // alternatively, you may define index via data- attribute
      var clickedGallery = clickedListItem.parentNode,
      childNodes = clickedListItem.parentNode.querySelectorAll('.gallery-col.filter-result'),
      numChildNodes = childNodes.length,
      nodeIndex = 0,
      index;

      for (var i = 0; i < numChildNodes; i++) {
        if (childNodes[i].nodeType !== 1) {
          continue;
        }

        if (childNodes[i] === clickedListItem) {
          index = nodeIndex;
          break;
        }
        nodeIndex++;
      }

      if (index >= 0) {
        if( classie.has(clickedGallery, 'gallery-list')){
          if (WrapkitUtils.closest(e.target, '.thumbnail')) {
            // open PhotoSwipe if valid index found
            openPhotoSwipe(index, clickedGallery);
          } else{
            return;
          }
        } else{
          if(WrapkitUtils.closest(e.target, '.embed-bar')){
            return;
          } else{
            // open PhotoSwipe if valid index found
            openPhotoSwipe(index, clickedGallery);
          }
        }
      }
      return false;
    };

    // parse picture index and gallery index from URL (#&pid=1&gid=2)
    var photoswipeParseHash = function() {
      var hash = window.location.hash.substring(1),
      params = {};

      if (hash.length < 5) {
        return params;
      }

      var vars = hash.split('&');
      for (var i = 0; i < vars.length; i++) {
        if (!vars[i]) {
          continue;
        }
        var pair = vars[i].split('=');
        if (pair.length < 2) {
          continue;
        }
        params[pair[0]] = pair[1];
      }

      if (params.gid) {
        params.gid = parseInt(params.gid, 10);
      }

      return params;
    };

    var openPhotoSwipe = function(index, galleryElement, disableAnimation, fromURL) {
      var pswpElement = document.querySelectorAll('.pswp')[0],
      gallery,
      options,
      items;

      items = parseThumbnailElements(galleryElement);

      // define options (if needed)
      options = {

        // define gallery index (for URL)
        galleryUID: galleryElement.getAttribute('data-pswp-uid'),

        getThumbBoundsFn: function(index) {
          // See Options -> getThumbBoundsFn section of documentation for more info
          var thumbnail = items[index].el.getElementsByTagName('img')[0], // find thumbnail
          pageYScroll = window.pageYOffset || document.documentElement.scrollTop,
          rect = thumbnail.getBoundingClientRect();

          return {
            x: rect.left,
            y: rect.top + pageYScroll,
            w: rect.width
          };
        }
      };

      // PhotoSwipe opened from URL
      if (fromURL) {
        if (options.galleryPIDs) {
          // parse real index when custom PIDs are used
          // http://photoswipe.com/documentation/faq.html#custom-pid-in-url
          for (var j = 0; j < items.length; j++) {
            if (items[j].pid === index) {
              options.index = j;
              break;
            }
          }
        } else {
          // in URL indexes start from 1
          options.index = parseInt(index, 10) - 1;
        }
      } else {
        options.index = parseInt(index, 10);
      }

      // exit if index not found
      if (isNaN(options.index)) {
        return;
      }

      if (disableAnimation) {
        options.showAnimationDuration = 0;
      }

      // Pass data to PhotoSwipe and initialize it
      gallery = new PhotoSwipe(pswpElement, PhotoSwipeUI_Default, items, options);
      gallery.init();
    };

    // loop through all gallery elements and bind events
    var galleryElements = document.querySelectorAll(gallerySelector);

    for (var i = 0, l = galleryElements.length; i < l; i++) {
      galleryElements[i].setAttribute('data-pswp-uid', i + 1);
      galleryElements[i].onclick = onThumbnailsClick;
    }

    // Parse URL and open gallery if it contains #&pid=3&gid=1
    var hashData = photoswipeParseHash();
    if (hashData.pid && hashData.gid) {
      openPhotoSwipe(hashData.pid, galleryElements[hashData.gid - 1], true, true);
    }
  };

  // execute above function
  initPhotoSwipeFromDOM('#gallery');

})(window);