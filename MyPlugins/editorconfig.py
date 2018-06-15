import sublime
import sublime_plugin
import os.path

print('asdfasdf')

# def apply_config(view):
#     pass


class EditorConfigEventListener(sublime_plugin.EventListener):
    def on_load(self, view):
        print('on_load', view)
        # if not view.settings().has('editconfig'):
            # apply_config(view)

    def on_activated(self, view):
        print('on_activated', view)
        # if not view.settings().has('editconfig'):
            # apply_config(view)
