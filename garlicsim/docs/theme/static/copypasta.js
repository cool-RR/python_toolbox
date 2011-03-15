(function() {
  var $, append_to_element, blank_dialog, blank_widget, copypasta, cover, css, currentContainer, currentLive, debug_msg, dialog_types, e, editable_click, editable_elements, end_editing, find_current_url, form_data, handle_dialog_message, handle_widget_message, hide_edit_preview, hide_edit_previews, ids, iframe_host, images, indicator, init, is_scrolled_into_view, load_iframe_form, locate_text_containers, overlay, paths, queue, receive_from_iframe, resize, s, scripts, send_to_iframe, show_dialog, show_edit_dialog, show_edit_preview, start_editing, static_host, w, widget, widget_url;
  w = window;
  if (!w.postMessage) {
    return;
  }
  append_to_element = ((function() {
    var _i, _len, _ref, _results;
    _ref = document.documentElement.childNodes;
    _results = [];
    for (_i = 0, _len = _ref.length; _i < _len; _i++) {
      e = _ref[_i];
      if (e.nodeType === 1) {
        _results.push(e);
      }
    }
    return _results;
  })())[0];
  iframe_host = "https://copypasta.credibl.es";
  static_host = "//copypasta.credibl.es";
  css = document.createElement('link');
  css.rel = "stylesheet";
  css.href = static_host + "/stylesheets/compiled/copypasta.css?v=2";
  append_to_element.appendChild(css);
  $ = false;
  currentLive = false;
  currentContainer = false;
  form_data = {};
  w.copypasta = copypasta = {
    $: false,
    page_id: w.copypasta_page_id
  };
  copypasta.account_id = w.copypasta_account_id;
  copypasta.debug = w.copypasta_debug || w.location.hash.indexOf('copypasta-debug') > 0;
  copypasta.auto_start = w.copypasta_auto_start || w.location.hash.indexOf('copypasta-auto') > 0;
  copypasta.include_url_hash = w.copypasta_include_url_hash;
  copypasta.content_selector = w.copypasta_content_selector;
  copypasta.paragraph_threshold = w.copypasta_paragraph_threshold || 3;
  copypasta.character_threshold = w.copypasta_character_threshold || 100;
  copypasta.locate_text_containers = locate_text_containers = function() {
    var containers, p, parent, parent_character_count, parent_count, _i, _len, _ref;
    containers = [];
    parent = false;
    parent_count = 0;
    parent_character_count = 0;
    _ref = $('p');
    for (_i = 0, _len = _ref.length; _i < _len; _i++) {
      p = _ref[_i];
      p = $(p);
      if (parent !== p.parent().get(0)) {
        if (parent_count >= copypasta.paragraph_threshold || parent_character_count > copypasta.character_threshold) {
          containers.push(parent);
        }
        parent = p.parent().get(0);
        parent_count = 0;
        parent_character_count = p.text().length;
      }
      parent_count += 1;
      parent_character_count += p.text().length;
    }
    if (parent_count >= copypasta.paragraph_threshold || parent_character_count > copypasta.character_threshold) {
      containers.push(parent);
    }
    return containers;
  };
  debug_msg = function(msg) {
    if (copypasta.debug) {
      if (console && console.log) {
        return console.log(msg);
      }
    }
  };
  ids = {
    indicator: 'copy-pasta-edit-indicator',
    dialog: 'copy-pasta-dialog',
    iframe: 'copy-pasta-iframe',
    btn: 'copy-pasta-button',
    widget: 'copy-pasta-widget'
  };
  paths = {
    indicator: '#' + ids.indicator,
    dialog: '#' + ids.dialog,
    btn: '#copypasta-button, #copy-pasta-button, .copy-pasta-button',
    active: '.copy-pasta-active',
    iframe: '#' + ids.iframe,
    overlay: '.copy-pasta-overlay',
    status: '#copy-pasta-button .status',
    widget: '#' + ids.widget,
    widget_iframe: '#' + ids.widget + ' iframe'
  };
  indicator = function() {
    if ($(paths.indicator).length === 0) {
      $('body').append('<div id="' + ids.indicator + '"><p>click to correct</p></div>');
      $(paths.indicator).bind('mouseout', deactivate);
      $(paths.indicator).bind('click', show_edit_dialog);
    }
    return $(paths.indicator);
  };
  overlay = function(el) {
    if ($(el).prev(paths.overlay).length === 0) {
      $(el).before('<div class="copy-pasta-overlay"></div>');
    }
    return $(el).prev(paths.overlay);
  };
  cover = function(target, element) {
    var sz;
    sz = {
      width: $(target).outerWidth() + 'px',
      height: $(target).outerHeight() + 'px'
    };
    element || (element = overlay(target).fadeIn());
    return $(element).css(sz);
  };
  find_current_url = function() {
    var a, oh, url;
    oh = w.location.hash;
    if (copypasta.include_url_hash) {
      w.location.hash = w.location.hash.replace(/#?copypasta-[a-z]+/g, '');
    } else {
      w.location.hash = '';
    }
    url = $('link[rel=canonical]').attr('href') || w.location.href.replace(/#+$/, '');
    a = w.document.createElement('a');
    a.href = url;
    url = a.href;
    w.location.hash = oh;
    return url;
  };
  blank_dialog = function(class_name) {
    return '<div id="' + ids.dialog + '" class="' + class_name + '"><iframe frameborder="no" id="' + ids.iframe + '" scrolling="no"></iframe></div>';
  };
  resize = function(path, data) {
    return $(path).animate({
      height: data.h
    });
  };
  show_edit_dialog = function() {
    var account_id, page_id, url, _ref, _ref2, _ref3;
    e = currentLive;
    (_ref = e.original_text) != null ? _ref : e.original_text = e.innerHTML;
    page_id = (_ref2 = copypasta.page_id) != null ? _ref2 : '';
    account_id = (_ref3 = copypasta.account_id) != null ? _ref3 : '';
    form_data.new_edit = {
      'edit[original]': e.original_text,
      'edit[proposed]': e.original_text,
      'edit[url]': find_current_url(),
      'edit[element_path]': copypasta.getElementCssPath(e)
    };
    url = iframe_host + '/edits/new?view=framed&url=' + escape(find_current_url()) + '&page[key]=' + escape(page_id) + '&account_id=' + account_id;
    $(paths.widget).hide();
    return show_dialog(url, 'edit');
  };
  dialog_types = {
    "default": {
      options: {
        escClose: true,
        overlayClose: true,
        overlayId: 'copy-pasta-lightbox-overlay',
        containerId: 'copy-pasta-lightbox-container',
        opacity: 70,
        persist: true
      }
    },
    edit: {
      "class": 'copy-pasta-lightbox'
    }
  };
  show_dialog = function(src, type) {
    var t;
    if (!$.fn.modal) {
      copypasta.modal_init($);
    }
    if ($.modal && $('#copy-pasta-lightbox-container').length > 0) {
      $.modal.close();
      return setTimeout((function() {
        return show_dialog(src, type);
      }), 11);
    } else {
      t = dialog_types["default"];
      t.options.onShow = function() {
        if (src) {
          cover(paths.iframe);
          debug_msg("Overlay shown");
          src = src;
          if (copypasta.debug) {
            src += '#debug';
          }
          debug_msg("Loading iframe: " + src);
          return $(paths.iframe).attr('src', src);
        }
      };
      if (type && dialog_types[type]) {
        t = dialog_types[type];
        if (!t.options) {
          t.options = {};
        }
        if (!t.extended) {
          t.options = $.extend(t.options, dialog_types["default"].options);
        }
        t.extended = true;
      }
      return $.modal(blank_dialog(t["class"]), t.options);
    }
  };
  widget_url = function() {
    var account_id, page_id, url, _ref, _ref2;
    page_id = (_ref = copypasta.page_id) != null ? _ref : '';
    account_id = (_ref2 = copypasta.account_id) != null ? _ref2 : '';
    return url = iframe_host + '/edits?view=framed&url=' + escape(find_current_url()) + '&page[key]=' + escape(page_id) + '&account_id=' + account_id;
  };
  blank_widget = '<div id="' + ids.widget + '"><h1><a href="https://copypasta.credibl.es"><img src="' + static_host + '/images/logo-small.png" /></a></h1><iframe frameborder="no" scrolling="no"></iframe></div>';
  widget = function(src) {
    var iframe;
    if ($(paths.widget).length === 0) {
      $('body').append(blank_widget);
      if (src == null) {
        src = widget_url();
      }
    }
    if (src != null) {
      iframe = $(paths.widget).find('iframe').attr('src', src);
      cover(iframe);
    }
    return $(paths.widget).show();
  };
  show_edit_preview = function(data) {
    var pos, s, target;
    debug_msg('Previewing ' + data.element_path);
    target = $(data.element_path);
    pos = target.position();
    if (!target.get(0).original_text) {
      target.get(0).original_text = target.html();
    }
    s = $('html').scrollTop(1) > 0 ? 'html' : 'body';
    return $(s).animate({
      scrollTop: pos.top
    }, function() {
      return target.html(data.proposed).addClass('copy-pasta-preview');
    });
  };
  hide_edit_preview = function(path) {
    var target;
    target = $(path);
    return target.removeClass('copy-pasta-preview').html(target.get(0).original_text);
  };
  hide_edit_previews = function() {
    return $('.copy-pasta-preview').each(function() {
      var o, _ref;
      o = (_ref = this.original_text) != null ? _ref : $(this).html();
      return $(this).removeClass('copy-pasta-preview').html(o);
    });
  };
  is_scrolled_into_view = function(elem) {
    var docViewBottom, docViewTop, elemBottom, elemTop;
    docViewTop = $(window).scrollTop();
    docViewBottom = docViewTop + $(window).height();
    elemTop = $(elem).offset().top;
    elemBottom = elemTop + $(elem).height();
    return (elemBottom >= docViewTop) && (elemTop <= docViewBottom) && (elemBottom <= docViewBottom) && (elemTop >= docViewTop);
  };
  load_iframe_form = function(id) {
    if (id && form_data[id]) {
      send_to_iframe({
        'label': 'form_data',
        'data': form_data[id]
      });
      return form_data[id] = false;
    }
  };
  send_to_iframe = function(msg) {
    debug_msg("Parent send: " + msg.label + " to " + iframe_host);
    msg = JSON.stringify(msg);
    return $(paths.iframe).get(0).contentWindow.postMessage(msg, iframe_host);
  };
  receive_from_iframe = function(e) {
    var data;
    if (e.origin !== iframe_host) {
      debug_msg(e);
      return;
    }
    data = JSON.parse(e.data);
    debug_msg("Parent receive: " + data.label + " from " + e.origin + ' for frame type: ' + data.frame_type);
    if (data.frame_type === 'dialog') {
      return handle_dialog_message(data);
    } else {
      return handle_widget_message(data);
    }
  };
  handle_widget_message = function(data) {
    if (data.label === 'ready') {
      return overlay(paths.widget_iframe).fadeOut();
    } else if (data.label === 'loading') {
      return cover(paths.widget_iframe);
    } else if (data.label === 'resize') {
      return resize(paths.widget + ' iframe', data);
    } else if (data.label === 'finished') {
      return end_editing();
    } else if (data.label === 'preview') {
      return show_edit_preview(data);
    } else if (data.label === 'preview-off') {
      return hide_edit_preview(data.element_path);
    }
  };
  handle_dialog_message = function(data) {
    if (data.label === 'ready') {
      if (!load_iframe_form(data.form_id)) {
        return overlay(paths.iframe).fadeOut();
      }
    } else if (data.label === 'form_data_loaded') {
      return overlay(paths.iframe).fadeOut();
    } else if (data.label === 'finished') {
      if ($.modal) {
        $.modal.close();
      }
      hide_edit_previews();
      widget().show();
      if (data.reload_widget) {
        cover(paths.widget_iframe);
        return $(paths.widget_iframe).attr('src', $(paths.widget_iframe).attr('src'));
      }
    } else if (data.label === 'resize') {
      return resize(paths.dialog, data);
    }
  };
  editable_elements = 'p, h1, h2, h3, h4, h5, td, th, li';
  editable_click = function(e) {
    if (!(e instanceof HTMLAnchorElement)) {
      currentLive = this;
      show_edit_dialog();
      return false;
    }
  };
  copypasta.start_editing = start_editing = function() {
    var elements;
    images.load();
    $(paths.btn).addClass('on');
    elements = $(currentContainer).addClass('copy-pasta-active').find(editable_elements).filter(':visible').filter(function(i) {
      return $.trim($(this).text()) !== '';
    });
    debug_msg("Found " + elements.length + " editable elements");
    elements.addClass('copy-pasta-editable').bind('click', editable_click);
    return widget();
  };
  end_editing = function() {
    $(paths.btn).removeClass('on');
    hide_edit_previews();
    $(currentContainer).removeClass('copy-pasta-active');
    $('.copy-pasta-editable').removeClass('copy-pasta-editable').unbind('click', editable_click);
    return widget().remove();
  };
  init = function() {
    if (!(window.JSON && window.postMessage)) {
      return;
    }
    if (copypasta.content_selector) {
      currentContainer = $(copypasta.content_selector);
    } else {
      currentContainer = $(locate_text_containers());
    }
    $(paths.btn).show().bind('click', function() {
      if ($(this).hasClass('on')) {
        return end_editing();
      } else {
        return start_editing();
      }
    });
    if (w.addEventListener) {
      w.addEventListener('message', receive_from_iframe, false);
    } else if (w.attachEvent) {
      w.attachEvent('onmessage', function() {
        return receive_from_iframe(event);
      });
    }
    if (copypasta.auto_start) {
      return start_editing();
    }
  };
  scripts = [
    {
      test: function() {
        if (w.jQuery && w.jQuery.fn && w.jQuery.fn.jquery > "1.3") {
          copypasta.$ = $ = w.jQuery;
          debug_msg("Using existing jquery: version " + $.fn.jquery);
          return true;
        }
      },
      src: '//copypasta.credibl.es/javascripts/jquery-1.4.4.min.js',
      callback: function() {
        (copypasta.$ = $ = w.jQuery).noConflict(1);
        return debug_msg("Loaded own jquery: version " + $.fn.jquery);
      }
    }, {
      test: function() {
        return copypasta.getElementCssPath && w.jQuery && w.jQuery.fn.lightbox_me;
      },
      src: '//copypasta.credibl.es/javascripts/utils.min.js'
    }
  ];
  scripts.load = function(queue, callback) {
    var def, i, remaining, s;
    remaining = (function() {
      var _i, _len, _results;
      _results = [];
      for (_i = 0, _len = queue.length; _i < _len; _i++) {
        i = queue[_i];
        if (!i.state) {
          _results.push(i);
        }
      }
      return _results;
    })();
    if (remaining.length === 0) {
      return;
    }
    def = remaining.pop();
    def.state = 'pending';
    s = document.createElement('script');
    s.type = "text/javascript";
    s.src = def.src;
    s.onload = s.onreadystatechange = function() {
      var d, i;
      d = this.readyState;
      if (def.state !== 'loaded' && (!d || d === 'loaded' || d === 'complete')) {
        def.state = 'loaded';
        if (def.callback) {
          def.callback();
        }
        remaining = (function() {
          var _i, _len, _results;
          _results = [];
          for (_i = 0, _len = queue.length; _i < _len; _i++) {
            i = queue[_i];
            if (i.state !== 'loaded') {
              _results.push(i);
            }
          }
          return _results;
        })();
        if (remaining.length === 0) {
          return callback();
        }
      }
    };
    if (queue.length > 0) {
      scripts.load(queue, callback);
    }
    return append_to_element.appendChild(s);
  };
  images = ["translucent-blue.png", "translucent-black.png", "translucent-black-85.png", "loading.gif", "pencil.png", "logo-small.png"];
  images.load = function() {
    var i, img, _i, _len, _results;
    _results = [];
    for (_i = 0, _len = images.length; _i < _len; _i++) {
      i = images[_i];
      img = new Image;
      _results.push(img.src = static_host + '/images/' + i);
    }
    return _results;
  };
  queue = (function() {
    var _i, _len, _results;
    _results = [];
    for (_i = 0, _len = scripts.length; _i < _len; _i++) {
      s = scripts[_i];
      if (s && !s.test()) {
        _results.push(s);
      }
    }
    return _results;
  })();
  if (queue.length > 0) {
    scripts.load(queue, init);
  } else {
    init();
  }
}).call(this);
