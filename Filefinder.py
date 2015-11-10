import sublime, sublime_plugin

class FilefinderCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.v = self.view.window().show_input_panel("file search phrases:", '', self.on_done, self.on_change, self.on_cancel)
    def on_done(self, user_input):
        ll = []
        for i in range(len(user_input)):
            ll.append(user_input)
        self.view.window().show_quick_panel(ll, self.on_select_done, sublime.MONOSPACE_FONT, )
    def on_change(self, user_input):
        sublime.status_message("matching files:%d" % len(user_input))
    def on_cancel(self, user_input):
        sublime.status_message("User said: " + user_input)
    def on_select_done(self, sel):
        sublime.status_message("User select file to open: %d" % sel)

'''
# may alert all, no use
class KeyBindingListener(sublime_plugin.EventListener):
    def on_modified(self, view):
        #if view.name() != 'fucker':
        #    return
        print("The on_modified event fired!" + view.name())
'''
