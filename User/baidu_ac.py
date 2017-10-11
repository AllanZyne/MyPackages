import sublime, sublime_plugin

from collections import deque

Copy_buffer = deque(maxlen=5)

def on_done(view, edit, i):
    if i < 0:
        return
    for pos in view.sel():
        view.insert(edit, pos.begin(), Copy_buffer[i])

class PasteTextMenuCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # print(Copy_buffer)
        self.view.show_popup_menu(Copy_buffer, lambda i: on_done(self.view, edit, i))

class TestEventListen(sublime_plugin.EventListener):
    
    def on_query_completions(self, view, prefix, locations):
        pass
        # print('query', prefix)

    def on_text_command(self, view, command_name, args):
        # print(command_name, args)
        if command_name == 'copy' or command_name == 'cut':
            pass
            # for sel in view.sel():
            #     text = view.substr(sel)
            #     Copy_buffer.append(text)
            # textContent = view.substr(sublime.Region(0, view.size()))
            # print(textContent)
            # rs = view.find_all(r'\w+')
            # print(rs)
            # view.add_regions('key', rs, 'string.quoted.single.python', '', sublime.DRAW_NO_OUTLINE | sublime.DRAW_NO_FILL)

    def on_hover(self, view, point, hover_zone):
        pass
        # print('on_hover', point)
        # scopeName = view.scope_name(point)
        # print(scopeName.split())
        # scopeRagion = view.extract_scope(point)
        # scopeText = view.substr(scopeRagion)
        # view.show_popup_menu(scopeName.split(), on_done)
        
        # html = '<b>{0}</b><br>{1}'.format(scopeText, scopeName)

        # view.show_popup(html, sublime.HIDE_ON_MOUSE_MOVE)
        # ph = sublime.Phantom(scopeRagion, 
        #   '{0}<br>{1}'.format(scopeText, scopeName), 
        #   sublime.LAYOUT_BELOW)

        # phs = sublime.PhantomSet(view)
        # phs.update([ph])

        # print(substr(view.word(point)))
        # pass
