import sublime
import sublime_plugin

from .editorconfig import get_properties, EditorConfigError

LINE_ENDINGS = {
    'lf': 'unix',
    'crlf': 'windows',
    'cr': 'cr'
}

CHARSETS = {
    'latin1': 'western (iso 8859-1)',
    'utf-8': 'utf-8',
    'utf-8-bom': 'utf-8 with bom',
    'utf-16be': 'utf-16 be',
    'utf-16le': 'utf-16 le'
}


def apply_config(view):
    file_name = view.file_name();
    # print('view', file_name)
    if not file_name:
        return

    # TODO: 检查配置文件是否改变
    try:
        config = get_properties(file_name)
    except EditorConfigError:
        sublime.status_message('.editorconfig format error')
    else:
        sublime.status_message('.editorconfig detected')

        indent_size = config.get('indent_size')
        tab_width = config.get('tab_width')
        indent_style = config.get('indent_style')
        charset = config.get('charset')
        end_of_line = config.get('end_of_line')
        insert_final_newline = config.get('insert_final_newline')
        trim_trailing_whitespace = config.get('trim_trailing_whitespace')
        max_line_length = config.get('max_line_length')

        # 根据 detect_indentation 的结果来判断
        if not view.settings().get('detect_indentation'):
            view.run_command('detect_indentation', {'show_message': False})

        if indent_size:
            if indent_size == 'tab':
                if tab_width and view.settings().get('tab_size') != int(tab_width):
                    print('*tab_size:', view.settings().get('tab_size'), tab_width)
                    view.run_command('set_setting', {"setting": "tab_size", "value": int(tab_width)})
            elif view.settings().get('tab_size') != int(indent_size):
                print('*tab_size:', view.settings().get('tab_size'), indent_size)
                view.run_command('set_setting', {"setting": "tab_size", "value": int(indent_size)})

        if indent_style == 'space':
            if view.settings().get('translate_tabs_to_spaces') == False:
                print('*indent_style:space')
                view.run_command('expand_tabs', {'set_translate_tabs': True})
                view.run_command('set_setting', {"setting": "translate_tabs_to_spaces", "value": True})
                view.settings().set('translate_tabs_to_spaces', True)
        elif indent_style == 'tab':
            if view.settings().get('translate_tabs_to_spaces') == True:
                print('*indent_style:tab')
                view.run_command('unexpand_tabs', {'set_translate_tabs': True})
                view.run_command('set_setting', {"setting": "translate_tabs_to_spaces", "value": False})
                view.settings().set('translate_tabs_to_spaces', False)

        if charset in CHARSETS:
            if view.encoding() == 'Undefined':
                view.settings().set('default_encoding', CHARSETS[charset])
            elif view.encoding().lower() != CHARSETS[charset]:
                print('*charset', view.encoding(), CHARSETS[charset])
                # TODO: 转换编码
                view.set_encoding(CHARSETS[charset])
                view.settings().set('default_encoding', CHARSETS[charset])

        if end_of_line in LINE_ENDINGS:
            if view.line_endings().lower() != LINE_ENDINGS[end_of_line]:
                print('*line_endings', view.line_endings(), LINE_ENDINGS[end_of_line])
                view.set_line_endings(LINE_ENDINGS[end_of_line])

        if insert_final_newline == 'true':
            view.settings().set('ensure_newline_at_eof_on_save', True)
        elif insert_final_newline == 'false':
            view.settings().set('ensure_newline_at_eof_on_save', False)

        if trim_trailing_whitespace == 'true':
            view.settings().set('trim_trailing_white_space_on_save', True)
        elif trim_trailing_whitespace == 'false':
            view.settings().set('trim_trailing_white_space_on_save', False)

        if max_line_length == 'off':
            view.settings().set('rulers', [])
        elif max_line_length:
            view.settings().set('rulers', [int(max_line_length)])

class EditorConfigEventListener(sublime_plugin.EventListener):
    def on_load(self, view):
        # print('on_load', view)
        # if not view.settings().has('editconfig'):
        apply_config(view)

    def on_activated(self, view):
        # print('on_activated', view)
        # if not view.settings().has('editconfig'):
        apply_config(view)

    def on_pre_save(self, view):
        pass
