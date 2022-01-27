class NotModule(Exception):
    """
    when connector is not set 
    in AbstractbaseBackend or in it's
    childs this will be risen.
    """
class ConnectorNotFound(Exception):
    """
    when AbstractbaseBackend class cant
    find connector automatically
    """
class NotClass(Exception):
    """
    when checking the connector(API facade)
    if it is not a class AbstractbaseBackend
    raise this class
    """