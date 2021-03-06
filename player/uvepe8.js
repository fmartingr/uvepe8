// Generated by CoffeeScript 1.3.3

/*
# UVEPE8 Player
# Author:       Felipe "Pyron" Martín (@fmartingr)
# Notes:		    See README
*/


(function() {
  var uvepe8;

  uvepe8 = function(dom_object, animation, autostart) {
    if (!(this instanceof uvepe8)) {
      return new uvepe8(dom_object, animation, autostart);
    } else {
      return this.init(dom_object, animation, autostart);
    }
  };

  uvepe8.prototype = {
    log: function(string) {
      if (this.options.log != null) {
        return console.log(string);
      }
    },
    framework: function(selector) {
      var dom_elements;
      dom_elements = document.querySelectorAll(selector);
      dom_elements = Array.prototype.slice.call(dom_elements);
      if (dom_elements.length > 1) {
        if (typeof console !== "undefined" && console !== null) {
          console.error("WARNING: There are more elements with this selector query! Using the first one.");
        }
      }
      return dom_elements[0];
    },
    canvas_supported: function() {
      var element;
      element = this.create_canvas();
      return !!(element.getContext('2d'));
    },
    draw_canvas: function() {
      var destiny_x, destiny_y, diff, frame, height, source_x, source_y, width, _i, _len, _ref;
      this.log("Draw frame " + this.current_frame);
      frame = this.get_frame(this.current_frame);
      if (frame !== null) {
        if (this.current_frame === 0) {
          this.buffer_context.drawImage(this.image, 0, 0, this.options.width, this.options.height, 0, 0, this.options.width, this.options.height);
        } else {
          _ref = frame.diff;
          for (_i = 0, _len = _ref.length; _i < _len; _i++) {
            diff = _ref[_i];
            this.log(diff);
            destiny_x = diff[0];
            destiny_y = diff[1];
            source_x = diff[2];
            source_y = diff[3];
            width = diff[4];
            height = diff[5];
            this.buffer_context.clearRect(destiny_x, destiny_y, width, height);
            this.buffer_context.drawImage(this.image, source_x, source_y, width, height, destiny_x, destiny_y, width, height);
          }
        }
        this.dom_context.clearRect(0, 0, this.options.width, this.options.height);
        return this.dom_context.drawImage(this.buffer_element, 0, 0);
      }
    },
    draw_fallback: function() {
      var destiny_x, destiny_y, diff, element, frame, height, source_x, source_y, width, _i, _len, _ref;
      this.log("Draw frame " + this.current_frame);
      frame = this.get_frame(this.current_frame);
      if (frame !== null) {
        if (this.current_frame === 0) {
          element = this.create_div();
        } else {
          _ref = frame.diff;
          for (_i = 0, _len = _ref.length; _i < _len; _i++) {
            diff = _ref[_i];
            this.log(diff);
            destiny_x = diff[0];
            destiny_y = diff[1];
            source_x = diff[2];
            source_y = diff[3];
            width = diff[4];
            height = diff[5];
            element = this.create_div(source_x, source_y, destiny_x, destiny_y, width, height);
            if (width === this.options.width && height === this.options.height) {
              element.style.className = 'full-sized-frame';
            }
          }
        }
        return this.dom_layer.appendChild(element);
      }
    },
    get_frame: function(number) {
      if (this.options.frames[number] != null) {
        return this.options.frames[number];
      } else {
        return null;
      }
    },
    draw: function() {
      var frame, timeout,
        _this = this;
      frame = this.get_frame(this.current_frame);
      if (frame !== null) {
        timeout = this.options.timeout;
        if (frame.jump != null) {
          timeout = timeout * frame.jump;
        }
        this.log("Frame: " + this.current_frame + " with timeout: " + timeout);
        this.timeout_id = setTimeout(function() {
          return _this.draw();
        }, timeout);
        if (this.use_canvas) {
          this.draw_canvas();
        } else {
          this.draw_fallback();
        }
        return this.current_frame++;
      }
    },
    play: function() {
      if (this.image_loaded) {
        return this.draw();
      } else {
        return console.error("[Image is not loaded! (is probably loading...)]");
      }
    },
    pause: function() {
      return clearTimeout(this.timeout_id);
    },
    stop: function() {
      this.pause();
      this.current_frame = 0;
      if (this.use_canvas) {
        return this.draw_canvas();
      }
    },
    create_canvas: function() {
      return document.createElement('canvas');
    },
    create_div: function(source_x, source_y, destiny_x, destiny_y, width, height) {
      var layer;
      if (source_x == null) {
        source_x = 0;
      }
      if (source_y == null) {
        source_y = 0;
      }
      if (destiny_x == null) {
        destiny_x = 0;
      }
      if (destiny_y == null) {
        destiny_y = 0;
      }
      if (width == null) {
        width = this.options.width;
      }
      if (height == null) {
        height = this.options.height;
      }
      layer = document.createElement('div');
      layer.style.position = 'absolute';
      layer.style.left = "" + destiny_x + "px";
      layer.style.top = "" + destiny_y + "px";
      layer.style.backgroundImage = "url(" + this.options.image + ")";
      layer.style.backgroundPosition = "-" + source_x + "px -" + source_y + "px";
      layer.style.width = "" + width + "px";
      layer.style.height = "" + height + "px";
      layer.style.zIndex = this.current_frame;
      return layer;
    },
    start_canvas: function() {
      this.dom_canvas = this.create_canvas();
      this.dom_canvas.width = this.options.width;
      this.dom_canvas.height = this.options.height;
      this.dom_context = this.dom_canvas.getContext('2d');
      this.dom.appendChild(this.dom_canvas);
      this.buffer_element = this.create_canvas();
      this.buffer_element.width = this.options.width;
      this.buffer_element.height = this.options.height;
      return this.buffer_context = this.buffer_element.getContext('2d');
    },
    start_fallback: function() {
      this.dom_layer = this.create_div();
      this.dom_layer.style.position = 'relative';
      this.dom_layer.className = 'uvepe8-fallback';
      return this.dom.appendChild(this.dom_layer);
    },
    init: function(dom_object, animation, autostart) {
      var _this = this;
      if (autostart == null) {
        autostart = true;
      }
      if (animation != null) {
        this.options = animation;
      }
      if (dom_object != null) {
        this.options.dom = dom_object;
      }
      this.use_canvas = this.canvas_supported();
      this.dom = this.framework(this.options.dom);
      this.options.timeout = 1000 / this.options.fps;
      this.image = new Image();
      this.image.src = this.options.image;
      this.dom.style.width = this.options.width;
      this.dom.style.height = this.options.height;
      if (this.use_canvas) {
        this.start_canvas();
      } else {
        this.start_fallback();
      }
      this.image.onload = function() {
        _this.image_loaded = true;
        _this.stop();
        if (autostart) {
          return _this.play();
        }
      };
      return this;
    }
  };

  window.uvepe8 = uvepe8;

}).call(this);
