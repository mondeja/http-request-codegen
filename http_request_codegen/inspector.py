
import inspect


def function_has_kwarg(func, kwarg_name):
    response = False
    _inside_func_def = False
    for line in inspect.getsource(func).split("\n"):
        if not _inside_func_def and line.lstrip().startswith("def "):
            _inside_func_def = True

        # Would be rare if a kwarg as a string with default value containing
        # 'kwarg_name='. For this library we don't need this check
        if _inside_func_def and (('%s=' % kwarg_name) in line):
            response = True
            break

        if _inside_func_def and line.rstrip().endswith("):"):
            break
    return response
