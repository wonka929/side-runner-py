import time
from inspect import signature, Parameter
from .log import getLogger
logger = getLogger(__name__)


def with_retry(retry, wait, func, *args):
    for i in range(retry):
        try:
            return func(*args)
        except Exception as exc:
            logger.info(exc)
        finally:
            time.sleep(wait)


def call_with_argname_bind(func, args_dict):
    params = signature(func).parameters
    param_names = [
        p.name
        for p in params.values()
        if p.kind == Parameter.POSITIONAL_OR_KEYWORD
    ]

    try:
        if len(param_names) == len(args_dict) and all([k in param_names for k in args_dict.keys()]):
            return func(**args_dict)
        else:
            return func()
    except TypeError as exc:
        logger.warning('Mismatch of hook function args: {}'.format(str(exc)))
