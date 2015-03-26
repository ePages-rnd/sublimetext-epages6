import sublime, sublime_plugin

import os
import re
import subprocess
import sys

def ep6tools(view, tool, quote = False):
    if view.settings().get('ep6vm'):
        settings = view.settings().get('ep6vm');

        cmd = ['python3']

        path = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/') + '/ep6-tools.py'
        cmd.append(path)

        cmd.append('--vm')
        cmd.append(settings['vm'])

        cmd.append('--user')
        cmd.append(settings['user'])

        cmd.append('--password')
        cmd.append(settings['password'])

        cmd.append('--storetypes')
        cmd.append(settings['storetypes'])

        cmd.append('--cartridges')
        cmd.append(settings['cartridges'])

        cmd.append('--log')
        cmd.append(settings['log'])

        cmd.append('--file')
        cmd.append(view.file_name())

        cmd.extend(tool)

        return cmd

    else:
        sys.exit('Error: No epages6 virtual machine settings found!')

def execute(cmd):
    # TODO: maybe use sys.stdout.encoding instead of utf-8
    return subprocess.Popen(cmd,  shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE).communicate()

class Epages6EventListener(sublime_plugin.EventListener):
    def on_post_save_async(self, view):
        if view.settings().get('ep6vm') and view.settings().get('ep6vm')['copy_to_shared']:
            file_name = view.file_name()
            file_name, file_ext = os.path.splitext(file_name)
            file_ext = file_ext.replace('.', '').lower()
            if file_ext in ['js', 'css', 'less', 'html']:
                view.window().run_command('ep6_tools', {'tool': ['--copy-to-shared'], 'shell': True})

class Ep6ToolsCommand(sublime_plugin.WindowCommand):
    def run(self, tool = '', shell = False):
        cmd = ep6tools(self.window.active_view(), tool)

        print('[Started, please wait ...]')

        if shell:
            result = execute(cmd)
            print(result[0].decode('utf-8').strip())
            print(result[1].decode('utf-8').strip())
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
                path = execute(ep6tools(self.window.active_view(), ['--get-file-from-vm-path', m.group(1) + ':' + str(line)], True))[0].decode('utf-8').strip()
                self.window.open_file(path, sublime.ENCODED_POSITION)
            else:
                path = execute(ep6tools(self.window.active_view(), ['--get-file-from-vm-path', m.group(1)], True))[0].decode('utf-8').strip()
                self.window.open_file(path)

class OpenLogCommand(sublime_plugin.WindowCommand):
    def run(self, log):
        path = execute(ep6tools(self.window.active_view(), ['--get-log', log], True))[0].decode('utf-8').strip()
        self.window.open_file(path)
