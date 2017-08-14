﻿# Copyright 2004-2017 Tom Rothamel <pytom@bishoujo.us>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

init -1500 python:

    # basics: If not None, the default value of the fullscreen
    # preference when the game is first run.
    config.default_fullscreen = None

    # basics: If not None, the default value of the text_cps
    # preference when the game is first run.
    config.default_text_cps = None

    # If not None, the default value of afm_time
    config.default_afm_time = None

    # If not None, the default value of afm_enable
    config.default_afm_enable = False

    # If not None, the default language to use.
    config.default_language = None

    # If not None, the default value of wait_voice
    config.default_wait_for_voice = True

    # If not None, the default value of voice_sustain
    config.default_voice_sustain = False

    # If not None, the default value of mouse_move.
    config.default_mouse_move = True

    # If not None, the default value of show_empty_window.
    config.default_show_empty_window = True

    # If not None, the default value of emphasize_audio.
    config.default_emphasize_audio = False

    # If not None, the default value of set_volume (music)
    config.default_music_volume = 1.0

    # If not None, the default value of set_volume (sfx)
    config.default_sfx_volume = 1.0

    # If not None, the default value of set_volume (voice)
    config.default_voice_volume = 1.0

init 1500 python hide:

    if not persistent._set_preferences:
        persistent._set_preferences = True

        if config.default_fullscreen is not None:
            _preferences.fullscreen = config.default_fullscreen

        if config.default_text_cps is not None:
            _preferences.text_cps = config.default_text_cps

        if config.default_afm_time is not None:
            _preferences.afm_time = config.default_afm_time

        if config.default_language is not None:
            _preferences.language = config.default_language

        if config.default_wait_for_voice is not None:
            _preferences.wait_voice = config.default_wait_for_voice

        if config.default_voice_sustain is not None:
            _preferences.voice_sustain = config.default_voice_sustain

        if config.default_mouse_move is not None:
            _preferences.mouse_move = config.default_mouse_move

        if config.default_afm_enable is not None:
            _preferences.afm_enable = config.default_afm_enable

        if config.default_show_empty_window is not None:
            _preferences.show_empty_window = config.default_show_empty_window

        if config.default_emphasize_audio is not None:
            _preferences.emphasize_audio = config.default_emphasize_audio

        _preferences.set_volume('music', config.default_music_volume)
        _preferences.set_volume('sfx', config.default_sfx_volume)
        _preferences.set_volume('voice', config.default_voice_volume)

    # Use default_afm_enable to decide if we use the afm_enable
    # preference.
    if config.default_afm_enable is not None:
        _preferences.using_afm_enable = True
    else:
        _preferences.afm_enable = True
        _preferences.using_afm_enable = False

    error = _preferences.check()

    if error:
        raise Exception(error)

init -1500 python:
    def _imagemap_auto_function(auto_param, variant):
        rv = auto_param % variant

        if renpy.image_exists(rv):
            return rv
        elif renpy.loadable(rv):
            return rv
        else:
            return None

    config.imagemap_auto_function = _imagemap_auto_function

init -1500 python:

    config.hyperlink_protocol = "call_in_new_context"

    # Hyperlink functions. Duplicated in _errorhandling.rpym.
    def hyperlink_styler(target):
        return style.hyperlink_text

    def hyperlink_function(target):

        if ":" not in target:
            target = config.hyperlink_protocol + ":" + target

        if target.startswith("jump:"):
            renpy.jump(target[5:])
        elif target.startswith("call:"):
            renpy.call(target[5:])
        elif target.startwith("call_in_new_context:"):
            renpy.call_in_new_context[20:]
        else:
            try:
                import webbrowser
                webbrowser.open(target)
            except:
                pass

    style.default.hyperlink_functions = (hyperlink_styler, hyperlink_function, None)

init -1500:
    image text = renpy.ParameterizedText(style="centered_text")
    image vtext = renpy.ParameterizedText(style="centered_vtext")

