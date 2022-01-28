from django.test import TestCase
from .Rmodels import AbstractBaseBackEnd,NoSQLDBs
from .exceptions import NotModule
import inspect
import redis
class TestAbstractbaseBackend(TestCase):

    def setUp(self):
        self.backend = AbstractBaseBackEnd(redis,NoSQLDBs.REDIS)
    
    def test_start(self):
        
        connection = self.backend.start()
        self.assertIsInstance(connection,self.backend.connector)
        backends_functions_itself = inspect.getmembers(
            self.backend,
            inspect.isfunction
        )
        backends_functions_itself = [code for _,code in backends_functions_itself]
        self.assertIn(redis.Redis.geoadd,backends_functions_itself)
        self.assertIn(redis.Redis.save,backends_functions_itself)
        self.assertIn(redis.Redis.sadd,backends_functions_itself)
        self.assertIn(redis.Redis.lpush,backends_functions_itself)
    
    def test_set_api_module(self):
        with self.assertRaises(NotModule):
            self.backend._set_api_module('This is not module')
    
    def test_find_possible_connectors(self):
        connector = self.backend._find_possible_connectors()
        self.assertEqual(connector,redis.Redis)
    
    def test_API_functions(self):
        """
        tests if binded functions work 
        properly or not
        """
        self.backend.start(host='127.0.0.1')
        self.backend.ping()
        self.backend.set('TEST','VALUE')
        val = self.backend.get('TEST')
        self.assertEqual(val,b'VALUE')

        