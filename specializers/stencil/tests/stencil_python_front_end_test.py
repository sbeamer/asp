import unittest2 as unittest
from stencil_python_front_end import *
from assert_utils import *
import ast

class BasicTests(unittest.TestCase):
    def test_parse_interior(self):
        python_ast = ast.parse(
'''
def kernel(self, in_grid, out_grid):
    for x in out_grid.interior_points():
        for y in in_grid.neighbors(x, 1):
            out_grid[x] = out_grid[x] + in_grid[y]
'''
                              )
        stencil_model = StencilPythonFrontEnd(dict()).parse(python_ast)
        assert_has_type(stencil_model, StencilModel)
        assert len(stencil_model.interior_kernel.body) > 0 and len(stencil_model.border_kernel.body) == 0

    def test_parse_border(self):
        python_ast = ast.parse(
'''
def kernel(self, in_grid, out_grid):
    for x in out_grid.border_points():
        for y in in_grid.neighbors(x, 1):
            out_grid[x] = out_grid[x] + in_grid[y]
'''
                              )
        stencil_model = StencilPythonFrontEnd(dict()).parse(python_ast)
        assert_has_type(stencil_model, StencilModel)
        assert len(stencil_model.interior_kernel.body) == 0 and len(stencil_model.border_kernel.body) > 0

    def test_parse_both(self):
        python_ast = ast.parse(
'''
def kernel(self, in_grid, out_grid):
    for x in out_grid.interior_points():
        for y in in_grid.neighbors(x, 1):
            out_grid[x] = out_grid[x] + in_grid[y]
    for x in out_grid.border_points():
        for y in in_grid.neighbors(x, 1):
            out_grid[x] = out_grid[x] + in_grid[y]
'''
                              )
        stencil_model = StencilPythonFrontEnd(dict()).parse(python_ast)
        assert_has_type(stencil_model, StencilModel)
        assert len(stencil_model.interior_kernel.body) > 0 and len(stencil_model.border_kernel.body) > 0

    def test_parse_constants(self):
        python_ast = ast.parse(
'''
def kernel(self, in_grid, out_grid):
    for x in out_grid.interior_points():
        for y in in_grid.neighbors(x, 1):
            out_grid[x] = out_grid[x] - 1/4*in_grid[y] + 1.0/4*in_grid[y]
'''
                              )
        stencil_model = StencilPythonFrontEnd(dict()).parse(python_ast)
        assert_has_type(stencil_model, StencilModel)

if __name__ == '__main__':
    unittest.main()
