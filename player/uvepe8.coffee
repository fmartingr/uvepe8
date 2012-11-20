###
# UVEPE8 Player
# Author:       Felipe "Pyron" Martín (@fmartingr)
# Notes:		    See README
###

uvepe8 = (dom_object, animation, autostart) ->
  #options =
  #  dom: ""
  #  width: ""
  #  height: ""
  #  frames: ""
  #  image: ""
  #  fps: ""
  #  log

  if not (@ instanceof uvepe8)
    new uvepe8(dom_object, animation, autostart)
  else
    @init(dom_object, animation, autostart)

uvepe8.prototype = 
  log: (string) ->
    if @options.log?
      console.log string
  
  find_framework: ->
    if jQuery? or Zepto?
      @framework = $
    if not @framework?
      throw "[Can't found compatible framwork. Please include Zepto or jQuery.]"
    true

  canvas_supported: ->
    element = @create_canvas()
    not not (element.getContext('2d'))

  draw_canvas: ->
    empty_array = []
    @log "Draw frame " + @current_frame
    frame = @get_frame(@current_frame)
    if frame isnt null
      if @current_frame is 0 # First frame
        @buffer_context.drawImage(@image, 0, 0, @options.width, @options.height, 0, 0, @options.width, @options.height)
      else
        for diff in frame.diff
          @log diff
          source_x = diff[2]
          source_y = diff[3]
          width = diff[4]
          height = diff[5]
          destiny_x = diff[0]
          destiny_y = diff[1]
          @buffer_context.clearRect destiny_x, destiny_y, width, height
          @buffer_context.drawImage(@image, source_x, source_y, width, height, destiny_x, destiny_y, width, height)
      @dom_context.clearRect 0, 0, @options.width, @options.height
      @dom_context.drawImage @buffer_element, 0, 0

  draw_fallback: ->
    @log 'fallback'

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
      setTimeout(=>
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

  create_canvas: ->
    document.createElement 'canvas'

  start_canvas: ->
    # DOM
    @dom_canvas = @create_canvas()
    @dom_canvas.width = @options.width
    @dom_canvas.height = @options.height
    @dom_context = @dom_canvas.getContext '2d'
    @dom.append(@dom_canvas)

    # BUFFERING
    @buffer_element = @create_canvas()
    @buffer_element.width = @options.width
    @buffer_element.height = @options.height
    @buffer_context = @buffer_element.getContext '2d'

  start_fallback: ->
    throw "[Sorry. Fallback is not implemented yet. Use a canvas compatible browser.]"

    #@next_frame_buffer = document.createElement 'canvas' TODO

  init: (dom_object, animation, autostart=true) ->
    @options = animation if animation?
    @options.dom = dom_object if dom_object?
    if @find_framework()
      @use_canvas = @canvas_supported()
      @current_frame = 0
      @dom = @framework(@options.dom)
      @options.timeout = (1000/@options.fps)
      if @use_canvas
        # Canvas support!
        @image = new Image()
        @image.src = @options.image
        @dom.css
          width: @options.width
          height: @options.height
        @start_canvas()
        @image.onload = =>
          @image_loaded = true
          @play() if autostart
      else
        # Fallback support TODO
        @start_fallback()

    @

window.uvepe8 = uvepe8