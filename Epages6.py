import sublime, sublime_plugin
import subprocess
import re

ep6_settings = sublime.load_settings('Epages6.sublime-settings')

def ep6tools(view, tool):
    cmd = ['perl', ep6_settings.get('path')]

    if ep6_settings.get('verbose'):
        cmd.append('--verbose')

    if view.settings().get('ep6_vm'):
        cmd.append('--vm=' + view.settings().get('ep6_vm'))

    cmd.extend(tool)
    cmd.append(view.file_name())

    return cmd


class Epages6EventListener(sublime_plugin.EventListener):
    def on_post_save_async(self, view):
        if (ep6_settings.get('copy_to_shared')):
            view.window().run_command('ep6_tools', {'tool': ['--copy-to-shared'], 'shell': True})

class Ep6ToolsCommand(sublime_plugin.WindowCommand):
    def run(self, tool = '', shell = False):
        cmd = ep6tools(self.window.active_view(), tool)

        if shell:
            (status, output) = subprocess.getstatusoutput(' '.join(cmd))
            if status == 0:
                print(output)
        else:
            self.window.run_command('exec', {'cmd': cmd})

class ReopenCurrentFileCommand(sublime_plugin.WindowCommand):
    def run(self):
        current_view = self.window.active_view()
        current_view.run_command('reopen', {'encoding': current_view.encoding()})

class OpenFileFromVmPathCommand(sublime_plugin.WindowCommand):
    def run(self):
        vm_path = sublime.get_clipboard()
        m = re.compile(r"^.*INCLUDE\s(.*?)\s.*$").match(vm_path)
        if m:
            # print(m.group(1))
            path = subprocess.getoutput(' '.join(ep6tools(self.window.active_view(), ['--get-file-from-vm-path=' + m.group(1)])))
            # print(path)
            self.window.open_file(path)




