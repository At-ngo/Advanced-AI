import os
import sys
import json
import traceback

os.environ['MPLCONFIGDIR'] = 'C:/Users/ACER/AppData/Local/Temp'
os.environ['IPYTHONDIR'] = 'C:/Users/ACER/AppData/Local/Temp/ipython'

from IPython.core.interactiveshell import InteractiveShell
from IPython.utils.capture import capture_output


class NotebookShell(InteractiveShell):
    def enable_gui(self, gui=None):
        return None


def _split_lines(text):
    if not text:
        return []
    lines = text.splitlines(keepends=True)
    return lines


def _format_mime_bundle(data_dict):
    out = {}
    for k, v in data_dict.items():
        if isinstance(v, str) and '\n' in v and k in ('text/plain', 'text/html', 'text/markdown'):
            out[k] = _split_lines(v)
        else:
            out[k] = v
    return out


def execute_notebook(nb_path, skip_indices=None, seed=42):
    skip_indices = set(skip_indices or [])
    abs_nb_path = os.path.abspath(nb_path)
    nb_dir = os.path.dirname(abs_nb_path)
    orig_cwd = os.getcwd()

    with open(abs_nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    os.chdir(nb_dir)
    if nb_dir not in sys.path:
        sys.path.insert(0, nb_dir)

    try:
        sh = NotebookShell.instance()
        # Reset user namespace cleanly per notebook
        sh.reset(new_session=True)
        sh.run_cell('%matplotlib inline')
        if seed is not None:
            sh.run_cell(f'import numpy as _np; _np.random.seed({seed})')

        exec_count = 1
        errors = []

        for idx, cell in enumerate(nb.get('cells', [])):
            if cell.get('cell_type') != 'code':
                continue
            if idx in skip_indices:
                continue

            src = ''.join(cell.get('source', []))
            if not src.strip():
                cell['outputs'] = []
                cell['execution_count'] = None
                continue

            cell_outputs = []
            with capture_output(stdout=True, stderr=True, display=True) as cap:
                res = sh.run_cell(src, store_history=False)

            if cap.stdout:
                cell_outputs.append({
                    'output_type': 'stream',
                    'name': 'stdout',
                    'text': _split_lines(cap.stdout)
                })
            if cap.stderr:
                cell_outputs.append({
                    'output_type': 'stream',
                    'name': 'stderr',
                    'text': _split_lines(cap.stderr)
                })

            for disp in cap.outputs:
                cell_outputs.append({
                    'output_type': 'display_data',
                    'data': _format_mime_bundle(disp.data),
                    'metadata': disp.metadata or {}
                })

            if res.result is not None:
                data, metadata = sh.display_formatter.format(res.result)
                cell_outputs.append({
                    'output_type': 'execute_result',
                    'execution_count': exec_count,
                    'data': _format_mime_bundle(data),
                    'metadata': metadata or {}
                })

            if not res.success:
                err_obj = res.error_in_exec or res.error_before_exec
                err_name = type(err_obj).__name__ if err_obj else 'ExecutionError'
                err_val = str(err_obj) if err_obj else 'Unknown error'
                tb = traceback.format_exception(type(err_obj), err_obj, err_obj.__traceback__) if err_obj else []
                cell_outputs.append({
                    'output_type': 'error',
                    'ename': err_name,
                    'evalue': err_val,
                    'traceback': tb
                })
                errors.append((idx, err_name, err_val))

            cell['outputs'] = cell_outputs
            cell['execution_count'] = exec_count
            exec_count += 1

        with open(abs_nb_path, 'w', encoding='utf-8') as f:
            json.dump(nb, f, indent=1, ensure_ascii=False)

        print(f"[EXECUTED] {os.path.basename(abs_nb_path)} -> {exec_count-1} code cells, {len(errors)} errors", flush=True)
        for idx, en, ev in errors:
            print(f"  ERROR Cell {idx}: {en}: {ev}", flush=True)
        return len(errors) == 0
    finally:
        os.chdir(orig_cwd)


if __name__ == '__main__':
    for arg in sys.argv[1:]:
        execute_notebook(arg)

