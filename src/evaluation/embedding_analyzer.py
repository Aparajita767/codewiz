import ast
from typing import Dict, List, Any
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__),'..'))
from models.code_embeddings import CodeEmbedder, demonstrate_embeddings

class EmbeddingAnalyzer:
    '''
    Combine rule based checklist with pattern based intelligence
    '''
    def __init__(self):
        self.embedder = CodeEmbedder()
        self.quality_patterns = self._initialize_quality_patterns()

    def _initialize_quality_patterns(self) -> Dict[str,Any]:
        '''
        Define 'good' and 'bad' code patterns
        '''
        return {
            'high_quality_indicators' : [
                'func_calculate','func_process','func_validate',
                'return_single',
                'args_2','args_3'
            ],
            'low_quality_indicators' : [
                'high_conditional_complexity',
                'high_loop_complexity',
                'args_5','args_6','args_7'
            ]
        }
    
    def analyze_with_embeddings(self,code:str) -> Dict[str,Any]:
        '''
        Combined code analysis
        '''
        try:
            tree = ast.parse(code)

        except SyntaxError as e:
            return {'error' : f'Syntax error : {e}'}
        
        analysis_results = {
            'rule_based_issues' : [],
            'pattern_based_insights' : [],
            'similar_function_analysis' : [],
            'overall_quality_score' : 1.0
        }

        functions = [node for node in ast.walk(tree) if isinstance(node,ast.FunctionDef)]

        for function in functions:
            #rule based issues
            rule_issues = self._rule_based_analysis(function)
            analysis_results['rule_based_issues'].extend(rule_issues)

            #pattern based analysis using embedding
            pattern_insights = self._pattern_based_analysis(function)
            analysis_results.extend(pattern_insights)

            #similar function analysis
            if self.embedder.is_fitted:
                similar_analysis = self._similar_function_analysis(function)
                analysis_results.extend(similar_analysis)
            
            return analysis_results
        
    def _rule_based_analysis(self,function:ast.FunctionDef)-> List[str]:
        '''
        Static analysis
        '''
        issues = []
        if len(function.args.args) > 4:
            issues.append(f'Function {function.name} : many arguments ({len(function.args.args)})')

        if len(function.body) > 30:
            issues.append(f'Function {function.name} : long function ({len(function.body)} lines)')

        return issues
    
    def _pattern_based_analysis(self,function : ast.FunctionDef) -> List[str]:
        '''
        Analyze code pattersn using feature extraction
        '''
        insights = []
        features = self.embedder.extract_code_features(function)
        feature_list = features.split()

        #check for quality indicators
        quality_matches = [f for f in feature_list if f in self.quality_patterns['high_quality_indicators']]
        issues_matches = [f for f in feature_list if f in self.quality_patterns['low_quality_indicators']]

        if quality_matches:
            insights.append(f'Good patterns : {', '.join(quality_matches)}')
        
        if issues_matches:
            insights.append(f'Concerning patterns : {', '.join(issues_matches)}')

        return insights
    
    def _similar_function_analysis(self,function:ast.FunctionDef) -> List[str]:
        '''
        Learn from similar functions in database
        '''
        insights = []
        similar_functions =self.embedder.find_similar_functions(function,top_k=3)

        if similar_functions and similar_functions[0]['similarity'] > 0.7:
            best_match = similar_functions[0]
            insights.append(f'Similar to : {best_match['name']} (confidence : {best_match['similarity']:.2f})')
            insights.append(f'Pattern quality score: {best_match['quality_score']}')

        return insights
    
    def train_on_good_examples(self,good_code_examples:List[str]):
        '''
        Train system on good code
        '''
        for i, code in enumerate(good_code_examples):
            try:
                tree = ast.parse(code)
                functions = [node for node in ast.walk(tree) if isinstance(node,ast.FunctionDef)]

                for function in functions:
                    self.embedder.add_function_to_database(function,quality_score=0.9)
            
            except SyntaxError as e:
                continue
        
        self.embedder.fit_embeddings()

def test_basic_functionality():
     simple_code = """
def hello_world():
    return "Hello, World!"
    """
     embedder = CodeEmbedder()

     try:
         tree = ast.parse(simple_code)
         function_node = [node for node in ast.walk(tree) if isinstance(node,ast.FunctionDef)][0]

         features = embedder.extract_code_features(function_node)

         function_id = embedder.add_function_to_database(function_node)

         embedder.fit_embeddings()

     except Exception as e:
         print(f'Error {e}')

if __name__ == '__main__':
    test_basic_functionality()

    demonstrate_embeddings()