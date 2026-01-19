# Mergington High School Activities API

A super simple FastAPI application that allows students to view and sign up for extracurricular activities.

## Features

- View all available extracurricular activities
- Sign up for activities
- **🔍 NEW: Search and filter activities**
- **🔍 NEW: Sort activities by multiple criteria**
- **🔍 NEW: Autocomplete suggestions**

## Getting Started

1. Install the dependencies:
```bash
   pip install -r requirements.txt
```

2. Run the application:
```bash
   uvicorn app:app --reload
```

3. Open your browser and go to:
   - API documentation: http://localhost:8000/docs
   - Alternative documentation: http://localhost:8000/redoc
   - Main page: http://localhost:8000

## API Endpoints

### Core Endpoints

| Method | Endpoint                                                          | Description                                                         |
| ------ | ----------------------------------------------------------------- | ------------------------------------------------------------------- |
| GET    | `/activities`                                                     | Get all activities with their details and current participant count |
| POST   | `/activities/{activity_name}/signup?email=student@mergington.edu` | Sign up for an activity                                             |
| DELETE | `/activities/{activity_name}/unregister?email=student@mergington.edu` | Unregister from an activity                                    |

### 🔍 New Search & Filter Endpoints

| Method | Endpoint                          | Description                                    |
| ------ | --------------------------------- | ---------------------------------------------- |
| GET    | `/activities/search`              | Search and filter activities with multiple criteria |
| GET    | `/activities/categories`          | Get all available activity categories          |
| GET    | `/activities/suggestions?q={query}` | Get autocomplete suggestions                 |

## 🔍 Search & Filter Features

### Search Activities

The `/activities/search` endpoint supports multiple query parameters:

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `q` | string | Search term (searches name and description) | `programming` |
| `category` | string | Filter by category | `Academic`, `Sports`, `Arts` |
| `available` | boolean | Show only activities with open spots | `true`, `false` |
| `day` | string | Filter by day of week | `Monday`, `Tuesday`, etc. |
| `sort_by` | string | Sort results | `name`, `participants`, `availability` |

### Usage Examples
```bash
# Search for programming activities
curl "http://localhost:8000/activities/search?q=programming"

# Get all Sports activities
curl "http://localhost:8000/activities/search?category=Sports"

# Find available activities on Monday
curl "http://localhost:8000/activities/search?available=true&day=Monday"

# Get Academic activities sorted by popularity
curl "http://localhost:8000/activities/search?category=Academic&sort_by=participants"

# Combined filters: Available Academic activities on Monday
curl "http://localhost:8000/activities/search?category=Academic&available=true&day=Monday&sort_by=name"
```

### Response Format
```json
{
  "total": 1,
  "query": "programming",
  "filters": {
    "category": null,
    "available": null,
    "day": null,
    "sort_by": "name"
  },
  "results": {
    "Programming Class": {
      "description": "Learn programming fundamentals and build software projects",
      "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
      "max_participants": 20,
      "participants": ["emma@mergington.edu", "sophia@mergington.edu"],
      "category": "Academic"
    }
  }
}
```

### Get Categories
```bash
# Get all available categories
curl "http://localhost:8000/activities/categories"
```

Response:
```json
{
  "categories": ["Academic", "Arts", "Sports"]
}
```

### Autocomplete Suggestions
```bash
# Get search suggestions
curl "http://localhost:8000/activities/suggestions?q=pro"
```

Response:
```json
{
  "query": "pro",
  "suggestions": [
    {
      "text": "Programming Class",
      "type": "activity"
    },
    {
      "text": "Programming",
      "type": "keyword"
    }
  ]
}
```

## Data Model

The application uses a simple data model with meaningful identifiers:

1. **Activities** - Uses activity name as identifier:
   - Description
   - Schedule
   - Maximum number of participants allowed
   - List of student emails who are signed up
   - **Category** (Academic, Sports, Arts)

2. **Students** - Uses email as identifier:
   - Name
   - Grade level

All data is stored in memory, which means data will be reset when the server restarts.

## Testing

Run the test suite (if tests are included):
```bash
# Install test dependencies
pip install pytest httpx

# Run all tests
pytest test_search.py -v

# Run specific test
pytest test_search.py::test_search_by_query -v
```

## Available Activities

The system includes the following activities:

**Academic:**
- Chess Club
- Programming Class
- Math Club
- Debate Team
- GitHub Skills

**Sports:**
- Gym Class
- Soccer Team
- Basketball Team

**Arts:**
- Art Club
- Drama Club

## Interactive Documentation

Once the server is running, explore the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Try out the search features directly in the Swagger UI!

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

See LICENSE file for details.