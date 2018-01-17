"""Editor for Python programming."""
import sys
import time
import traceback
import turtle

from browser import document, window


jq = window.jQuery
editor = window.ace.edit('editor')
console = document['console']

# Editor setting.

editor.getSession().setMode('ace/mode/python')
editor.setOptions({
    'behavioursEnabled': False,
})
editor.focus()

# Turtle graphics

_turtles = set()

turtle.set_defaults(
    canvwidth=600,
    canvheight=400,
    turtle_canvas_wrapper=document['turtle-div']
)

_turtle_orig_goto = turtle.Turtle._goto


def _turtle_new_goto(self, *args):
    _turtle_orig_goto(self, *args)
    _turtles.add(self)


turtle.Turtle._goto = _turtle_new_goto

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

    def __init__(self, class_=None):
        """Construct a console output."""
        if class_ is None:
            self._fmt = '{}'
        else:
            self._fmt = '<span class="{}">{{}}</span>'.format(class_)

    def write(self, data):
        """Write the given data."""
        console.html += self._fmt.format(escape(str(data)).replace('\n',
                                                                   '<br>'))

    def flush(self):
        """Flush the written data."""
        pass

    def clear(self):
        """Clear the console."""
        console.html = ''


def escape(string):
    """Replace special characters to HTML-safe sequences."""
    # NOTE: somehow html.escape() didn't work.
    return (string.replace('&', '&amp;').replace('<', '&lt;').
            replace('>', '&gt;'))


sys.stdout = ConsoleOutput()
sys.stderr = ConsoleOutput('error')
info_console = ConsoleOutput('info')


# Home button

home_button = document['homeButton']


@home_button.bind('click')
def on_home_click(e):
    """Event handler for clicking "Home" button."""
    e.preventDefault()


# Running the script.

run_button = document['runButton']


@run_button.bind('click')
def run_python(e):
    """Event handler for clicking "Run" button."""
    src = editor.getValue()
    on_window_unload(None)  # save to storage
    info_console.clear()
    _turtles.clear()
    t0 = time.perf_counter()
    try:
        ns = {'__name__': '__main__'}
        exec(src, ns)
        if _turtles:
            turtle.show()
    except Exception:
        traceback.print_exc(file=sys.stderr)
    info_console.write('Completed in %8.3f s\n' % (time.perf_counter() - t0))
    e.preventDefault()


# Loading a script.

load_button = document['loadButton']
load_input = document['loadInput']


@load_button.bind('click')
def load_python(e):
    """Event handler for clicking "Load" button."""
    load_input.click()
    e.preventDefault()


def handle_files(files):
    """Handle a file list object."""
    f = files[0]
    reader = window.FileReader.new()
    reader.onload = lambda e: editor.setValue(e.target.result, -1)
    reader.readAsText(f)


window.handleFiles = handle_files

# Saving the script.

saveas_button = document['saveAsButton']
saveas_input = document['saveAsInput']


@saveas_button.bind('click')
def save_python(e):
    """Event handler for clicking "SaveAs" button."""
    filename = saveas_input.value
    if not filename:
        filename = saveas_input.placeholder
    filename += '.py'
    blob = window.Blob.new([editor.getValue()],
                           {type: 'text/plain;charset=utf-8'})
    window.saveAs(blob, filename)
    e.preventDefault()
