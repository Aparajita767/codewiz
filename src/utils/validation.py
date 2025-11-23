# portfolio/1_code_ai/src/utils/validation.py
"""
Validation utilities for code analysis
"""
import ast
from typing import Dict, List, Any, Optional, Tuple
import re

class CodeValidator:
    """
    Validation utilities for code analysis pipeline
    """
    
    @staticmethod
    def validate_python_syntax(code: str) -> Tuple[bool, Optional[str]]:
        """
        Validate Python syntax and return error if invalid
        """
        try:
            ast.parse(code)
            return True, None
        except SyntaxError as e:
            return False, f"Syntax error: {e}"
    
    @staticmethod
    def validate_code_security(code: str) -> List[str]:
        """
        Basic security validation for dangerous patterns
        """
        security_issues = []
        
        # Dangerous imports
        dangerous_imports = [
            'os.system', 'subprocess.call', 'eval', 'exec', 
            'pickle.loads', 'marshal.loads', 'yaml.load'
        ]
        
        for dangerous_import in dangerous_imports:
            if dangerous_import in code:
                security_issues.append(f"Dangerous import detected: {dangerous_import}")
        
        # Potential code injection
        if 'input()' in code and any(op in code for op in ['eval', 'exec']):
            security_issues.append("Potential code injection with input() and eval/exec")
        
        return security_issues
    
    @staticmethod
    def validate_analysis_input(code: str, analysis_type: str) -> Tuple[bool, List[str]]:
        """
        Validate input for code analysis
        """
        issues = []
        
        if not code or not code.strip():
            issues.append("Code input cannot be empty")
            return False, issues
        
        if len(code) > 10000:  # 10KB limit
            issues.append("Code exceeds maximum size limit (10KB)")
        
        # Syntax validation
        is_valid_syntax, syntax_error = CodeValidator.validate_python_syntax(code)
        if not is_valid_syntax:
            issues.append(syntax_error)
        
        # Security validation for certain analysis types
        if analysis_type in ['security', 'comprehensive']:
            security_issues = CodeValidator.validate_code_security(code)
            issues.extend(security_issues)
        
        return len(issues) == 0, issues
    
    @staticmethod
    def validate_analysis_results(results: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Validate analysis results structure and content
        """
        issues = []
        
        required_sections = [
            'structural_analysis',
            'metric_analysis', 
            'security_analysis',
            'data_flow_analysis',
            'overall_assessment'
        ]
        
        for section in required_sections:
            if section not in results:
                issues.append(f"Missing required section: {section}")
        
        # Validate overall assessment structure
        if 'overall_assessment' in results:
            assessment = results['overall_assessment']
            if 'overall_score' not in assessment:
                issues.append("Overall assessment missing score")
            if 'quality_level' not in assessment:
                issues.append("Overall assessment missing quality level")
        
        return len(issues) == 0, issues

class PerformanceValidator:
    """
    Performance validation utilities
    """
    
    @staticmethod
    def measure_analysis_time(analysis_function, *args, **kwargs) -> Dict[str, Any]:
        """
        Measure analysis execution time
        """
        import time
        
        start_time = time.time()
        result = analysis_function(*args, **kwargs)
        end_time = time.time()
        
        execution_time = end_time - start_time
        
        return {
            'result': result,
            'execution_time_seconds': execution_time,
            'performance_level': PerformanceValidator._assess_performance(execution_time)
        }
    
    @staticmethod
    def _assess_performance(execution_time: float) -> str:
        """Assess performance level based on execution time"""
        if execution_time < 1.0:
            return "Excellent"
        elif execution_time < 3.0:
            return "Good"
        elif execution_time < 10.0:
            return "Acceptable"
        else:
            return "Slow"
    
    @staticmethod
    def validate_memory_usage() -> Dict[str, Any]:
        """
        Validate memory usage (simplified implementation)
        """
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        memory_info = process.memory_info()
        
        return {
            'memory_rss_mb': memory_info.rss / 1024 / 1024,
            'memory_vms_mb': memory_info.vms / 1024 / 1024,
            'memory_percent': process.memory_percent()
        }