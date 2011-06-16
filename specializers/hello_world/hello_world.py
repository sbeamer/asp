import inspect
import asp.codegen.python_ast as ast
import asp.codegen.cpp_ast as cpp_ast
import asp.codegen.ast_tools as ast_tools

class HelloWorld(object):
  def __init__(self):
    # check for hello method
    try:
      dir(self).index('hello')
    except ValueError:
      raise Exception('No hello method defined.')
    self.hello_src = inspect.getsource(self.hello)
    self.hello_ast = ast.parse(self.hello_src.lstrip())  
    self.hello = self.shadow_hello

  def shadow_hello(self):
    from asp.jit import asp_module
    mod = asp_module.ASPModule()
    mod.module.add_to_preamble([cpp_ast.Include("iostream", True)])
    converted = ast_tools.ConvertAST().visit(self.hello_ast)
    mod.add_function(converted, 'hello')
    mod.hello()

    # Print out source of generated code
    # print mod.module.generate()
