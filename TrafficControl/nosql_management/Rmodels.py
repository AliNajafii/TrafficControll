"""
This module represents all models of
nosql models which is saved in nosql.
"""
import abc
from modulefinder import Module
from .exceptions import NotClass,NotModule,ConnectorNotFound
from enum import Enum
import inspect
import re

class NoSQLDBs(Enum):
    """
    Add all Nosqls if you want
    """
    REDIS = [r'((r|R)edis)','Redis','redis']

class AbstractBackend:
    """
    This abstract class is for
    nosql API implementation.
    combination of Backend and manager
    is based on Bridge Design Pattern
    and composition relationship.
    """

    @abc.abstractmethod
    def _set_api_module(self,module:Module):
        """
        setting API module
        """
        
    
    def _set_connector_class(self,cls:str):
        """
        set API class connector
        for no sql DB.
        cls should be str
        """
    
    def _API_function_finder(self):
        """
        Finds all methods available
        on connector class.
        or it you can any implement
        any way to find API functions
        """


     
class AbstractManager:
    """
    This class is for managing all
    interface oprations to a nosql
    DB. This is part Abstract of 
    Bridge Design Pattern.
    all functionalities are defined here.
    """
    @abc.abstractmethod
    def set_backend(self,backend:AbstractBackend):
        """
        setting implementation of an API
        to this Manager.
        """
    @abc.abstractmethod
    def start_backend(self): 
        """
        To startup the backend
        and make it ready to
        run.
        """

    
class AbstractBaseBackEnd(AbstractBackend):
    """
    extract all facade module functions 
    and bind them to the backend class.
    'start' method extracs and bind them to
    the backend object and returns connector object.
    """
    def __init__(self,facade_module : Module,nosql_type:NoSQLDBs,connector = None):
        self.module = facade_module
        self._functions = set()
        self.connector = None
        self.db_name = nosql_type

    
    def _set_api_module(self,module:Module):
        if not inspect.ismodule(self.connector):
            raise NotModule(f'{module.__class__.__name__} is not a module.')
        self.module = module
    
    def _set_connector_class(self,cls:str):
        if not inspect.isclass(cls):
            raise NotClass
        self.connector = cls
        
        
    def _find_possible_connectors(self):
        """
        finds the possible connector
        of API if connector is not given
        """
        if not self.connector:
            classes = inspect.getmembers(self.module,predicate=inspect.isclass)
            for name_patterns in self.db_name.value :
                for name,code in classes:
                    if re.fullmatch(name_patterns,name):
                        self._set_connector_class(code)
                        return code
            raise ConnectorNotFound('Connector class not found .set connector(API Facade) manually')
        else:
            return self.connector
    def _bind_API_methods(self):
        methods = inspect.getmembers(self.connector,predicate=inspect.isfunction)
        for name,code in methods :
            setattr(self,name,code)
        
    def start(self,connector_method=None,*args,**kwargs):
        """
        This method make connection by API connector
        connector_method is when you want make connection
        by a specific method.
        """
        self.connector = self._find_possible_connectors()
        if not connector_method:
            self.connection = self.connector(*args,**kwargs)
            self._bind_API_methods()
            return self.connection
        else :
            if hasattr(self.connector,connector_method):
                self.connection = self.connector.connector_method(*args,**kwargs)
        return self.connection
    
