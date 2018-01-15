"""Editor for Python programming."""
import sys
import time
import traceback

from browser import document, window


jq = window.jQuery
editor = window.ace.edit('editor')
console = document['console']

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

run_button = document['runButton']


@run_button.bind('click')
def run_python(e):
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
    e.preventDefault()


# Load a script.

load_button = document['loadButton']
file_input = document['fileInput']


@load_button.bind('click')
def load_python(e):
    """Event handler for clicking "Load" button."""
    file_input.click()
    e.preventDefault()


def handle_files(files):
    f = files[0]
    reader = window.FileReader.new()
    reader.onload = lambda e: editor.setValue(e.target.result, -1)
    reader.readAsText(f)


window.handleFiles = handle_files
