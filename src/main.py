import os
import sys
from typing import Dict, List
from pathlib import Path

from gitpilot.analyzers import ArchitectureAnalyzer
from gitpilot.models import AIModel
from gitpilot.diff_parser import GitDiffParser
from gitpilot.config import Config

class GitPilot:
    def __init__(self, config_path: str = 'gitpilot.yaml'):
        self.config = Config.load(config_path)
        self.models = self._initialize_models()
        self.parser = GitDiffParser()
    
    def _initialize_models(self) -> List[AIModel]:
        return [AIModel.load(model_name) for model_name in self.config.models]
    
    def analyze_diff(self, diff_content: str) -> Dict:
        parsed_diff = self.parser.parse(diff_content)
        results = {}
        
        for model in self.models:
            results[model.name] = model.analyze(parsed_diff)
        
        return results

def main():
    pilot = GitPilot()
    # Main execution logic

if __name__ == '__main__':
    main()