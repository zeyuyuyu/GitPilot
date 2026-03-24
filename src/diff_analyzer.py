"""Analyzes semantic differences between webpage versions and scores their significance."""

from difflib import SequenceMatcher
from bs4 import BeautifulSoup
import re
import math

class DiffAnalyzer:
    def __init__(self):
        self.importance_weights = {
            'title': 3.0,
            'header': 2.0,
            'link': 1.5,
            'text': 1.0
        }

    def calculate_semantic_diff(self, old_html: str, new_html: str) -> dict:
        """Analyzes semantic differences between two HTML versions and returns impact metrics."""
        old_soup = BeautifulSoup(old_html, 'html.parser')
        new_soup = BeautifulSoup(new_html, 'html.parser')

        changes = {
            'title_changes': self._compare_titles(old_soup, new_soup),
            'header_changes': self._compare_headers(old_soup, new_soup),
            'link_changes': self._compare_links(old_soup, new_soup),
            'content_changes': self._compare_content(old_soup, new_soup)
        }

        impact_score = self._calculate_impact_score(changes)

        return {
            'changes': changes,
            'impact_score': impact_score,
            'change_summary': self._generate_change_summary(changes)
        }

    def _compare_titles(self, old_soup: BeautifulSoup, new_soup: BeautifulSoup) -> dict:
        old_title = old_soup.title.string if old_soup.title else ''
        new_title = new_soup.title.string if new_soup.title else ''
        similarity = SequenceMatcher(None, old_title, new_title).ratio()
        return {
            'changed': similarity < 1.0,
            'similarity': similarity,
            'old': old_title,
            'new': new_title
        }

    def _compare_headers(self, old_soup: BeautifulSoup, new_soup: BeautifulSoup) -> list:
        old_headers = [h.text.strip() for h in old_soup.find_all(['h1', 'h2', 'h3'])]
        new_headers = [h.text.strip() for h in new_soup.find_all(['h1', 'h2', 'h3'])]
        
        changes = []
        for i, (old, new) in enumerate(zip(old_headers, new_headers)):
            if old != new:
                changes.append({
                    'index': i,
                    'old': old,
                    'new': new,
                    'similarity': SequenceMatcher(None, old, new).ratio()
                })
        return changes

    def _compare_links(self, old_soup: BeautifulSoup, new_soup: BeautifulSoup) -> dict:
        old_links = set(a.get('href', '') for a in old_soup.find_all('a'))
        new_links = set(a.get('href', '') for a in new_soup.find_all('a'))
        
        return {
            'added': list(new_links - old_links),
            'removed': list(old_links - new_links),
            'total_changes': len(new_links ^ old_links)
        }

    def _compare_content(self, old_soup: BeautifulSoup, new_soup: BeautifulSoup) -> dict:
        def get_main_content(soup):
            # Remove script, style, and nav elements
            for tag in soup(['script', 'style', 'nav']):
                tag.decompose()
            return ' '.join(soup.stripped_strings)

        old_content = get_main_content(old_soup)
        new_content = get_main_content(new_soup)
        
        similarity = SequenceMatcher(None, old_content, new_content).ratio()
        word_diff = abs(len(old_content.split()) - len(new_content.split()))
        
        return {
            'similarity': similarity,
            'word_count_diff': word_diff,
            'significant_change': similarity < 0.9
        }

    def _calculate_impact_score(self, changes: dict) -> float:
        """Calculate overall impact score from 0-10 based on weighted changes."""
        score = 0.0
        
        # Title changes
        if changes['title_changes']['changed']:
            score += (1 - changes['title_changes']['similarity']) * self.importance_weights['title']

        # Header changes
        header_change_impact = sum(1 - c['similarity'] for c in changes['header_changes'])
        score += header_change_impact * self.importance_weights['header']

        # Link changes
        link_change_ratio = changes['link_changes']['total_changes'] / 10  # Normalize by assuming 10 changes is significant
        score += min(1.0, link_change_ratio) * self.importance_weights['link']

        # Content changes
        content_impact = (1 - changes['content_changes']['similarity']) * self.importance_weights['text']
        score += content_impact

        # Normalize to 0-10 scale
        return min(10.0, score * 2)

    def _generate_change_summary(self, changes: dict) -> str:
        """Generate a human-readable summary of the changes."""
        summary_parts = []

        if changes['title_changes']['changed']:
            summary_parts.append(f"Title changed (similarity: {changes['title_changes']['similarity']:.2f})")

        if changes['header_changes']:
            summary_parts.append(f"{len(changes['header_changes'])} headers modified")

        link_changes = changes['link_changes']
        if link_changes['added'] or link_changes['removed']:
            summary_parts.append(
                f"Links modified: {len(link_changes['added'])} added, {len(link_changes['removed'])} removed")

        content = changes['content_changes']
        if content['significant_change']:
            summary_parts.append(
                f"Significant content changes detected (similarity: {content['similarity']:.2f}, "
                f"word diff: {content['word_count_diff']})")

        return '; '.join(summary_parts) if summary_parts else 'No significant changes detected'