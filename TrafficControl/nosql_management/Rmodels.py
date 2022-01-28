"""
This module represents all models of
nosql models which is saved in nosql.
"""
import abc
from modulefinder import Module
from .exceptions import NotClass,NotModule,ConnectorNotFound,BackEndNotStarted
from enum import Enum
import inspect
import redis
from .utils import decode_value
import re

class NoSQLDBs(Enum):
    """
    Add all Nosqls if you want
    """
    REDIS = [r'((r|R)edis)','Redis','redis']

class NoSQLDataStructurs(Enum):
    LIST = 'list'
    SET = 'set'
    ZSET = 'zset'
    HASHMAP = 'hash'
    GEO

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
    it can extract methods of a connector of automaticly .
    but you can give connector manually too.
    """
    def __init__(self,facade_module : Module,nosql_type:NoSQLDBs,connector = None):
        self.module = facade_module
        self._functions = set()
        self.connector = None
        self.db_name = nosql_type
        self.started = False

    def _check_started(self):
        if not self.started :
            raise BackEndNotStarted

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
        methods = inspect.getmembers(self.connection,predicate=inspect.ismethod)
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
            self.started = True
            return self.connection
        else :
            if hasattr(self.connector,connector_method):
                self.connection  = self.connector.connector_method(*args,**kwargs)
                self.started = True
        return self.connection

class SimpleKeyValueBasedNoSQLBackend(AbstractBaseBackEnd):
    """
    The implementation of Key value based nosql
    like redis . this backend represents the all
    functionalities of key value based functions.
    if you want to use functionalities like aggragation
    or mapreduce , you should make your own functions.
    note1 : this class contains simple functionality 
    of a key-value based nosql.
    note2 : if you want to make a same behaviour 
    for all key-value based backends you should add methods
    to this class.

    """

    def handel_response(self,value):
        """
        to handel responses from API
        for ex decoding values and etc.
        """
        return decode_value(value)

    def getKey(self,value):
        self._check_started()
        self.connection.get(value)

    def setKey(self,key,value):
        self._check_started()
        self.connection.set(key,value)

class RedisBackend(SimpleKeyValueBasedNoSQLBackend):
    """
    this backend uses redis module as API
    """
    def __init__(
        self,
        module = redis,
        nosql_type=NoSQLDBs.REDIS,
        connector = redis.Redis,
        decode_values = False
        ):
        super().__init__(module,nosql_type,connector)
        self.connector : redis.Redis = connector #to make autocomlpelet
        self.decode = decode_values
    
    def handel_response(self,value):
        if self.decode :
            return super().handel_response(value)
        return value

    def get(self,key):
        self._check_started()
        value  = self.connector.get(key)
        return self.handel_response(value)
    
    def set(self,key,value,*args,**kwargs):
        self._check_started()
        return self.connector.set(key,value,*args,**kwargs)
    
    def create_hash_map(self,h_name:str,**kwargs):
        """
        if just send one key and value parameter it uses
        hset command otherwise uses hmset command
        """
        if len(kwargs) == 1 :
            return self.connector.hset(
                h_name,
                kwargs.get('key'),
                kwargs.get('value')
                )
        elif len(kwargs) > 1 :
            return self.connector.hmset(
                h_name,
                kwargs
            )
        else :
            raise ValueError('Hash map should hase values')
    
    def delete_hash_map_fields(self,h_name:str,*args):
        return self.connector.hdel(h_name,*args)
    
    def get_hash_map_values(self,h_name:str,*args,_all = False):
        """
        if _all set to True returns all fields
        """
        if _all :
            response_dict = self.connector.hgetall(h_name)
            return self.handel_response(response_dict)
        else :
            response_dict = self.connector.hmget(h_name,args)
            return self.handel_response(response_dict)
    
    def delete_keys(self,*keys):
        return self.connector.delete(*keys)

    def delete_hash_map(self,h_name:str):
        return self.delete_keys(h_name)

    def aggregate_key(self,key_pattern:str,exlude_pattern:str = None):
        pass

    
    




    
