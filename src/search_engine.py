# src/search_engine.py
from typing import List, Dict, Any, Optional
import json
from datetime import datetime

class SearchEngine:
    def __init__(self):
        self.activities = []
        self.search_index = {}
        self.recent_searches = []
        
    def index_activity(self, activity: Dict[str, Any]) -> None:
        """Index an activity for faster searching"""
        activity_id = activity.get('id')
        searchable_text = self._create_searchable_text(activity)
        
        # Create inverted index
        words = searchable_text.lower().split()
        for word in words:
            if word not in self.search_index:
                self.search_index[word] = set()
            self.search_index[word].add(activity_id)
    
    def _create_searchable_text(self, activity: Dict[str, Any]) -> str:
        """Combine all searchable fields into one text"""
        searchable_fields = [
            activity.get('name', ''),
            activity.get('description', ''),
            activity.get('category', ''),
            ' '.join(activity.get('tags', []))
        ]
        return ' '.join(filter(None, searchable_fields))
    
    def search(self, query: str, filters: Optional[Dict] = None) -> List[Dict]:
        """Perform full-text search with optional filters"""
        if not query.strip():
            return self.filter_activities(filters) if filters else self.activities
        
        # Add to recent searches
        self._add_recent_search(query)
        
        # Find matching activity IDs
        query_words = query.lower().split()
        matching_ids = self._find_matching_ids(query_words)
        
        # Get full activity objects
        results = [
            activity for activity in self.activities 
            if activity.get('id') in matching_ids
        ]
        
        # Apply filters if provided
        if filters:
            results = self._apply_filters(results, filters)
        
        # Rank results by relevance
        results = self._rank_results(results, query)
        
        return results
    
    def _find_matching_ids(self, query_words: List[str]) -> set:
        """Find activity IDs that match query words"""
        if not query_words:
            return set()
        
        # Start with first word matches
        matching_ids = self.search_index.get(query_words[0], set()).copy()
        
        # Intersect with other word matches (AND logic)
        for word in query_words[1:]:
            matching_ids &= self.search_index.get(word, set())
        
        return matching_ids
    
    def _apply_filters(self, activities: List[Dict], filters: Dict) -> List[Dict]:
        """Apply filters to activity list"""
        filtered = activities
        
        if 'category' in filters:
            filtered = [a for a in filtered if a.get('category') == filters['category']]
        
        if 'availability' in filters:
            filtered = [a for a in filtered if a.get('available') == filters['availability']]
        
        if 'schedule' in filters:
            filtered = [a for a in filtered if a.get('schedule') == filters['schedule']]
        
        if 'min_popularity' in filters:
            filtered = [a for a in filtered if a.get('popularity', 0) >= filters['min_popularity']]
        
        return filtered
    
    def _rank_results(self, results: List[Dict], query: str) -> List[Dict]:
        """Rank results by relevance"""
        query_lower = query.lower()
        
        def relevance_score(activity: Dict) -> float:
            score = 0.0
            
            # Exact match in name gets highest score
            if query_lower in activity.get('name', '').lower():
                score += 10.0
            
            # Match in description
            if query_lower in activity.get('description', '').lower():
                score += 5.0
            
            # Match in category
            if query_lower in activity.get('category', '').lower():
                score += 3.0
            
            # Popularity boost
            score += activity.get('popularity', 0) * 0.1
            
            return score
        
        return sorted(results, key=relevance_score, reverse=True)
    
    def _add_recent_search(self, query: str) -> None:
        """Track recent searches (max 10)"""
        if query in self.recent_searches:
            self.recent_searches.remove(query)
        self.recent_searches.insert(0, query)
        self.recent_searches = self.recent_searches[:10]
    
    def get_suggestions(self, partial_query: str) -> List[str]:
        """Get autocomplete suggestions"""
        if not partial_query:
            return self.recent_searches[:5]
        
        partial_lower = partial_query.lower()
        suggestions = []
        
        # Check recent searches first
        for search in self.recent_searches:
            if partial_lower in search.lower():
                suggestions.append(search)
        
        # Check indexed words
        for word in self.search_index.keys():
            if word.startswith(partial_lower) and word not in suggestions:
                suggestions.append(word)
        
        return suggestions[:5]
    
    def filter_activities(self, filters: Dict) -> List[Dict]:
        """Filter activities without search"""
        return self._apply_filters(self.activities, filters)
    
    def sort_activities(self, activities: List[Dict], sort_by: str = 'alphabetical') -> List[Dict]:
        """Sort activities by specified criteria"""
        if sort_by == 'alphabetical':
            return sorted(activities, key=lambda x: x.get('name', '').lower())
        elif sort_by == 'popularity':
            return sorted(activities, key=lambda x: x.get('popularity', 0), reverse=True)
        elif sort_by == 'date':
            return sorted(activities, key=lambda x: x.get('created_at', ''), reverse=True)
        
        return activities