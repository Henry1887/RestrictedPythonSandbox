import os
from RestrictedPython import compile_restricted
from RestrictedPython.Guards import safe_builtins

def display(message: str):
    print(message)

def sandbox_process(sandbox_code, exposed_objects):
    local_env = {
        '__builtins__': safe_builtins,
        '_getattr_': getattr,
        '_getitem_': lambda obj, index: obj[index],
        '_getiter_': iter,
        '_write_': lambda obj: obj,
        'exposed_objects': exposed_objects,
        'display': display
    }

    if exposed_objects.get("open", None):
        local_env["open"] = exposed_objects["open"]

    if exposed_objects.get("spawn_sandboxed_python", None):
        local_env["spawn_sandboxed_python"] = exposed_objects["spawn_sandboxed_python"]

    try:
        compiled_code = compile_restricted(sandbox_code, '<string>', 'exec')
        exec(compiled_code, local_env)
    except Exception as e:
        return f"Error in sandbox: {e}"
    return "1"

def spawn_sandboxed_python(code, allow_spawning_sandbox=False, exposed_objects={}, dir_permissions=None, file_permissions=None, current_open=None):
    if current_open is not None:
        original_open = current_open
        
        def restricted_open(filepath, mode='r', *args, **kwargs):
            filepath = os.path.abspath(filepath)

            request_write = "w" in mode
            request_read = "r" in mode
            was_in_any_folder = False

            if dir_permissions and filepath:
                for dir in dir_permissions:
                    if os.path.commonpath([filepath, os.path.abspath(dir)]) == os.path.abspath(dir):
                        was_in_any_folder = True
                        if request_write and 'w' not in dir_permissions[dir]:
                            raise PermissionError(f"Write access is restricted to the directory: {dir}")
                        if request_read and 'r' not in dir_permissions[dir]:
                            raise PermissionError(f"Read access is restricted to the directory: {dir}")
            if not was_in_any_folder:
                raise PermissionError(f"Access to {filepath} is not allowed.")
            
            if file_permissions and filepath in file_permissions:
                perms = file_permissions[filepath]
                if request_read and 'r' not in perms:
                    raise PermissionError(f"Read access is restricted to the file: {filepath}")
                if request_write and 'w' not in perms:
                    raise PermissionError(f"Write access is restricted to the file: {filepath}")
            return original_open(filepath, mode, *args, **kwargs)

        exposed_objects['open'] = restricted_open

    if allow_spawning_sandbox:
        exposed_objects['spawn_sandboxed_python'] = spawn_sandboxed_python

    return sandbox_process(code, exposed_objects)
