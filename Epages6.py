import sublime, sublime_plugin
import subprocess
import re

ep6_settings = sublime.load_settings('Epages6.sublime-settings')

def ep6tools(view, tool, quote = False):
    cmd = ['perl']
    path = ep6_settings.get('path')

    if quote: path = '"' + path + '"'

    cmd.append(path)

    if ep6_settings.get('verbose'):
        cmd.append('--verbose')

    if view.settings().get('ep6_vm'):
        cmd.append('--vm=' + view.settings().get('ep6_vm'))

    cmd.extend(tool)
    cmd.append(view.file_name())

    return cmd

def execute(cmd):
    # TODO: maybe use sys.stdout.encoding instead of utf-8
    return subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE).communicate()[0].decode('utf-8').strip()

class Epages6EventListener(sublime_plugin.EventListener):
    def on_post_save_async(self, view):
        if (ep6_settings.get('copy_to_shared')):
            view.window().run_command('ep6_tools', {'tool': ['--copy-to-shared'], 'shell': True})

class Ep6ToolsCommand(sublime_plugin.WindowCommand):
    def run(self, tool = '', shell = False):
        cmd = ep6tools(self.window.active_view(), tool)

        if shell:
            print(execute(' '.join(cmd)))
        else:
            self.window.run_command('exec', {'cmd': cmd})

class ReopenCurrentFileCommand(sublime_plugin.WindowCommand):
    def run(self):
        current_view = self.window.active_view()
        current_view.run_command('reopen', {'encoding': current_view.encoding()})

class OpenFileFromVmPathCommand(sublime_plugin.WindowCommand):
    def run(self):
        # example:
        # <!-- END INCLUDE /srv/epages/eproot/Cartridges/DE_EPAGES/ShopCSVExportImport/Templates/MBO/MBO.INC-CSVExportImportTabPage.Script.html -->
        # or:
        # Use of uninitialized value in string ne at /srv/epages/eproot/Cartridges/DE_EPAGES/Amazon/UI/AmazonOffer.pm line 125.
        clipboard = sublime.get_clipboard()
        line = 0

        # is there a "line = $line_number" ?
        line_regex = re.compile(r"^.*line (\d+).*$").match(clipboard)
        if line_regex:
            line = int(line_regex.group(1))

        m = re.compile(r"^.*\s(\/.*?)\s.*$").match(clipboard)
        if m:
            if line > 0:
                path = execute(' '.join(ep6tools(self.window.active_view(), ['--get-file-from-vm-path=' + m.group(1) + ':' + str(line)], True)))
                self.window.open_file(path, sublime.ENCODED_POSITION)
            else:
                path = execute(' '.join(ep6tools(self.window.active_view(), ['--get-file-from-vm-path=' + m.group(1)], True)))
                self.window.open_file(path)


class OpenLogCommand(sublime_plugin.WindowCommand):
    def run(self, log):
        path = execute(' '.join(ep6tools(self.window.active_view(), ['--get-log=' + log], True)))
        self.window.open_file(path)
