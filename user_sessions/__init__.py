try:
    from importlib.metadata import version
except ImportError:
    from pkg_resources import DistributionNotFound, get_distribution

    try:
        __version__ = get_distribution("django-user-sessions").version
    except DistributionNotFound:
        # package is not installed
        __version__ = None
else:
    __version__ = version("django-user-sessions")
