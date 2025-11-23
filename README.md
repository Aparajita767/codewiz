# Intelligent Code Analysis 

A comprehensive, ML-enhanced code analysis tool that combines traditional static analysis with machine learning for intelligent code quality assessment.

## Quick Start

```bash
# Clone and install
git clone https://github.com/yourusername/codewiz.git
cd codewiz
pip install -r requirements.txt

# Run demos
python demo_scripts/basic_analysis_demo.py
python demo_scripts/comprehensive_analysis_demo.py

```
## Features

**Static Analysis**: AST parsing, complexity metrics, security checks

**ML Enhancement**: Code embeddings, anomaly detection, quality prediction

**Hybrid Approach**: Combines rule-based and ML analysis

## Basic Usage

```python
from core.result_integrator import CodeAnalysisOrchestrator

analyzer = CodeAnalysisOrchestrator()
code = "your_python_code_here"
results = analyzer.comprehensive_analysis(code)
print(f"Quality Score: {results['overall_assessment']['overall_score']}")

```

## V1.0.0
Static analysis pipeline
ML powered code embeddings
Ensemble anomaly detection
Code quality predictions

## Future updates planned
Extended language support (currently only supports python)
Testing for all ml components and testing performance of models
Web interface with result visualization

## Contributing
Contributions are most welcome!

## License
MIT License
