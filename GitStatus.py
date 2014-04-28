import sublime, sublime_plugin
import subprocess, os

class EventListener(sublime_plugin.EventListener):

    def fire(self):
        GS = GitStatusCommand(sublime.active_window())
        GS.run()
    def on_clone(self, view):
        self.fire()
    def on_post_save(self, view):
        self.fire()
    def on_post_load(self, view):
        self.fire()
    def on_post_close(self, view):
        self.fire()
    def on_post_activated(self, view):
        self.fire()
    def on_post_deactivated(self, view):
        self.fire()

class GitStatusCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.check()

    def check(self):
        clean     = "nothing to commit, working directory clean"
        dirty     = "o changes added to commit"
        untracked = "nothing added to commit but untracked files present"
        notgit    = "ot a git repository"

        base_dir = self.window.folders()[0]
        os.chdir(base_dir)

        matches = subprocess.check_output(['git', 'status']).strip()
        matches = matches.decode('utf8', 'ignore').split("\n")
        status  = matches[-1]

        view = sublime.active_window().active_view()
        if clean in status:
            view.set_status('GitStatus', "Git: Clean")
        elif dirty in status:
            view.set_status('GitStatus', "Git: Dirty")
        elif untracked in status:
            view.set_status('GitStatus', "Git: Untracked")
        elif notgit in status:
            view.set_status('GitStatus', "Git: Not git")
        else:
            view.set_status('GitStatus', "Git: ?")

class Gitter():
    def all(self, window, ftype=None):
        self.window = window
        self.check(ftype)

    def check(self, ftype):
        self.items = []

        base_dir = self.window.folders()[0]
        os.chdir(base_dir)
        matches = subprocess.check_output(['git', 'ls-files', '-mdov', '--exclude-standard']).strip()
        matches = matches.decode('utf8', 'ignore').split("\n")
        for m in matches:
            if ftype:
                if ftype != m[0]:
                    continue

            change_type = self.get_type(m[0])
            fullpath = m[2:]
            # Split second part with directory separator and start getting
            parts = fullpath.split('/')
            file_name = parts[-1]

            parts.pop(-1)
            if len(parts) > 1:
                path = "/" + "/".join(parts) + "/"
            elif len(parts) == 1:
                path = "/" + parts[0]
            else:
                path = "/"


            self.items.append([file_name, change_type + path])

        self.window.show_quick_panel(self.items, self.selected, sublime.MONOSPACE_FONT, -1, self.highlight)

    def fopen(self, f):
        self.window.open_file(f, sublime.ENCODED_POSITION)
    def fpreview(self, f):
        self.window.open_file(f, sublime.TRANSIENT)

    def selected(self, index):
        item = self.items[index]
        fullpath = item[1] + item[0]
        parts = fullpath.split(': ')
        parts.pop(0)
        fullpath = "".join(parts)

        self.fopen(self.window.folders()[0] + fullpath)

    def highlight(self, index):
        item = self.items[index]
        fullpath = item[1] + item[0]
        parts = fullpath.split(': ')
        parts.pop(0)
        fullpath = "".join(parts)

        # Commented out as highlighting closes the quick input panel
        # So it's now doing nothing

        # self.fpreview(self.window.folders()[0] + fullpath)

    def get_type(self, ch):
        if ch == "C":
            return "Modified/Created: "
        elif ch == "R":
            return "Deleted: "
        elif ch == "H":
            return "Cached: "
        elif ch == "S":
            return "SkipWorktree: "
        elif ch == "M":
            return "Unmerged: "
        elif ch == "K":
            return "To be killed: "
        elif ch == "?":
            return "Unstaged: "
        else:
            return ch

class GitChangedCommand(sublime_plugin.WindowCommand):
    def run(self):
        G = Gitter()
        G.all(self.window)

class GitUnmergedCommand(sublime_plugin.WindowCommand):
    def run(self):
        G = Gitter()
        G.all(self.window, 'M')

