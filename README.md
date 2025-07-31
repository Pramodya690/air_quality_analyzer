# Air Quality Analysis  - Setup & Usage Guide

### Features
  -	Analyze air quality with user queries.
  -	Dynamically render results: Table (type: 'table') or Text (type: 'text').
  -	Display explanatory text from the backend.
  -	Styled using Tailwind CSS.
  
## Frontend setup 
### Installation & Setup
  1. Clone the Repository:
     git clone https://github.com/Pramodya690/air_quality_analyzer.git  
  2. Install Node Dependencies:
     npm install
     
### Tailwind CSS Setup
  - This app uses Tailwind CSS v3.4.1. It's pre-configured.
  - If setting up manually:
     - npm install -D tailwindcss@3.4.1 postcss autoprefixer
     - npx tailwindcss init -p
  - Update tailwind.config.js:
     - content: ["./src/**/*.{js,jsx,ts,tsx}"]
  - Add to src/index.css:
     - @tailwind base;
     - @tailwind components;
     - @tailwind utilities;
     
### Running the frontend
  - npm run dev
  - App will run at http://localhost:5173/
  
### Backend API Integration
  - Ensure your backend is running at http://localhost:8000.
  - Update the axios.post URL in App.jsx if necessary.
  
  ## Expected sample API Response Formats
  - Text Response:
   { "result": { "output": { "type": "text", "data": ["room3", "room2"] }, "explanation": "..." } }
  - Table Response:
   { "result": { "output": { "type": "table", "data": [ { "hour": 0, "average_temperature": 23.1 } ], "columns": ["hour", "average_temperature"] }, "explanation": "..." } }

## Backend set up
---
### Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/)
- [Poetry](https://python-poetry.org/)
- [Pandas](https://pandas.pydata.org/)
- [NumPy](https://numpy.org/)
- [OpenAI API](https://platform.openai.com/)


### Prerequisites

- Python 3.9+
- [Poetry](https://python-poetry.org/docs/#installation)

### Installation & Setup

- Go to the backend directory
  - cd backend

### Install dependencies
- poetry install

### Running the backend
 - poetry run uvicorn main:app --reload
 - App will run at http://localhost:8000/
  
### Example User Query
  What is the average temperature of each room in the morning and evening?
  
### Questions?
  Reach out via GitHub issues or discussions.
