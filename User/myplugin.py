import sublime
import sublime_plugin


def on_done(index):
    print('on_done', index)

def on_highlighted(index):
    print('on_highlighted', index)

items = ['none']

def on_change(index, window):
    print('on_changed', index)
    items.append(index)
    window.show_quick_panel(items, on_done, 0, 0, on_highlighted)


class ExampleCommand(sublime_plugin.WindowCommand):
    def __init__(self, window):
        sublime_plugin.WindowCommand.__init__(self, window)

    def run(self):
        print('1212122')
        # self.view.insert(edit, 0, "Hello, World!")
        self.window.show_input_panel('caption', 'initial_text', on_done, lambda x: on_change(x, self.window), None)
        # self.window.show_quick_panel(['item0', 'item1', 'item2'], on_done, 
        #     sublime.KEEP_OPEN_ON_FOCUS_LOST, 0, on_highlighted)

