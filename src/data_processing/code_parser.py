import ast 
import tokenize
from typing import Dict, List, Optional, Any

class CodeParser:
    '''
    Convert code from text to it's basic structures
    '''

    def __init__(self):
        self.supported_languages = ['python'] #expand later

    def parse_to_ast(self,code:str) -> Optional[ast.AST]:
        '''
        Transform linear text to tree structure
        '''
        try:
            tree = ast.parse(code)
            return tree
        except SyntaxError as e:
            print(f'Cannot understand this code structure : {e}')
            return None
        
    def extract_functions(self,code:str) -> List[Dict[str,Any]]:
        '''
        Identify and catalog all functions 
        '''
        # First create AST
        tree = self.parse_to_ast(code)
        if not tree:
            return []
        
        functions = []

        #Look for function definitions in AST
        for node in ast.walk(tree): #ast.walk recursively yields descendant nodes starting at node
            if isinstance(node,ast.FunctionDef):
                #check if node is instance of function definition
                function_info = {
                    'name' : node.name,
                    'line_number' : node.lineno,
                    'arguments' : self._extract_arguments(node.args),
                    'body_length' : len(node.body),
                    'has_docstring' : bool(ast.get_docstring(node)),
                    'complexity' : self._calculate_function_complexity(node)
                }
                functions.append(function_info)
            
        
        return functions
    
    def _extract_arguments(node,args_node:ast.arguments) -> List[str]:
        '''
        Extract function arguments
        '''
        arguments = [arg.arg for arg in args_node.args]

        #handle defaults,kwargs etc.
        if args_node.vararg:
            arguments.append(f'**{args_node.vararg.arg}')
        if args_node.kwarg:
            arguments.append(f'**{args_node.kwarg.arg}')

        return arguments
    
    def _calculate_function_complexity(self,function_node:ast.FunctionDef) -> int:
        '''
        Cyclomatic complexity - Measures paths through code
        Higher no. of paths = harder to test and maintain
        '''
        complexity = 1 #initial value

        for node in ast.walk(function_node):
            #count decision points
            if isinstance(node,(ast.If,ast.While,ast.For,ast.AsyncFor)):
                #decision points like if else loops,while loops etc increase complexity
                complexity += 1
            if isinstance(node,ast.BoolOp) and isinstance(node.op,(ast.And,ast.Or)):
                #logical operators like AND and OR increase complexity
                complexity += 1

        return complexity

#testing code
if __name__ == '__main__':
    sample_code = """
def calculate_sum(a, b):
    '''Add two numbers and return result'''
    result = a + b
    return result

def process_data(data, threshold=10):
    '''Process data with optional threshold'''
    if not data:
        return []
    
    filtered = []
    for item in data:
        if item > threshold:
            filtered.append(item * 2)
        else:
            filtered.append(item)
    
    return filtered
"""
parser = CodeParser()
functions = parser.extract_functions(sample_code)

print('AST')
print('='*40)
tree = parser.parse_to_ast(sample_code)
print(ast.dump(tree,indent=4))

print('CODE UNDERSTANDING REPORT')
print('='*40)

for func in functions:
    print(f'\nFunction: {func['name']}')
    print(f'Line : {func['line_number']}')
    print(f'Arguments : {func['arguments']}')
    print(f'Body length : {func['body_length']} statements')
    print(f'Has docstring : {func['has_docstring']}')
    print(f'Complexity score : {func['complexity']}')

    if func['complexity'] > 5:
        print('!!! High complexity - consider breaking into smaller functions')
    if not func['has_docstring']:
        print('Consider adding docstring')
    if len(func['arguments']) > 4:
        print('Too many arguments - consider using a config object')