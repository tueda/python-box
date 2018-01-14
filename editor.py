"""Editor for Python programming."""
import sys
import time
import traceback

from browser import document, window


jq = window.jQuery
editor = window.ace.edit('editor')
console = document['console']
run_button = document['runButton']

# Editor setting.

editor.getSession().setMode('ace/mode/python')
editor.focus()

# HTML 5 local storage

if hasattr(window, 'localStorage'):
    from browser.local_storage import storage
else:
    storage = None

if storage is not None and 'py_src' in storage:
    editor.setValue(storage['py_src'], -1)


def on_window_unload(_e):
    """Event handler for exiting the page."""
    if storage is not None:
        storage['py_src'] = editor.getValue()


jq(window).on('unload', on_window_unload)


# Console output.

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


# Running the script.

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
