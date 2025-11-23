'''
Structural analysis - focuses on code organization and patterns
'''
import ast
from typing import Dict,List,Any
from core.code_parser import CodeParser,FunctionInfo
from utils.ast_utils import ASTUtils

class StructuralAnalyzer:
    '''
    Analyze code structure and organization
    '''
    def __init__(self,code_parser:CodeParser):
        self.parser = code_parser
        self.ast_utils = ASTUtils()

    def analyze_structure(self,code:str) -> Dict[str,Any]:
        '''
        Comprehensive structural analysis
        '''
        functions = self.parser.extract_functions(code)
        tree = self.parser.parse_code(code)

        return {
            'function_count' : len(functions),
            'class_count' : self.count_classes(tree),
            'import_count' : self.count_imports(tree),
            'average_function_length' : self.calculate_avg_function_length(functions),
            'max_nesting_depth' : self.calculate_max_nesting(tree),
            'structural_issues' : self.find_structural_issues(functions,tree)
        }
    
    def count_classes(self,tree:ast.AST) -> int:
        '''
        Count class definitions
        '''
        return len([node for node in ast.walk(tree) if isinstance(node,ast.ClassDef)])
    
    def count_imports(self,tree:ast.AST) -> int:
        '''
        Count import statements
        '''
        import_nodes = [node for node in ast.walk(tree) if isinstance(node,(ast.Import,ast.ImportFrom))]

        return len(import_nodes)
    
    def calculate_avg_function_length(self,functions:List[FunctionInfo]) -> float:
        '''
        Calculate average function body length
        '''
        if not functions:
            return 0.0
        total_length = sum(len(func.body) for func in functions)

        return total_length/len(functions)
    
    def calculate_max_nesting(self,tree:ast.AST) -> int:
        '''
        Calculate maximum nesting depth in code
        '''
        max_depth = 0
        current_depth = 0

        for node in ast.walk(tree):
            if isinstance(node,(ast.FunctionDef,ast.ClassDef,ast.If,ast.For,ast.While)):
                current_depth += 1
                max_depth = max(max_depth,current_depth)
        return max_depth
    
    def find_structural_issues(self,functions:List[FunctionInfo],tree:ast.AST)->List[str]:
        '''Identify structural issues in code'''
        issues = []

        #Check for too long functions
        for func in functions:
            if len(func.body) > 50:
                issues.append(f'Function "{func.name}" is too long ({len(func.body)} lines)')

        # Check for organizational problems
        if len(functions) > 10 and self.count_classes(tree) == 0:
            issues.append('Many functions but no classes - consider organizing functions into classes')

        return issues