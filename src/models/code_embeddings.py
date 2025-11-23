import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import ast
from typing import Dict, List, Any
import hashlib

class CodeEmbedder:
    '''
    Convert code functions into numerical vectors to capture semantic meaning and structure
    '''
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1,2)
        )
        self.function_database = {} #to store function vectors

    def extract_code_features(self,function_node:ast.FunctionDef) -> str:
        '''
        Convert AST structure to a feature str
        captures : 
            -Structure patterns
            -Operation types
            -Naming conventions
            -Complexity signals
        '''
        features = []

        # 1 - function signature features
        features.append(f'func_{function_node.name}')
        features.append(f'args_{len(function_node.args.args)}')

        #2 - Extract operation types
        operations = self._extract_operations(function_node)
        features.extend(operations)

        #3- control flow complexity
        complexity_features = self._extract_complexity_features(function_node)
        features.extend(complexity_features)

        # 4 - return type pattern
        return_pattern = self._extract_return_pattern(function_node)
        features.append(return_pattern)

        return ' '.join(features)
    
    def _extract_operations(self,node:ast.AST) -> List[str]:
        operations = set()
        for child in ast.walk(node):
            if isinstance(child,ast.Call):
                operations.add('operation_call')
            if isinstance(child,ast.Assign):
                operations.add('operation_assign')
            if isinstance(child,ast.AugAssign):
                operations.add('operation_aug_assign')
            if isinstance(child,ast.Compare):
                operations.add('operation_compare')
            if isinstance(child,ast.BinOp):
                operations.add('operation_math')
            if isinstance(child,ast.Subscript):
                operations.add('operation_subscript')

        return list(operations)
    
    def _extract_complexity_features(self,node:ast.AST) -> List[str]:
        '''
        Extract complexity related features
        '''
        features = []
        if_counts = for_counts = while_counts = 0 #initialize counts to 0

        for child in ast.walk(node):
            if isinstance(child, ast.If):
                if_counts += 1
            if isinstance(child, ast.For):
                for_counts += 1
            if isinstance(child,ast.While):
                while_counts += 1
            
        if if_counts > 3:
            features.append('High_conditional_complexity')
        
        if for_counts + while_counts > 2:
            features.append('High_loop_complexity')

        
        return features
    
    def _extract_return_pattern(self,node:ast.FunctionDef) -> str:
        '''
        Analyze pattern of function
        '''
        return_nodes = [n for n in ast.walk(node) if isinstance(n,ast.Return)]

        if not return_nodes:
            return 'return_none'
        elif len(return_nodes) == 1:
            return 'return_single'
        else:
            return 'return_multiple'
        
    
    def add_function_to_database(self,function_node:ast.FunctionDef,quality_score:float = 1.0) : 
        '''
        Store function patterns with quality score
        '''
        features = self.extract_code_features(function_node)

        function_id = f'{function_node.name}_{hashlib.md5(features.encode()).hexdigest()[:8]}'

        self.function_database[function_id] = {
            'features' : features,
            'quality_score' : quality_score,
            'name' : function_node.name,
            'node' : function_node
        }
        return function_id
    
    def fit_embeddings(self):
        '''
        Learn vector space from our function database. This creates our code understanding model
        '''
        if not self.function_database:
            print('No function database to learn from')
            return
        
        # Convert feature strings to numerical value
        feature_texts = [data['features'] for data in self.function_database.values()]
        self.embedding_vectors = self.vectorizer.fit_transform(feature_texts)
        self.is_fitted = True

        print(f'Learned embeddings for {len(feature_texts)} functions')
        print(f'Vocabulary size : {len(self.vectorizer.vocabulary_)}')

    def find_similar_functions(self,target_function:ast.FunctionDef,top_k:int = 5) -> List[Dict]:
        '''
        Find functions with similar patterns
        '''
        if not self.is_fitted:
            print('Embeddings not fitted yet - call fit_embeddings() first')
            return []
        target_features = self.extract_code_features(target_function)
        target_vector = self.vectorizer.transform([target_features])

        #calculate similarity between all known functions
        similarities = cosine_similarity(target_vector,self.embedding_vectors)

        #Get top matches
        similar_indices = similarities[0].argsort()[-top_k:][::-1]
        function_ids = list(self.function_database.keys())

        results = []
        for idx in similar_indices:
            function_id = function_ids[idx]
            function_data = self.function_database[function_id]

        results.append({
            'function_id' : function_id,
            'name' : function_data['name'],
            'similarity' : similarities[0][idx],
            'quality_score' : function_data['quality_score'],
            'features' : function_data['features']
        })

        return results
    
def demonstrate_embeddings():
    '''
    Conceptual demonstration
    '''
    embedder = CodeEmbedder()
    sample_functions = [
        """
def calculate_total(items):
    total = 0
    for item in items:
        total += item.price * item.quantity
    return total
        """,
        """
def process_user_data(users):
    result = []
    for user in users:
        if user.active:
            user_data = {
                'name': user.name,
                'score': user.calculate_score()
            }
            result.append(user_data)
    return result
        """,
        """
def validate_input(data, rules):
    errors = []
    for field, value in data.items():
        if field in rules:
            if not rules[field](value):
                errors.append(f"{field} is invalid")
    return len(errors) == 0, errors
        """
    ]

    print('BUILDING CODE EMBEDDING DEMONSTRATION')
    print('='*50)

    for i,code in enumerate(sample_functions):
        tree = ast.parse(code)
        function_node = [node for node in ast.walk(tree) if isinstance(node,ast.FunctionDef)][0]

        function_id = embedder.add_function_to_database(function_node)
        print(f'Added function {i+1} : {function_node.name} -> {function_id}')

        embedder.fit_embeddings()

        test_code = """
def compute_order_summary(orders):
    summary = 0
    for order in orders:
        if order.valid:
            summary += order.amount
    return summary
    """
        
        test_tree = ast.parse(test_code)
        test_function = [node for node in ast.walk(test_tree) if isinstance(node,ast.FunctionDef)][0]

        print(f'FINDING SIMILAR FUNCTIONS TO : {test_function.name}')
        print('='*50)
        
        similar_functions = embedder.find_similar_functions(test_function)

        for i, similar in enumerate(similar_functions,1):
            print(f'\n{i}. {similar['name']} (similarity : {similar['similarity']:.3f})')
            print(f'Quality score : {similar['quality_score']}')
            print(f'Pattern:{similar['features'][:100]}...')

if __name__ == '__main__':
    demonstrate_embeddings()