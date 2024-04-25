from darklock.singleton import Singleton
from darklock.log_disc_writer import LogDiscWriter
import builtins
import re
import os
import sys
import traceback


class RestrictOSAccess(metaclass=Singleton):
    def __init__(self):
        self.original_open = None
        self.original_import = None
        self.logging_importer = None
        self.original_os_write = None
        self.original_makedirs = None

        self.whitelisted_operations = [] # [('open', '/dev/null')]
        self.whitelisted_filenames = []
        self.whitelisted_imports = []
        self.blacklisted_filenames = []

    def restrict_os_write(self, *args, **kwargs):
        return self.original_os_write(*args, **kwargs)

    def restricted_open(self, *args, **kwargs):
        if ('open', args[0]) in self.whitelisted_operations or self.check_stack_trace():
            return self.original_open(*args, **kwargs)
        raise PermissionError("File system operations are not allowed")

    def restricted_os_makedirs(self, *args, **kwargs):
        if ('makedirs', args[0]) in self.whitelisted_operations or self.check_stack_trace():
            return self.original_makedirs(*args, **kwargs)
        #raise PermissionError("File system operations are not allowed")

    def restricted_open(self, *args, **kwargs):
        if ('open', args[0]) in self.whitelisted_operations or self.check_stack_trace():
            return self.original_open(*args, **kwargs)
        raise PermissionError("File system operations are not allowed")

    def restricted_exec(self, *args, **kwargs):
        raise PermissionError("System calls are not allowed")

    def restricted_subprocess(self, *args, **kwargs):
        raise PermissionError("Subprocess invocations are not allowed")

    def restricted_import(self, name, *args, **kwargs):
        if any(re.search(pattern, name) for pattern in self.whitelisted_imports):
            return self.original_import(name, *args, **kwargs)
        print(f"Failed to import: {name}")
        raise PermissionError("Importing modules is not allowed")

    def log_imports(self, name, *args, **kwargs):
        #self.logging_importer = LoggingImporter()
        sys.meta_path.insert(0, self.logging_importer)

    def restricted_module(self, *args, **kwargs):
        raise PermissionError("Module operations are not allowed")

    def restricted_os(self, *args, **kwargs):
        raise PermissionError("OS operations are not allowed")

    def restricted_sys(self, *args, **kwargs):
        raise PermissionError("System operations are not allowed")

    def restricted_socket(self, *args, **kwargs):
        raise PermissionError("Socket operations are not allowed")

    def check_stack_trace(self) -> bool:
        stack_trace = traceback.extract_stack()
        # Add more logic here to check the stack trace
        # and allow certain operations
        # from specific chains.
        res = False
        for frame in stack_trace:
            for name in self.whitelisted_filenames:
                if name in frame.filename:
                    res = True
            for name in self.blacklisted_filenames:
                if name in frame.filename:
                    res = False
        return res

    def log_writes(self):
        os.write = LogDiscWriter()

    def activate(
        self,
        whitelisted_operations: list = None,
        whitelisted_filenames: list = None,
        whitelisted_imports: list = None,
        blacklisted_filenames: list = None,
    ):
        """
        Install restrictions on OS access.
        :return:
        """
        self.whitelisted_operations = whitelisted_operations or []
        self.whitelisted_filenames = whitelisted_filenames or []
        self.whitelisted_imports = whitelisted_imports or []
        self.blacklisted_filenames = blacklisted_filenames or []

        self.original_open = builtins.open
        self.original_import = builtins.__import__
        self.original_os_write = os.write
        self.original_makedirs = os.makedirs

        os.makedirs = self.restricted_os_makedirs

        os.write = self.restrict_os_write

        #builtins.open = self.restricted_open

        self.log_writes()

    def deactivate(self):
        """
        Uninstall the restrictions on OS access.
        :return:
        """
        builtins.open = self.original_open
        os.system = os.system
        os.popen = os.popen
        if 'subprocess' in sys.modules:
            sys.modules['subprocess'].Popen = sys.modules['subprocess'].Popen
        builtins.__import__ = self.original_import
        os.write = self.original_os_write  # restore os.write to its original state
        os.makedirs = self.original_makedirs  # restore os.makedirs to its original state
