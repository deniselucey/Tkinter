# A Tkinter Text widget that provides a scrolling display of console
# stderr and stdout.

import threading
from tkinter import *

class ConsoleText(Text):

    class IORedirector(object):
        #A general class for redirecting I/O to this Text widget.
        def __init__(self,text_area):
            self.text_area = text_area

    class StdoutRedirector(IORedirector):
        #A class for redirecting stdout to this Text widget.
        def write(self,str):
            self.text_area.insert(END, str)

    class StderrRedirector(IORedirector):
        #A class for redirecting stderr to this Text widget.
        def write(self,str):
            self.text_area.write(str,True)

    def __init__(self, master=None, cnf={}, **kw):
        #See the __init__ for Tkinter.Text for most of this stuff.

        Text.__init__(self, master, cnf, **kw)

        self.started = False
        self.write_lock = threading.Lock()

        self.tag_configure('STDOUT',background='white',foreground='black')
        self.tag_configure('STDERR',background='white',foreground='red')

        self.config(state=NORMAL)
        self.bind('<Key>',lambda e: 'break') #ignore all key presses

    def start(self):

        if self.started:
            return

        self.started = True

        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr

        stdout_redirector = ConsoleText.StdoutRedirector(self)
        stderr_redirector = ConsoleText.StderrRedirector(self)

        sys.stdout = stdout_redirector
        sys.stderr = stderr_redirector

    def stop(self):

        if not self.started:
            return

        self.started = False

        sys.stdout = self.original_stdout
        sys.stderr = self.original_stderr

    def write(self,val,is_stderr=False):

        self.write_lock.acquire()

        self.insert('end',val,'STDERR' if is_stderr else 'STDOUT')
        self.see('end')

        self.write_lock.release()