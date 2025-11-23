import ast
from typing import Dict, List

class BasicQualityAnalyzer:
    def __init__(self):
        self.quality_rules = {
            'function_length' : 50,
            'argument_count' : 4,
            'complexity_threshold' : 10
        }

    def analyze_code_quality(self,code:str) -> Dict[str,List[str]]:
        issues = {
            'style_issues' : [],
            'complexity_issues' : [],
            'maintainability_issues' : [],
            'documentation_issues' : []
        }

        tree = ast.parse(code)

        #Analyze each function
        for node in ast.walk(tree):
            if isinstance(node,ast.FunctionDef):
                self._analyze_function(node,issues)
        
        return issues
    
    def _analyze_function(self,function_node:ast.FunctionDef,issues:Dict):
        '''
        Apply function level quality rules
        '''
        # Rule : Function name should be descriptive
        if not self._is_descriptive_name(function_node.name):
            issues['style_issues'].append(f'Function {function_node.name} : Name could be more descriptive')
        
        # Rule : Function should not be too long
        if len(function_node.body) > self.quality_rules['function_length']:
            issues['maintainability_issues'].append(f'Function {function_node.name} : Too long {len(function_node.body)} lines')

        # Rule : Check argument count
        arg_count = len(function_node.args.args)
        if arg_count > self.quality_rules['argument_count']:
            issues['complexity_issues'].append(f'Function {function_node.name} : Too many arguments ({arg_count})')

    
    def _analyze_module_structure(self,tree:ast.AST,issues:Dict):
        '''Module level quality rules'''
        imports = [node for node in ast.walk(tree) if isinstance(node,ast.Import,ast.ImportFrom)]
        functions = [node for node in ast.walk(tree) if isinstance(node,ast.FunctionDef)]
        classes = [node for node in ast.walk(tree) if isinstance(node,ast.ClassDef)]

        #Rule - reasonable organizatin
        if len(functions) > 20 and len(classes) == 0:
            issues['maintainability_issues'].append(f'Many functions but no classes - consider organizing into classes')

    def _is_descriptive_name(self,name:str) -> bool:
        # should have at least 2 segments or be a known verb
        if '_' in name and len(name) > 8:
            return True
        common_verbs = {'get','set','create','update','delete','calculate','process'}
        return any(name.startswith(verb) for verb in common_verbs)
    
# Test our quality analyzer
if __name__ == "__main__":
    sample_code = '''def process_data(d, p):
    x = 0
    for i in d:
        if i > p:
            x += i
    print("Result:", x)

data_list = [10, 5, 20, 15, 30]
threshold_value = 12

process_data(data_list, threshold_value)

# Another call with problematic input
process_data([1, 2, "three"], 0)'''
    analyzer = BasicQualityAnalyzer()
    issues = analyzer.analyze_code_quality(sample_code)
    print('\n' + 'CODE QUALITY ANALYSIS' + '='*40)
    for category,problems in issues.items():
        if problems:
            print(f'\n{category.upper().replace('_',' ')} : ')
            for problem in problems:
                print(f'  - {problem}')