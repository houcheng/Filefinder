import sublime, sublime_plugin
import os

class Utility:
    def filematch(filenetry, names):
        (d, f) = filenetry
        for n in names:
            filepath = os.path.join(d, f).upper()
            if filepath.find(n) < 0:
                return False
        return True
    def openfile(filepath):
        sublime.active_window().open_file(filepath)

class Filefinder:
    def __init__(self):
        '''
        Hard coded config
        '''
        self.incdir=['~/Dropbox/1Reading', '~/Dropbox/2Writing', '~/Dropbox/ItriProjects', '~/Dropbox/ITRI']
        self.filelist=[]

    def initFileList(self):
        self.filelist = []
        for root in self.incdir:
            home = os.getenv('HOME')
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
        return len(self.found)

class FilefinderSingleton:
    filefinder = Filefinder()
    def getInstance():
        return FilefinderSingleton.filefinder

class FilefinderCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.v = self.view.window().show_input_panel("file search phrases:",'', self.on_done,
            self.on_change, self.on_cancel)
        FilefinderSingleton.getInstance().initFileList()
        self.updateFileCount()
    def updateFileCount(self):
        l = len( FilefinderSingleton.getInstance().found)
        sublime.status_message("matching files:%d" % l)
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
