# src/filters.py
from typing import List, Dict, Any
from enum import Enum

class SortOption(Enum):
    ALPHABETICAL = "alphabetical"
    POPULARITY = "popularity"
    DATE = "date"

class FilterManager:
    def __init__(self):
        self.available_categories = set()
        self.available_schedules = set()
        
    def update_available_filters(self, activities: List[Dict]) -> None:
        """Update available filter options based on current activities"""
        for activity in activities:
            if 'category' in activity:
                self.available_categories.add(activity['category'])
            if 'schedule' in activity:
                self.available_schedules.add(activity['schedule'])
    
    def get_filter_options(self) -> Dict[str, Any]:
        """Get all available filter options"""
        return {
            'categories': sorted(list(self.available_categories)),
            'schedules': sorted(list(self.available_schedules)),
            'sort_options': [option.value for option in SortOption]
        }
    
    def validate_filters(self, filters: Dict) -> Dict:
        """Validate and sanitize filter inputs"""
        valid_filters = {}
        
        if 'category' in filters and filters['category'] in self.available_categories:
            valid_filters['category'] = filters['category']
        
        if 'schedule' in filters and filters['schedule'] in self.available_schedules:
            valid_filters['schedule'] = filters['schedule']
        
        if 'availability' in filters and isinstance(filters['availability'], bool):
            valid_filters['availability'] = filters['availability']
        
        if 'min_popularity' in filters:
            try:
                valid_filters['min_popularity'] = int(filters['min_popularity'])
            except (ValueError, TypeError):
                pass
        
        return valid_filters