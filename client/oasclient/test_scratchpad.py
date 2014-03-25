"""
Quick and dirty tests.
"""
from jsonext import ServiceProxy

if __name__ == '__main__':
   
   s = ServiceProxy('localhost', 'jsonrpc', port=8080)
   print s.get_currencies()

