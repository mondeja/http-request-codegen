'''Common exceptions for http-request-codegen.'''


def raise_post_text_plain_n_parameters_not_1(
    n_parameters,
    exc_type=ValueError,
):
    '''Raises a ``ValueError`` with a message indicating that the user must
    pass only one parameter attempting to generate ``text/plain`` content-type
    encoded POST request.

    Args:
        n_parameters (int): Number of parameters provided by the user.
        exc_type (type): Exception type to raise.

    Examples:
        >>> raise_post_text_plain_n_parameters_not_1(5)
        Traceback (most recent call last):
        ...
        ValueError: You can only send one parameter making a POST ..., got 5
    '''
    raise exc_type(
        (
            'You can only send one parameter making a POST request encoded'
            ' as \'text/plain\', got %d'
        ) % n_parameters,
    )
