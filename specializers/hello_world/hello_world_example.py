from hello_world import *

class HelloWorldTest(HelloWorld):
  def hello():
    print 'hello', 'world'

HelloWorldTest().hello()