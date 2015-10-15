import ctypes
ll = ctypes.cdll.LoadLibrary 
lib = ll("./libpycall.so")  
lib.foo(1, 3)
print '***finish***'