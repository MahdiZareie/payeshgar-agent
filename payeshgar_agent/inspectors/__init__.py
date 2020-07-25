"""
This package contains different modules, each containing a different type of inspector
each inspector should be able to inspect a specific type of endpoint
"""


class BaseInspector:
    """
    this class is here to represents the interface of an inspector class
    """

    def inspect(self, endpoint: dict):
        raise NotImplementedError()


def get_inspector(endpoint) -> BaseInspector:
    """
    This is a factory function responsible to create the correct Inspector class based on type of the endpoint
    at the moment we only support HTTP endpoints, so this function always ignores the endpoint parameter and
    will returns a new HTTPInspector instance
    """
    from payeshgar_agent.inspectors import HTTPInspector
    return HTTPInspector()
