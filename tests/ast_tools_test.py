import unittest

from asp.codegen.ast_tools import *
from asp.codegen.cpp_ast import *
import asp.codegen.python_ast as python_ast

# class LoopBlockerTests(unittest.TestCase):
#     def test_basic_blocking(self):
#         # this is "for(int i=0, i<8; i+=1) { a[i] = i; }"
#         ast = For(
#             ForInitializer(Value("int", CName("i")), CNumber(0)),
#             BinOp(CName("i"), "<", CNumber(8)),
#             Assign(CName("i"), BinOp(CName("i"), "+", CNumber(1))),
#             Block(contents=[Assign(Subscript(CName("a"), CName("i")),
#                    CName("i"))]))
#         wanted_output = "for (int ii=0; ii<8; ii += 2)\n{\nfor (int i=ii; i<min(ii+2,8); i+=1)\n{\na[i]=i;}}"
#         output = str(LoopBlocker().loop_block(ast, 2))
#         self.assertEqual(output, wanted_output)


class NodeVisitorTests(unittest.TestCase):
    def test_for_python_nodes(self):
        class Dummy(NodeVisitor):
            def visit_Name(self, node):
                return False
        p = python_ast.Name("hello", False)
        self.assertFalse(Dummy().visit(p))

    def test_for_cpp_nodes(self):
        class Dummy(NodeVisitor):
            def visit_CName(self, node):
                return False
        c = CName("hello")
        self.assertFalse(Dummy().visit(c))

    def test_for_cpp_children(self):
        class Dummy(NodeVisitor):
            def __init__(self):
                self.worked = False
            def visit_CName(self, _):
                self.worked = True

        c = BinOp(CNumber(1), "+", CName("hello"))
        d = Dummy()
        d.visit(c)
        self.assertTrue(d.worked)


class NodeTransformerTests(unittest.TestCase):

    class Dummy(NodeTransformer):
        def visit_Name(self, _):
            return python_ast.Name("hi", False)
        def visit_CName(self, _):
            return CName("hi")

    def test_for_python_nodes(self):
        p = python_ast.Name("hello", False)
        result = self.Dummy().visit(p)
        self.assertEqual(result.id, "hi")

    def test_for_cpp_nodes(self):
        c = CName("hello")
        result = self.Dummy().visit(c)
        self.assertEqual(result.name, "hi")

    def test_for_cpp_children(self):
        c = BinOp(CNumber(1), "+", CName("hello"))
        result = self.Dummy().visit(c)
        self.assertEqual(result.right.name, "hi")


class LoopUnrollerTests(unittest.TestCase):
    def setUp(self):
        # this is "for(int i=0, i<8; i+=1) { a[i] = i; }"
        self.test_ast = For(
            "i",
            CNumber(0),
            CNumber(7),
            CNumber(1),
            Block(contents=[Assign(Subscript(CName("a"), CName("i")),
                   CName("i"))]))

    def test_unrolling_by_2(self):
        result = LoopUnroller().unroll(self.test_ast, 2)
        wanted_result = "for (int i = 0; (i <= 7); i = (i + (1 * 2)))\n{\n  a[i] = i;\n  a[(i + 1)] = (i + 1);\n}"
        self.assertEqual(str(result).replace(' ',''), str(wanted_result).replace(' ', ''))

    def test_unrolling_by_4(self):
        result = LoopUnroller().unroll(self.test_ast, 4)
        wanted_result = "for (int i = 0; (i <= 7); i = (i + (1 * 4)))\n{\n  a[i] = i;\n  a[(i + 1)] = (i + 1);\n  a[(i + 2)] = (i + 2);\n  a[(i + 3)] = (i + 3);\n}"

        self.assertEqual(str(result).replace(' ',''), str(wanted_result).replace(' ', ''))

    def test_imperfect_unrolling (self):
        result = LoopUnroller().unroll(self.test_ast, 3)
        wanted_result = "for (int i = 0; (i <= 5); i = (i + (1 * 3)))\n{\n  a[i] = i;\n  a[(i + 1)] = (i + 1);\n  a[(i + 2)] = (i + 2);\n}\n" + "for (int i = 6; (i <= 7); i = (i + 1))\n{\n  a[i] = i;\n}"
        self.assertEqual(str(result).replace(' ',''), str(wanted_result).replace(' ', ''))




if __name__ == '__main__':
    unittest.main()
