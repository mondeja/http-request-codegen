import inspect
from types import FunctionType, LambdaType, MethodType


CallableTypes = (FunctionType, MethodType, LambdaType)


def function_has_kwarg(func, kwarg_name):
    '''Discovers if a given function has the argument ``kwarg_name`` in their
    definition. The check is not exhaustive because if an argument of the
    function contains the value ``'{kwarg_name}='`` will be falsely discovered.
    Useful only if you are sure that the function definition does not contains
    such argument value.

    It works also for module, class, method, function, traceback, frame, or
    code objects, but it only makes sense to use it for methods or functions.

    Args:
        func (function): Function to check if their keyword arguments contains
            the given ``kwarg_name``. If is not a module, class, method,
            function, traceback, frame, or code object, a TypeError argument
            will be raised.
        kwarg_name (str): Keyword argument name to check if it's defined as a
            keyword argument of the function ``func``. Does not trigger errors
            if the value passed to this argument can be casted to strings using
            string templates with ``'%s'`` syntax.

    Raises:
        TypeError: if  ``func`` is not a Python function.

    Examples:
        >>> def function_without_foo_kwarg(foo):
        ...     pass
        >>> function_has_kwarg(function_without_foo_kwarg, 'foo')
        False

        >>> def function_with_foo_kwarg(foo=None):
        ...     pass
        >>> function_has_kwarg(function_with_foo_kwarg, 'foo')
        True

        >>> def function_with_arg_valued_like_foo_kwarg_def(bar='foo=1'):
        ...     pass
        >>> function_has_kwarg(function_with_arg_valued_like_foo_kwarg_def,
        ...                    'foo')
        True

        >>> function_has_kwarg('bar', 'foo')
        Traceback (most recent call last):
          ...
        TypeError: function or method was expected, got str

        >>> def function_with_kwarg_def_123_valued(foo=123):
        ...     pass
        >>> function_has_kwarg(function_with_kwarg_def_123_valued, 123)
        False

    Returns:
        bool: ``True`` if the function contains such keyword argument name or
            ``False`` otherwise.
    '''
    response = False
    _inside_func_def = False
    try:
        func_source = inspect.getsource(func)
    except TypeError:
        raise TypeError(
            ('function or method was expected, got %s') % type(func).__name__,
        )

    for line in func_source.split('\n'):
        if not _inside_func_def and line.lstrip().startswith('def '):
            _inside_func_def = True

        # Would be rare if a kwarg as a string with default value containing
        # 'kwarg_name='. For this library we don't need this check
        if _inside_func_def and (('%s=' % kwarg_name) in line):
            response = True
            break

        if _inside_func_def and line.rstrip().endswith('):'):
            break
    return response
