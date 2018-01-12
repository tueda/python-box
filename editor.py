"""Editor for Python programming."""
import sys
import time
import traceback

from browser import document, window


editor = window.ace.edit('editor')
console = document['console']
run_button = document['runButton']


editor.getSession().setMode('ace/mode/python')
editor.focus()


class ConsoleOutput:
    """Console output."""

    def write(self, data):
        """Write the given data."""
        console.value += str(data)

    def flush(self):
        """Flush the written data."""
        pass


sys.stdout = ConsoleOutput()
sys.stderr = ConsoleOutput()


@run_button.bind('click')
def run_python(_e):
    """Event handler for clicking "Run" button."""
    src = editor.getValue()
    document['console'].value = ''
    t0 = time.perf_counter()
    try:
        ns = {'__name__': '__main__'}
        exec(src, ns)
    except Exception:
        traceback.print_exc(file=sys.stderr)
    print('<completed in %8.3f s>' % (time.perf_counter() - t0))
