# Sales Analysis Web Application - Architecture & Dependencies

## Project Overview
This is a Flask-based web application for analyzing sales data from Excel files. Users can upload Excel files with sales data, and the application identifies peak sales dates and generates interactive visualizations.

## Architecture Diagram

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Browser   │    │    Flask App    │    │   SalesAnalyzer │
│                 │    │                 │    │                 │
│  HTML/CSS Form  │◄──►│  app.py         │◄──►│  models.py      │
│                 │    │                 │    │                 │
│  Chart Display  │    │  Routes:        │    │  - load_excel() │
└─────────────────┘    │    / (GET/POST) │    │  - create_graph()│
                       └─────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   Templates     │    │   Libraries     │
                       │                 │    │                 │
                       │  index.html     │    │  pandas         │
                       │  style.css      │    │  plotly         │
                       └─────────────────┘    │  openpyxl       │
                                              │  dataclasses    │
                                              └─────────────────┘
```

## Component Descriptions

### 1. Frontend (Client-side)
- **HTML Template** (`templates/index.html`): Provides the user interface for file upload and results display
- **CSS Styling** (`static/style.css`): Basic styling for the web interface
- **JavaScript**: Plotly.js (embedded in HTML) for interactive chart rendering

### 2. Backend (Server-side)
- **Flask Application** (`app.py`):
  - Handles HTTP requests/responses
  - Manages file uploads
  - Coordinates between UI and data processing
  - Serves static files and templates

- **SalesAnalyzer Class** (`models.py`):
  - Validates and processes Excel data
  - Calculates sales statistics (peak, average, total)
  - Generates interactive Plotly charts
  - Manages data state and validation

### 3. Data Flow
```
File Upload → Validation → Processing → Analysis → Visualization → Display
     ↓           ↓           ↓          ↓            ↓           ↓
  Excel     Column/Date   Pandas     Peak Calc   Plotly      HTML
  File      Checks       DataFrame   Stats       Chart      Template
```

## Dependency Graph

### Direct Dependencies
```
Flask Application (app.py)
├── Flask (web framework)
├── models.SalesAnalyzer (data processing)
└── werkzeug (WSGI utility, via Flask)

SalesAnalyzer (models.py)
├── pandas (data manipulation)
├── plotly (chart generation)
├── openpyxl (Excel reading)
├── dataclasses (data structures)
└── io (byte stream handling)

Tests (test_models.py)
├── unittest (testing framework)
├── models.SalesAnalyzer (unit under test)
└── pandas (test data creation)
```

### Runtime Dependencies
```
Application Runtime
├── Python 3.8+ (runtime environment)
├── Virtual Environment (dependency isolation)
└── Operating System (Windows/Linux/macOS)
```

## File Structure
```
myPythonProject/
├── app.py                 # Main Flask application
├── models.py              # SalesAnalyzer class
├── test_models.py         # Unit tests
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html         # HTML template
├── static/
│   └── style.css          # CSS styles
└── uploads/               # Uploaded files directory
```

## Data Validation Rules
- **File Format**: Excel (.xlsx, .xls)
- **Structure**: Exactly 2 columns (Date, Sales_USD)
- **Data Types**: Date column must be datetime-convertible, Sales_USD must be numeric
- **Minimum Data**: At least 2 rows of valid data
- **Processing**: Invalid rows are dropped, peak sales date is identified

## Security Considerations
- File upload validation (extension checking)
- Input sanitization (pandas data type coercion)
- Error handling (graceful failure on invalid data)
- No database storage (data processed in memory)

## Testing Strategy
- **Unit Tests**: `test_models.py` covers SalesAnalyzer functionality
- **Coverage**: Data loading, validation, calculation, and visualization
- **Mock Data**: In-memory Excel generation for isolated testing
- **CI/CD**: Can be integrated with GitHub Actions or similar

## Deployment Considerations
- **WSGI Server**: Gunicorn/uWSGI for production
- **Static Files**: Nginx/Apache for serving static assets
- **Environment**: Production environment variables
- **Logging**: Structured logging for monitoring
- **Scaling**: Stateless design allows horizontal scaling