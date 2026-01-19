"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from typing import Optional, List
from enum import Enum
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"],
        "category": "Academic"
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"],
        "category": "Academic"
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"],
        "category": "Sports"
    },
    "Soccer Team": {
        "description": "Join the school soccer team and compete in matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": ["liam@mergington.edu", "noah@mergington.edu"],
        "category": "Sports"
    },
    "Basketball Team": {
        "description": "Practice and play basketball with the school team",
        "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["ava@mergington.edu", "mia@mergington.edu"],
        "category": "Sports"
    },
    "Art Club": {
        "description": "Explore your creativity through painting and drawing",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["amelia@mergington.edu", "harper@mergington.edu"],
        "category": "Arts"
    },
    "Drama Club": {
        "description": "Act, direct, and produce plays and performances",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["ella@mergington.edu", "scarlett@mergington.edu"],
        "category": "Arts"
    },
    "Math Club": {
        "description": "Solve challenging problems and participate in math competitions",
        "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
        "max_participants": 10,
        "participants": ["james@mergington.edu", "benjamin@mergington.edu"],
        "category": "Academic"
    },
    "Debate Team": {
        "description": "Develop public speaking and argumentation skills",
        "schedule": "Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 12,
        "participants": ["charlotte@mergington.edu", "henry@mergington.edu"],
        "category": "Academic"
    },
    "GitHub Skills": {
        "description": "Learn practical coding and collaboration skills through GitHub. Part of our GitHub Certifications program to help with college applications",
        "schedule": "Mondays and Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 25,
        "participants": [],
        "category": "Academic"
    }
}

# Enum for sort options
class SortBy(str, Enum):
    name = "name"
    participants = "participants"
    availability = "availability"


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.get("/activities/search")
def search_activities(
    q: Optional[str] = Query(None, description="Search query for activity name or description"),
    category: Optional[str] = Query(None, description="Filter by category (Academic, Sports, Arts)"),
    available: Optional[bool] = Query(None, description="Filter by availability (has space)"),
    sort_by: Optional[SortBy] = Query(SortBy.name, description="Sort results by field"),
    day: Optional[str] = Query(None, description="Filter by day of week (Monday, Tuesday, etc.)")
):
    """
    Search and filter activities with multiple criteria
    
    - **q**: Search term to match against activity names and descriptions
    - **category**: Filter by category (Academic, Sports, Arts)
    - **available**: Show only activities with available spots
    - **sort_by**: Sort by name, participants, or availability
    - **day**: Filter by day of the week in schedule
    """
    results = {}
    
    # Start with all activities
    for activity_name, activity_data in activities.items():
        include = True
        
        # Apply search query filter
        if q:
            search_term = q.lower()
            if (search_term not in activity_name.lower() and 
                search_term not in activity_data["description"].lower()):
                include = False
        
        # Apply category filter
        if category and include:
            if activity_data.get("category", "").lower() != category.lower():
                include = False
        
        # Apply availability filter
        if available is not None and include:
            has_space = len(activity_data["participants"]) < activity_data["max_participants"]
            if available != has_space:
                include = False
        
        # Apply day filter
        if day and include:
            if day.lower() not in activity_data["schedule"].lower():
                include = False
        
        if include:
            results[activity_name] = activity_data
    
    # Sort results
    if sort_by == SortBy.name:
        results = dict(sorted(results.items(), key=lambda x: x[0].lower()))
    elif sort_by == SortBy.participants:
        results = dict(sorted(results.items(), 
                            key=lambda x: len(x[1]["participants"]), 
                            reverse=True))
    elif sort_by == SortBy.availability:
        results = dict(sorted(results.items(), 
                            key=lambda x: x[1]["max_participants"] - len(x[1]["participants"]), 
                            reverse=True))
    
    return {
        "total": len(results),
        "query": q,
        "filters": {
            "category": category,
            "available": available,
            "day": day,
            "sort_by": sort_by
        },
        "results": results
    }


@app.get("/activities/categories")
def get_categories():
    """Get all available activity categories"""
    categories = set()
    for activity_data in activities.values():
        if "category" in activity_data:
            categories.add(activity_data["category"])
    
    return {
        "categories": sorted(list(categories))
    }


@app.get("/activities/suggestions")
def get_search_suggestions(q: str = Query(..., min_length=1, description="Partial search query")):
    """
    Get autocomplete suggestions based on partial query
    """
    suggestions = []
    query_lower = q.lower()
    
    # Search in activity names
    for activity_name in activities.keys():
        if query_lower in activity_name.lower():
            suggestions.append({
                "text": activity_name,
                "type": "activity"
            })
    
    # Search in descriptions (keywords)
    seen_keywords = set()
    for activity_name, activity_data in activities.items():
        words = activity_data["description"].lower().split()
        for word in words:
            if (query_lower in word and 
                len(word) > 3 and 
                word not in seen_keywords):
                suggestions.append({
                    "text": word.capitalize(),
                    "type": "keyword"
                })
                seen_keywords.add(word)
    
    return {
        "query": q,
        "suggestions": suggestions[:10]  # Limit to 10 suggestions
    }


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(
            status_code=400,
            detail="Student is already signed up"
        )

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str):
    """Unregister a student from an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is signed up
    if email not in activity["participants"]:
        raise HTTPException(
            status_code=400,
            detail="Student is not signed up for this activity"
        )

    # Remove student
    activity["participants"].remove(email)
    return {"message": f"Unregistered {email} from {activity_name}"}