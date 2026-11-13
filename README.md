# AI-Powered SQL Insight Agent

**An AI-powered SQL Copilot for Conversational Data Analysis**

The AI-Powered SQL Insight Agent is a Python-based application that allows users to interact with a MySQL database using natural-language questions. It uses Generative AI to convert questions into SQL queries, retrieves data, performs analysis, and presents results through explanations and visualizations.

The project was initially developed as a self-learning initiative to strengthen SQL, database management, data analysis, and Generative AI skills.

## Key Features

- **Natural Language to SQL:** Ask questions in plain English instead of writing SQL manually.
- **Schema-Aware SQL Generation:** Uses database schema information to generate relevant SQL queries.
- **SQL Validation:** Validates generated queries and applies read-only query restrictions.
- **MySQL Integration:** Connects to a MySQL database and executes validated queries.
- **Data Analysis:** Uses Pandas to analyze query results, including numerical summaries and data-quality observations.
- **AI-Generated Insights:** Uses Google Gemini to explain query results in understandable language.
- **Data Visualization:** Generates interactive charts using Plotly.
- **Interactive Web Interface:** Provides a conversational interface built with Streamlit.

## How It Works

1. The user enters a question in natural language.
2. The application retrieves the database schema.
3. Google Gemini generates a SQL query based on the question and schema.
4. The generated query passes through SQL validation.
5. The validated query is executed against the MySQL database using read-only database access.
6. Pandas analyzes the returned data.
7. Gemini generates a natural-language explanation of the results.
8. Plotly creates a suitable visualization when possible.
9. Results, insights, and charts are displayed in the Streamlit interface.

## Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Database | MySQL |
| Generative AI | Google Gemini API |
| Data Analysis | Pandas |
| Data Visualization | Plotly |
| Web Framework | Streamlit |
| Database Connectivity | SQLAlchemy, PyMySQL |
| SQL Validation | SQLGlot |
| Environment Configuration | python-dotenv |

## Project Structure

```text
AI-SQL-Insight-Agent/
│
├── agent/
│   ├── sql_generator.py
│   ├── query_runner.py
│   ├── result_analyzer.py
│   └── insight_generator.py
│
├── database/
│   └── connection.py
│
├── tools/
│   └── database_tools.py
│
├── visualization/
│   └── chart_generator.py
│
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

*The structure above highlights the main project components; additional files may be present.*

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/AI-SQL-Insight-Agent.git
cd AI-SQL-Insight-Agent
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root using `.env.example` as a reference.

Add your own MySQL connection details and Gemini API key. Never commit your actual `.env` file.

### 5. Configure the MySQL database

Create and populate the MySQL database using the required tables and sample data.

The application expects the configured database and the necessary tables to be available before running.

### 6. Run the application

```bash
python -m streamlit run app.py
```

Open the local URL displayed in your terminal, usually:

```text
http://localhost:8501
```

## Database

The current demonstration project uses a MySQL sales database with tables such as:

- `categories`
- `products`
- `customers`
- `orders`
- `order_items`
- `payments`

The application uses the configured database schema to support natural-language SQL generation and data analysis.

## Future Enhancements

The following capabilities are planned for future development:

- Retrieval-Augmented Generation (RAG) for retrieving relevant business knowledge and database documentation.
- CSV and Excel file upload and analysis.
- Machine Learning capabilities such as forecasting, clustering, and anomaly detection where appropriate.
- Support for additional databases such as PostgreSQL.
- Automated analytical reports and more advanced data exploration.
- Improved conversational context and follow-up analysis.

## Learning Outcomes

Through this project, I am developing practical experience in:

- SQL query generation and database operations.
- Python-based data analysis.
- Generative AI and LLM integration.
- Prompt engineering and schema-aware query generation.
- SQL validation and read-only database access.
- Interactive dashboards and data visualization.

## Author

**Nandhana C. Reghu**

- LinkedIn: https://www.linkedin.com/in/nandhana-c-reghu/
- GitHub: https://github.com/nandhanac

---

*This project is a learning-oriented AI SQL Copilot prototype designed to assist with conversational database querying and analysis. It is not intended to replace database professionals or data analysts.*