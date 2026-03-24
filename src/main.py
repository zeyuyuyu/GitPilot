#!/usr/bin/env python3

import argparse
import json
import os
from pathlib import Path

class GitPilot:
    def __init__(self, config_path=None):
        self.config_path = config_path or Path.home() / '.gitpilot.json'
        self.config = self.load_config()

    def load_config(self):
        """Load configuration from JSON file or create default"""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                return json.load(f)
        return self.create_default_config()

    def create_default_config(self):
        """Create and save default configuration"""
        config = {
            'github_token': '',
            'default_branch': 'main',
            'auto_commit': True,
            'commit_prefix': 'feat:'
        }
        self.save_config(config)
        return config

    def save_config(self, config):
        """Save configuration to JSON file"""
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=2)

    def run(self, args):
        """Main execution logic"""
        if args.configure:
            self.interactive_configure()
        elif args.show_config:
            self.display_config()
        # Add more command handlers here

    def interactive_configure(self):
        """Interactive configuration setup"""
        print('GitPilot Configuration Setup')
        self.config['github_token'] = input('Enter GitHub token: ') or self.config.get('github_token', '')
        self.config['default_branch'] = input('Enter default branch [main]: ') or 'main'
        self.save_config(self.config)
        print('Configuration saved successfully!')

    def display_config(self):
        """Display current configuration"""
        print('Current GitPilot Configuration:')
        for key, value in self.config.items():
            if key == 'github_token' and value:
                value = '********'
            print(f'{key}: {value}')

def main():
    parser = argparse.ArgumentParser(description='GitPilot - Automated Git Operations')
    parser.add_argument('--configure', action='store_true', help='Configure GitPilot settings')
    parser.add_argument('--show-config', action='store_true', help='Display current configuration')
    
    args = parser.parse_args()
    pilot = GitPilot()
    pilot.run(args)

if __name__ == '__main__':
    main()
