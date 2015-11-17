import sublime, sublime_plugin
import os, subprocess, sys

'''

'''
class Utility:
    @staticmethod
    def filematch(filenetry, names):
        (d, f) = filenetry
        for n in names:
            filepath = os.path.join(d, f).upper()
            if filepath.find(n) < 0:
                return False
        return True

    @staticmethod
    def progOpenfile(filepath):
        if sys.platform.startswith('darwin'):
            subprocess.call(('open', filepath))
        elif os.name == 'nt':
            os.startfile(filepath)
        elif os.name == 'posix':
            subprocess.call(('xdg-open', filepath))

    @staticmethod
    def openfile(filepath):
        binfiles = SettingSingleton.getInstance().get("binary_files")
        for ext in binfiles:
            extstr = '.' + ext
            if filepath[ - len(extstr):] == extstr:
                Utility.progOpenfile(filepath)
                return
        sublime.active_window().open_file(filepath)

'''
should load lazily or load on plugin reload. Got problem if directly load
on class initialization.
'''
class SettingSingleton:
    settings = None

    @staticmethod
    def getInstance():
        if SettingSingleton.settings == None:
            SettingSingleton.settings = sublime.load_settings('FileFinder.sublime-settings')
        return SettingSingleton.settings

class Filefinder:
    def __init__(self):
        self.incdirs = SettingSingleton.getInstance().get("include_dirs")
        if self.incdirs == None:
            self.incdirs = []
        self.filelist=[]

    def initFileList(self):
        self.filelist = []
        for root in self.incdirs:
            home = os.getenv('HOME')
            if home != None:
                root = root.replace('~', home)
            for curdir, sondirs, sonfiles in os.walk(root):
                for f in sonfiles:
                    self.filelist.append( (curdir, f) )
        self.found = self.filelist

    def searchFile(self, input):
        names = input.upper().split(' ')
        lastdir=''
        self.found = []
        for (d, f) in self.filelist:
            if Utility.filematch((d, f), names):
                if d != lastdir:
                    lastdir = d
                self.found.append(os.path.join(d, f))
        return
    def getFound(self):
        return self.found
    def getCount(self):
        if len(self.incdirs) == 0:
            raise Exception("Please configure include_dirs in settings!")
        return len(self.found)
'''
should load lazily or load on plugin reload. Got problem if directly load
on class initialization.
'''
class FilefinderSingleton:
    filefinder = None

    @staticmethod
    def getInstance():
        if FilefinderSingleton.filefinder == None:
            FilefinderSingleton.filefinder = Filefinder()
        return FilefinderSingleton.filefinder

class FilefinderCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        FilefinderSingleton.getInstance().initFileList()
        self.updateFileCount()
        self.v = self.view.window().show_input_panel("file search phrases:",'', self.on_done,
            self.on_change, self.on_cancel)
    def updateFileCount(self):
        try:
            sublime.status_message("matching files:%d" % FilefinderSingleton.getInstance().getCount())
        except Exception as err:
            sublime.status_message(str(err))
    def on_done(self, user_input):
        self.view.window().show_quick_panel(FilefinderSingleton.getInstance().found,
            self.on_select_done, sublime.MONOSPACE_FONT, )
    def on_change(self, user_input):
        FilefinderSingleton.getInstance().searchFile(user_input)
        self.updateFileCount()
    def on_cancel(self):
        sublime.status_message("User cancel ")
    def on_select_done(self, sel):
        filepath = FilefinderSingleton.getInstance().getFound()[sel]
        sublime.status_message("open: %s" % filepath)
        Utility.openfile(filepath)
