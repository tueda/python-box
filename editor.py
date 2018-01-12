import sys
import time
import traceback

from browser import document, window


editor = window.editor
console = document['console']
run_button = document['runButton']


class COutput:
    def write(self, data):
        console.value += str(data)

    def flush(self):
        pass


sys.stdout = COutput()
sys.stderr = COutput()


@run_button.bind('click')
def run_python(_e):
    src = editor.getValue()
    document['console'].value = ''
    t0 = time.perf_counter()
    try:
        ns = {'__name__': '__main__'}
        exec(src, ns)
    except Exception:
        traceback.print_exc(file=sys.stderr)
    print('<completed in %8.3f s>' % (time.perf_counter() - t0))
