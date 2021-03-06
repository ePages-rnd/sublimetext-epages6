import argparse
from distutils.version import LooseVersion
import os
import paramiko
import re
import shutil
import shlex


class ep6tools:
    def __init__(self, vm, user, password):
        self.vm = vm
        self.client = None

        if vm != None:
            try:
                self.client = paramiko.SSHClient()
                self.client.load_system_host_keys()
                self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

                self.client.connect(self.vm, username=user, password=password, timeout=1.0)

            except Exception as e:
                print('Error: ' + str(e))


    def execute(self, command):
        if self.vm != None:
            try:
               stdin, stdout, stderr = self.client.exec_command(command)
               stdin.close()

               for line in stdout:
                    print(line.strip('\n'))

               for line in stderr:
                    print(line.strip('\n'))

            except Exception as e:
                print('Error: ' + str(e))

    def execute_with_file(self, command, file):
        self.execute(command + ' "{}"'.format(self.get_vm_file_path(file)))

    def restart(self):
        self.execute('ep6-restart')

    def restart_all(self):
        self.execute('ep6-restart-all')

    def perm_all(self):
        self.execute('ep6-perm-all')

    def perm_cartridges(self):
        self.execute('ep6-perm-cartridges')

    def perm_webroot(self):
        self.execute('ep6-perm-webroot')

    def import_xml(self, file):
        self.execute_with_file('ep6-import-xml', file)

    def import_hook(self, file):
        self.execute_with_file('ep6-import-hook', file)

    def delete_xml(self, file):
        self.execute_with_file('ep6-delete-xml', file)

    def delete_hook(self, file):
        self.execute_with_file('ep6-delete-hook', file)

    def lint(self, file, lint_mode, lint_option):
        file = file.replace("\\", "/")

        if lint_mode == None:
            file_name, lint_mode = os.path.splitext(file)
            lint_mode = lint_mode.replace('.', '').lower()

        if lint_mode == 'html':
            self.execute("ep6-tlec < " + self.get_vm_file_path(file))
            return

        if lint_mode in ['pm', 'pl', 't']:
            if lint_option in ['critic', 'perlcritic']:
                self.execute_with_file('ep6-perlcritic', file)
            else:
                self.execute_with_file('ep6-perlc', file)

    def tidy(self, file, tidy_option):
        file = file.replace("\\", "/")

        if tidy_option in ['organize-imports']:
            self.execute_with_file('ep6-organize-imports', file)

    def copy_to_shared(self, file, storetypes):
        if os.path.exists(storetypes):
            shared_file = None;
            file = file.replace("\\", "/")
            m = re.compile(r".*Cartridges.*Data/Public(.*)$").match(file)
            if m:
                shared_file = self.store(storetypes) + "/Store" + m.group(1)

            # Dojo javascript needs Shrinksafe.pm to be build
            # m = re.compile(r".*Cartridges/(.*)/Data/javascript(.*)$").match(file)
            # if m:
            #     shared_file = self.store(storetypes) + "/Store/javascript/epages/cartridges/" + m.group(1).lower() + m.group(2)
            if shared_file is not None:
                file = os.path.normpath(file)
                shared_file = os.path.normpath(shared_file)

                print('copy ' + file + ' to ' + shared_file)

                shutil.copyfile(file, shared_file)
        else:
            print('StoreTypes folder not found: ' + storetypes)

    def store(self, path_to_storetypes):
        # /Users/emueller/VM-Mounts/emueller-vm-1/Shared/WebRoot/StoreTypes/6.15.2/Store/lib/package-bo.js
        storetypes = os.listdir(path_to_storetypes)
        storetypes = list(filter(lambda x: re.search(r'^\d\..*', x), storetypes))
        storetypes.sort(key=LooseVersion)
        return path_to_storetypes + '/' + storetypes[-1]

    def set_debug_level(self, debug_level):
        self.execute('ep6-set-debug-level {}'.format(debug_level))

    def get_log(self, logpath, log):
        print('{}/{}.log'.format(logpath, log))

    def get_file_from_vm_path(self, vm_file, cartridges):
        m = re.compile(r".*\/Cartridges(\/.+)$").match(vm_file)
        if m:
            print(cartridges + m.group(1))

    def get_vm_file_path(self, file):
        m = re.compile(r".*\/(Cartridges\/.+)$").match(file.replace('\\','/'))
        if m:
            return "/srv/epages/eproot/" + m.group(1)

def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("--vm")
    parser.add_argument("--user")
    parser.add_argument("--password")
    parser.add_argument("--file")
    parser.add_argument("--storetypes")
    parser.add_argument("--cartridges")
    parser.add_argument("--log")

    parser.add_argument("--restart", action='store_const', const=True)
    parser.add_argument("--restart-all", action='store_const', const=True)

    parser.add_argument("--perm-all", action='store_const', const=True)
    parser.add_argument("--perm-cartridges", action='store_const', const=True)
    parser.add_argument("--perm-webroot", action='store_const', const=True)

    parser.add_argument("--import-xml", action='store_const', const=True)
    parser.add_argument("--import-hook", action='store_const', const=True)
    parser.add_argument("--delete-xml", action='store_const', const=True)
    parser.add_argument("--delete-hook", action='store_const', const=True)

    parser.add_argument("--lint", action='store_const', const=True)
    parser.add_argument("--lint-mode")
    parser.add_argument("--lint-option")

    parser.add_argument("--tidy", action='store_const', const=True)
    parser.add_argument("--tidy-option")

    parser.add_argument("--copy-to-shared", action='store_const', const=True)

    parser.add_argument("--set-debug-level")

    parser.add_argument("--get-log")
    parser.add_argument("--get-file-from-vm-path")

    parser.add_argument("--ignore-me")

    return parser.parse_args()


args = parse_arguments()
ep6tool = ep6tools(args.vm, args.user, args.password)

if args.restart:
    ep6tool.restart()

if args.restart_all:
    ep6tool.restart_all()

if args.perm_all:
    ep6tool.perm_all()

if args.perm_cartridges:
    ep6tool.perm_cartridges()

if args.perm_webroot:
    ep6tool.perm_webroot()

if args.import_xml:
    ep6tool.import_xml(args.file)

if args.import_hook:
    ep6tool.import_hook(args.file)

if args.delete_xml:
    ep6tool.delete_xml(args.file)

if args.delete_hook:
    ep6tool.delete_hook(args.file)

if args.lint:
    ep6tool.lint(args.file, args.lint_mode, args.lint_option)

if args.tidy:
    ep6tool.tidy(args.file, args.tidy_option)

if args.copy_to_shared:
    ep6tool.copy_to_shared(args.file, args.storetypes)

if args.set_debug_level:
    ep6tool.set_debug_level(args.set_debug_level)

if args.get_log:
    ep6tool.get_log(args.log, args.get_log)

if args.get_file_from_vm_path:
    ep6tool.get_file_from_vm_path(args.get_file_from_vm_path, args.cartridges)
