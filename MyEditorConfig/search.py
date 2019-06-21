import sublime
import sublime_plugin


class ScopeInputHandler(sublime_plugin.TextInputHandler):
    def __init__(self, view):
        self.view = view

    def placeholder(self):
        return "Scope"

    def initial_text(self):
        return ''

    def preview(self, text):
        # print('preview', text)
        if len(text):
            self.view.add_regions('search_scope',
                self.view.find_by_selector(text),
                'whitish',
                flags = sublime.DRAW_NO_FILL)

    def cancel(self):
        self.view.erase_regions('search_scope')

    def confirm(self, text):
        self.view.erase_regions('search_scope')

class SearchScopeCommand(sublime_plugin.WindowCommand):
    def run(self, scope):
        # print('SearchScopeCommand')
        view = self.window.active_view()

    def input(self, args):
        # print('input', args)
        return ScopeInputHandler(self.window.active_view())
