import difflib

class DiffAnalyzer:
    def analyze_diff(self, old_text, new_text):
        """Analyze the differences between two text inputs."""
        diff = difflib.unified_diff(old_text.splitlines(), new_text.splitlines(), fromfile='old', tofile='new')
        return ''.join(line + '\
' for line in diff)
