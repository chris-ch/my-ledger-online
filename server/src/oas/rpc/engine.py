import sys
import logging
import json
import datetime

from functools import wraps
from urllib.parse import unquote

from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.http import HttpResponseBadRequest
from django.http import HttpResponseServerError
from django.http import HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.db import models

import oas.rpc

_LOG = logging.getLogger('oas.rpc.engine')

_remote_func_register = []

def model_serialize(my_obj):
    if my_obj is None:
        output = None
        
    elif getattr(my_obj, '__iter__', False):
        if getattr(my_obj, 'keys', False):
            output = dict()
            for k in my_obj.keys():
                output[k] = model_serialize(my_obj[k])
        
        else:
            output = list()
            for item in my_obj:
                output.append(model_serialize(item))
                
    elif isinstance(my_obj, models.Model):        
        # filtering out private and special fields
        def is_field_allowed(field):
            return not(field.startswith('_') or field == 'id' or field.endswith('_id'))
            
        output = dict([(field, model_serialize(my_obj.__dict__[field]))
                        for field in  my_obj.__dict__.keys()
                        if is_field_allowed(field)
                       ])
        
    elif getattr(my_obj, 'isoformat', False):
        output = my_obj.isoformat()[:10]
    
    elif getattr(my_obj, 'isalnum', False):
        output = my_obj
        
    elif getattr(my_obj, 'to_eng_string', False):
        output = my_obj.to_eng_string()
        
    else:
        output = my_obj
    
    #_LOG.debug('serialized: %s' % output)    
    return output

class RPCServerError:
    def __init__(self, wrapped_traceback):
        self._wrapped_traceback = wrapped_traceback
        
    def __str__(self):
        output = 'wrapped error: "%s"' % (''.join(self._wrapped_traceback))
        return output

"""
{target:"/jsonrpc", // this defines the URL to connect for the services
 transport:"POST", // We will use POST as the transport
 envelope:"JSON-RPC-1.2", // We will use JSON-RPC
 SMDVersion:"2.0",
 services: {
   add : { // define a service to add two numbers
   parameters: [
     {name:"a",type:"number"}, // define the two parameters
     {name:"b",type:"number"}],
   returns:{"type":"number"}
 },
 foo : {   // nothing is required to be defined, all definitions are optional.
   //This service has nothing defined so it can take any parameters
  //and return any value
 },
 getNews : {
   // we can redefine the target, transport, and envelope for specific services
   target: "/newsSearch",
   transport: "GET",
   envelope: "URL",
   parameters:[ { name: "query", type: "string", optional: false, default: "" } ],
   returns:{type:"array"}
 }
}
"""
@csrf_exempt
def jsonrpc_smd(request):
    smd = {
            'transport': 'GET',
            'envelope': 'JSON-RPC-2.0',
            'target': '/jsonrpc/',
            'SMDVersion': '2.0',    
            'parameters': [
                {
                'name': 'outputType',
                'default': 'json'
                },
                {
                'name': 'ignoreErrors',
                'optional': True
                }
                ],
            }
    smd['services'] = dict()
    for registered_func in _remote_func_register:
        # naive implementation for the time being
        parameters = []
        parameters.append({
                        'name':'legal_entity_code', 
                        'type':'string'
                    })
        returns = {'type': 'array'}
        smd['services'][registered_func] = {
                'parameters': parameters,
                'returns': returns
                }
        # OVERIDES
        smd['services'][registered_func] = {}
      
    output = json.dumps(smd)
    http_response = HttpResponse(output, mimetype='application/json') 
    return http_response
    
@csrf_exempt
def jsonrpc(request):
    try:
        json_response = {'jsonrpc': '2.0' }
        
        _LOG.debug('current user: %s ', request.user)
        if request.method == 'POST':
            _LOG.debug('reading data from post')
            data = request.raw_post_data
        
        else:
            _LOG.debug('reading data from get')
            raw_request = unquote(request.GET.urlencode().strip())
            # trailing characters may mess up output
            data = raw_request[:(raw_request.rfind('}') + 1)]
            
        _LOG.debug('parsing <JSON>%s</JSON>' % (data))
        try:
            json_request = json.loads(data)
            _LOG.debug('request json: %s' % (json_request))
            
        except:
                import traceback
                exc_type, exc_value, exc_tb = sys.exc_info()
                tb = traceback.format_exception(exc_type, exc_value, exc_tb)
                _LOG.error('An error occured while parsing JSON input: %s %s' % (str(data), ''.join(tb)))
                error = {'code': -32700, 'message': 'Parse error'}
                json_response['error'] = error
                return HttpResponseBadRequest(json.dumps(json_response), mimetype="application/json")
        
        try:
            if not getattr(json_request, 'has_key', False):
                # Batch request - TODO
                # in case of a batch request only processes the first occurence
                method = json_request[0]['method']
                params = json_request[0]['params']
                req_id = json_request[0]['id']
                
            else:
                method = json_request['method']
                params = json_request['params']
                req_id = json_request['id']
        
        except:
                import traceback
                exc_type, exc_value, exc_tb = sys.exc_info()
                tb = traceback.format_exception(exc_type, exc_value, exc_tb)
                _LOG.error('The JSON sent is not a valid Request object: %s %s' % (str(json_request), ''.join(tb)))
                error = {'code': -32600, 'message': 'Invalid Request'}
                json_response['error'] = error
                return HttpResponseBadRequest(json.dumps(json_response), mimetype="application/json")
                
        json_response['id'] = req_id
        
        _LOG.debug('method: "%s"' % str(method))
        _LOG.debug('params: %s' % str(params))    
        _LOG.debug('req_id: "%s"' % str(req_id))
        for registered_func in _remote_func_register:
            _LOG.debug('registered: "%s"' % str(registered_func))
            
        if method in _remote_func_register:    
            proc_module = sys.modules[settings.RPC_LIB]
            func = getattr(proc_module, method)
            try:
                import oas
                oas.init_context(request.user)
                with transaction.commit_on_success():
                    if not getattr(params, 'has_key', False):
                        _LOG.debug('function: %s(%s)' % (func.func_name, ', '.join(map(unicode, params))))
                        result = func(*params)
                    
                    else:
                        _LOG.debug('function: %s(%s)' % (func.func_name, unicode(params)))
                        result = func(**params)
                
                json_response['result'] = result
                
            except TypeError:
                error = {'code': -32602, 'message': 'Invalid params'}
                json_response['error'] = error
                import traceback
                exc_type, exc_value, exc_tb = sys.exc_info()
                tb = traceback.format_exception(exc_type, exc_value, exc_tb)
                _LOG.error('Invalid params %s: %s' % (func.func_name, ''.join(tb)))
                return HttpResponseBadRequest(json.dumps(json_response), mimetype="application/json")
                
            except oas.rpc.LegalEntityCreationFailure as error:
                error = {'code': -32000, 'message': 'Legal entity creation failed: %s' % error.message}
                json_response['error'] = error
                return HttpResponseServerError(json.dumps(json_response), mimetype="application/json")
                
            except:
                error = {'code': -32603, 'message': 'Server error'}
                json_response['error'] = error
                import traceback
                exc_type, exc_value, exc_tb = sys.exc_info()
                tb = traceback.format_exception(exc_type, exc_value, exc_tb)
                _LOG.error('An error occured while calling %s: %s' % (func.func_name, ''.join(tb)))
                return HttpResponseServerError(json.dumps(json_response), mimetype="application/json")
        
        else:
            _LOG.error('function not found: %s' % method)
            error = {'code': -32601, 'message': 'Method not found'}
            json_response['error'] = error
            return HttpResponseNotFound(json.dumps(json_response), mimetype="application/json")
        
        output = json.dumps(json_response)
        http_response = HttpResponse(output, mimetype="application/json")
        
    except:
        import traceback
        exc_type, exc_value, exc_tb = sys.exc_info()
        tb = traceback.format_exception(exc_type, exc_value, exc_tb)
        raise RPCServerError(tb)
        
    return http_response
    
def remote(func, serializer=model_serialize):
    _LOG.debug('declaring decorated function %s' % str(func.func_name))
    _remote_func_register.append(func.func_name)
    
    @wraps(func)
    def wrapper(*args, **kwds):
        _LOG.debug('calling %s(%s, %s)' % (str(func), args, kwds))
        result = func(*args, **kwds)
        serialized = serializer(result)    
        return serialized
        
    return wrapper

def remote_custom(serializer=model_serialize):
    
    def inner(func):
        _LOG.debug('declaring decorated function %s' % str(func.func_name))
        _LOG.debug('using specific serializer: %s', str(model_serialize))
        _remote_func_register.append(func.func_name)
        
        @wraps(func)
        def wrapper(*args, **kwds):
            _LOG.debug('calling %s(%s, %s)' % (str(func), args, kwds))
            result = func(*args, **kwds)
            serialized = serializer(result)
            return serialized
            
        return wrapper

    return inner

