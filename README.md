# UsefulDecorators
> Some Decorators I use for various purposes. Some more useful, some less.

This is a collection of some Decorators for Python you might find useful.
```
pip install usefull-decorators
```
## Programming Patterns

### Cache
The Cache Decorator will automatically cache the creation of an object of the decorated class. 
```py
from useful_decorators.patterns import Cache

def disable():
    return True

@Cache(disable=disable)
class Test:
  def __init__(self,q,p=False):
    self.q = q
    self.p = p
 
q1 = Test("test",True) #Create a new Object
q2 = Test("test",True) #This will return the SAME object form the cache
q3 = Test("test2") #This will create a new Object.
```

On each call of an `__init__` method, 
the cache will check if there ever was another call that used the same arguments, and if yes return that. If you really want a new Object ( ignore the cache )
you can use `<class>.__create_no_cache()` with the arguments you would usally pass to the `__init__` method. You can also reset the cache with `<class>.__clear_cache()`
You can also use the disable property of the decorator. This allows you to specify a function which is called to check if the cache is enabled or disabled.
```py
Test.__create_no_cache("hello",True) #Always creates a new Object (will not be added to the cache)
#or
Test.__clear_cache()
Test("hello",True)
```
Note that cached objects are the __same__. If you change an attribute on one of the objects, the other will change too. In the example above changing
something in `q1` will also change `q2`. 
### Singleton
The Singleton decorator will change the class to only ever create one instance. This is done by injecting code in the `__init__` method which checks if an 
object of the class is already created. 
```py
from useful_decorators.patterns import Singleton

@Singleton(strict=False)
class Test:
    def __init__(self, q, p=False):
        self.q = q
        self.p = p


q1 = Test("test", True)  # Creates a new Object
q2 = Test("test", True)  # This is the same object as q1
q3 = Test("test2")  # If strict is disabled, this is ALSO the same objects as q1
```
There are basically two methods to handle calls to the `__init__` method after the original object was created. We can ignore the call no matter the arguments 
and return the singleton in all cases (default) or we can raise an error. 
It is __always__ better to use another method to get the instance because it is clearer to everybody who reads the code. So after you create an instance you can do the following
```py
q2 = Test.getInstance()
```
Which returns the instance. This is the only way when strict is set to true to obtain an instance. If strict is set to false, you can overwrite the current instance by using
```py
Test.resetInstance()
Test("hi",True)
#OR
Test.createNew("hi",True)
```
`createNew` is just a shortcut to reset and create at the same time.
### Observable
The Observable decorator allowes to to attach function calls to changes in the fields of the class.
```py
from useful_decorators.patterns import Observable

def changeling(q):
    print(q)


@Observable(attach=[("q", changeling)]) #Now changeling gets called with the new value everytime a new value is assigned to the field named 'q'
class Test:
    def __init__(self, q, p=False):
        self.q = q
        self.p = p


q1 = Test("hello")
q1.q = "world" #changeling gets called with 'world'
```
The decorator expects a list of tuples as the `attach` keyword. Each tuple must contain a name of a field in the class, and a method to call. 
This method must take exactly ONE argument (the updated value).
Currently there is no function call if the field gets deleted with `del`.
### builder_function
The builder_function decorator is just a shortcut for a method returning the object it belongs to. So instead of
```py
class Test:
    def __init__(self):
        self.q = None
        self.p = None
        
    def set_q(self,q):
        self.q = q
        return self
```
you can write
```py
from useful_decorators.patterns import builder_function

class Test:
    def __init__(self):
        self.q = None
        self.p = None
        
    @builder_function    
    def set_q(self,q):
        self.q = q
```
This allowes for easy construction of Objects that can be used like this `obj.setx(x).create_q(q,v=True)....`
## Functions
This repo provides some decorators for functions in general.
### attach
This decorator allowes you to attach another function to the decorated function.
```py
from useful_decorators.functions import attach

def attached(q=1):
  print("world"*q)
 
@attach(attached)
def foo():
  print("hello")
 
foo() # hello world
```
You can also specify the arguments that shall be passed to the attached function like so
```py
from useful_decorators.functions import attach

def attached(q=1):
  print("world"*q)
 
@attach(attached,q=2)
def foo():
  print("hello")
 
foo() # hello worldworld
```
Of course you can attach multiple methods as well. Just add more `@attach` decorators.
### prepend
this is _exactly_ the same as __attach__ but will execute the specified method __before__ the original method.
### chain
the chain decorator allowes for chaining functions together and feeding ones output in another ones input. 
```py
from useful_decorators.functions import chain

def q1(q,h=2):
  print(q*h)

@chain(q1)
def q2(q):
  return q+1
  
@chain(q1,3) #same as @chain(q1,h=3)
def q3(q):
  return q+1
  
q2(1) # 4 because (1+1)*2 = 4
q3(1) # 6 because (1+1)*3 = 6
```
The input is always the FIRST argument of the chained function. The function with the decorator is always evaluated first and then fed into the function which is 
mentioned in the decorator. Of course the chain can be as long as you want.

