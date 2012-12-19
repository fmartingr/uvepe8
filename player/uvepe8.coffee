###
# UVEPE8 Player
# Author:       Felipe "Pyron" Martín (@fmartingr)
# Notes:		    See README
###

uvepe8 = (dom_object, animation, autostart) ->
  # Creates new instance or initializates itself
  if not (@ instanceof uvepe8)
    new uvepe8(dom_object, animation, autostart)
  else
    @init(dom_object, animation, autostart)

uvepe8.prototype = 
  log: (string) ->
    if @options.log?
      console.log string
  
  framework: (selector) ->
    dom_elements = document.querySelectorAll(selector)
    dom_elements = Array::slice.call(dom_elements)
    if dom_elements.length > 1
      console.error "WARNING: There are more elements with this selector query! Using the first one." if console?
    dom_elements[0]

  canvas_supported: ->
    element = @create_canvas()
    not not (element.getContext('2d'))

  draw_canvas: ->
    @log "Draw frame " + @current_frame
    frame = @get_frame(@current_frame)
    if frame isnt null
      if @current_frame is 0 # First frame
        @buffer_context.drawImage(@image, 0, 0, @options.width, @options.height, 0, 0, @options.width, @options.height)
      else
        for diff in frame.diff
          @log diff
          destiny_x = diff[0]
          destiny_y = diff[1]
          source_x = diff[2]
          source_y = diff[3]
          width = diff[4]
          height = diff[5]
          @buffer_context.clearRect destiny_x, destiny_y, width, height
          #@buffer_context.clearRect 0, 0, @options.width, @options.height
          @buffer_context.drawImage(@image, source_x, source_y, width, height, destiny_x, destiny_y, width, height)
      @dom_context.clearRect 0, 0, @options.width, @options.height
      @dom_context.drawImage @buffer_element, 0, 0

  draw_fallback: ->
    @log "Draw frame " + @current_frame
    frame = @get_frame(@current_frame)
    if frame isnt null
      if @current_frame is 0 # First frame
        element = @create_div()
      else
        for diff in frame.diff
          @log diff
          destiny_x = diff[0]
          destiny_y = diff[1]
          source_x = diff[2]
          source_y = diff[3]
          width = diff[4]
          height = diff[5]
          element = @create_div source_x, source_y, destiny_x, destiny_y, width, height
          if width is @options.width and height is @options.height
            element.style.className = 'full-sized-frame'
      @dom_layer.appendChild element

  get_frame: (number) ->
    if @options.frames[number]?
      return @options.frames[number]
    else
      return null

  draw: ->
    frame = @get_frame @current_frame
    if frame isnt null
      timeout = @options.timeout
      timeout = timeout*frame.jump if frame.jump?
      @log "Frame: #{@current_frame} with timeout: #{timeout}"
      @timeout_id = setTimeout(=>
        @draw()
      , timeout)
      if @use_canvas
        @draw_canvas()
      else
        @draw_fallback()
      @current_frame++

  play: ->
    if @image_loaded
      @draw()
    else
      console.error "[Image is not loaded! (is probably loading...)]"

  pause: ->
    clearTimeout @timeout_id

  stop: ->
    @pause()
    @current_frame = 0
    @draw_canvas() if @use_canvas

  create_canvas: ->
    document.createElement 'canvas'

  create_div: (source_x=0, source_y=0, destiny_x=0, destiny_y=0, width=@options.width, height=@options.height) ->
    layer = document.createElement 'div'
    layer.style.position = 'absolute'
    layer.style.left = "#{destiny_x}px"
    layer.style.top = "#{destiny_y}px"
    layer.style.backgroundImage = "url(#{@options.image})"
    #layer.style.backgroundAttachment = "fixed"
    #layer.style.backgroundPosition = "-#{source_x-width}px -#{source_y-height}px"
    layer.style.backgroundPosition = "-#{source_x}px -#{source_y}px"
    layer.style.width = "#{width}px"
    layer.style.height = "#{height}px"
    layer.style.zIndex = @current_frame
    layer

  start_canvas: ->
    # DOM
    @dom_canvas = @create_canvas()
    @dom_canvas.width = @options.width
    @dom_canvas.height = @options.height
    @dom_context = @dom_canvas.getContext '2d'
    @dom.appendChild @dom_canvas

    # BUFFERING
    @buffer_element = @create_canvas()
    @buffer_element.width = @options.width
    @buffer_element.height = @options.height
    @buffer_context = @buffer_element.getContext '2d'

    # TODO Double buffer @next_frame_buffer = document.createElement 'canvas'

  start_fallback: ->
    @dom_layer = @create_div()
    @dom_layer.style.position = 'relative'
    @dom_layer.className = 'uvepe8-fallback'
    @dom.appendChild @dom_layer

  init: (dom_object, animation, autostart=true) ->
    @options = animation if animation?
    @options.dom = dom_object if dom_object?
    @use_canvas = @canvas_supported()
    @dom = @framework(@options.dom)
    @options.timeout = (1000/@options.fps)
    @image = new Image()
    @image.src = @options.image
    @dom.style.width = @options.width
    @dom.style.height = @options.height
    if @use_canvas
      # Canvas support!
      @start_canvas()
    else
      # TODO Fallback support
      @start_fallback()
    @image.onload = =>
      @image_loaded = true
      @stop() # Drawing first frame
      @play() if autostart
    @

window.uvepe8 = uvepe8
