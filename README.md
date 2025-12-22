# End to End ML Project

A comprehensive machine learning pipeline project built with Python, featuring data ingestion, transformation, model training, and deployment capabilities with PostgreSQL integration.

## 📋 Table of Contents
- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Features](#features)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Usage](#usage)
- [Pipeline Documentation](#pipeline-documentation)
- [Database Setup](#database-setup)
- [Contributing](#contributing)

---

## Project Overview

This is a production-ready ML project that implements a complete machine learning workflow from data ingestion to model deployment. The project follows best practices for modular design, error handling, logging, and database integration.

**Author**: Hara Prasad  
**Version**: 0.1.0

---

## Architecture

The project is built on two primary pipelines:

### 1. **Training Pipeline**
Handles the complete ML workflow:
- **Data Ingestion**: Reads data from PostgreSQL, CSV, or MySQL
- **Data Transformation**: Feature engineering and preprocessing
- **Model Training**: Model fitting and optimization
- **Model Evaluation**: Performance metrics and validation
- **Model Monitoring**: Track model performance over time

### 2. **Prediction Pipeline**
Generates predictions from trained models:
- Accepts client input
- Processes through trained model
- Returns predictions (can be integrated as REST API)

---

## Features

✅ **Multi-Source Data Ingestion**
- PostgreSQL database support
- CSV file support
- Extensible for MySQL, MongoDB, etc.

✅ **Robust Error Handling**
- Custom exception handling
- Detailed logging system
- Error traceability

✅ **Modular Component Architecture**
- Data Ingestion
- Data Transformation
- Model Training
- Model Monitoring

✅ **Production-Ready**
- Environment variable configuration
- Logging and monitoring
- DVC integration for data versioning
- SQL scripts for database setup

---

## Installation

### Prerequisites
- Python 3.8+
- PostgreSQL 12+ (optional, for database features)
- pip or uv package manager

### Setup with `uv` (Recommended)

```bash
# Install uv package manager
pip install uv

# Navigate to project directory
cd d:\Python\mlproject

# Create virtual environment
uv venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate

# On Linux/Mac:
source .venv/bin/activate

# Install dependencies
uv add -r requirements.txt
```

### Setup with `pip`

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate

# On Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## Project Structure

```
mlproject/
├── app.py                          # Main application entry point
├── main.py                         # Alternative entry point
├── template.py                     # Project template/configuration
├── setup.py                        # Package setup configuration
├── pyproject.toml                  # Project metadata
├── requirements.txt                # Project dependencies
├── README.md                       # This file
│
├── artifact/                       # Data storage
│   ├── raw.csv                    # Raw data
│   ├── train.csv                  # Training dataset
│   ├── test.csv                   # Testing dataset
│   ├── train.parquet              # Parquet format training data
│   ├── test.parquet               # Parquet format testing data
│   ├── train.csv.dvc              # DVC version control
│   ├── test.csv.dvc
│   └── raw.csv.dvc
│
├── logs/                           # Application logs
│   └── [log files]
│
├── source/
│   └── mlproject/
│       ├── __init__.py
│       ├── expection.py            # Custom exception handling
│       ├── logger.py               # Logging configuration
│       ├── utils.py                # Utility functions
│       │
│       ├── components/
│       │   ├── __init__.py
│       │   ├── data_ingestion.py   # Data reading & splitting
│       │   ├── data_transformation.py  # Feature engineering
│       │   ├── model_training.py   # Model training logic
│       │   └── model_monitoring.py # Performance monitoring
│       │
│       ├── database/
│       │   ├── __init__.py
│       │   └── postgres.py         # PostgreSQL connection & operations
│       │
│       └── pipeline/
│           ├── __init__.py
│           ├── training_pipeline.py    # ML training workflow
│           └── prediction_pipeline.py  # Inference workflow
│
└── sql script/
    └── Script.sql                  # Database initialization scripts
```

---

## Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Database Configuration
DATABASE_URL=postgresql+psycopg://username:password@localhost:5432/mlproject
# OR use individual components:
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=mlproject

# Application Settings
LOG_LEVEL=INFO
```

### Database Setup

1. **Create PostgreSQL Database**:
```sql
CREATE DATABASE mlproject;
```

2. **Run SQL Scripts**:
Execute the scripts in `sql script/Script.sql` to initialize tables:
```bash
psql -U postgres -d mlproject -f "sql script/Script.sql"
```

3. **Update `.env`** with your PostgreSQL credentials

---

## Usage

### Running the Training Pipeline

```bash
# Using Python
python app.py

# Using uv
uv run app.py

# Using module execution
python -m source.mlproject.pipeline.training_pipeline
```

### Running the Prediction Pipeline

```python
from source.mlproject.pipeline.prediction_pipeline import PredictionPipeline

# Initialize predictor
predictor = PredictionPipeline()

# Make predictions
predictions = predictor.predict(input_data)
```

### Using Individual Components

```python
from source.mlproject.components.data_ingestion import DataIngestion
from source.mlproject.components.data_transformation import DataTransformation
from source.mlproject.components.model_training import ModelTrainer

# Data Ingestion
ingestion = DataIngestion()
train_data_path, test_data_path = ingestion.initiate_data_ingestion()

# Data Transformation
transformer = DataTransformation()
train_arr, test_arr = transformer.initiate_data_transformation(
    train_path=train_data_path,
    test_path=test_data_path
)

# Model Training
trainer = ModelTrainer()
model = trainer.initiate_model_training(X_train=train_arr[:, :-1], y_train=train_arr[:, -1])
```

---

## Pipeline Documentation

### Training Pipeline (`source/mlproject/pipeline/training_pipeline.py`)

**Workflow**:
1. **Data Ingestion** - Read from PostgreSQL/CSV, split into train/test
2. **Data Transformation** - Feature engineering, encoding, scaling
3. **Model Training** - Train ML models with hyperparameter tuning
4. **Model Evaluation** - Calculate metrics (accuracy, precision, recall, F1)
5. **Model Monitoring** - Track model performance and drift
6. **Model Persistence** - Save trained model and artifacts

**Key Methods**:
- `initiate_training_pipeline()` - Main entry point

### Prediction Pipeline (`source/mlproject/pipeline/prediction_pipeline.py`)

**Workflow**:
1. Load trained model from artifacts
2. Preprocess input data using saved transformers
3. Generate predictions
4. Return results in specified format

**Key Methods**:
- `predict(data)` - Generate predictions

### Components

#### Data Ingestion (`components/data_ingestion.py`)
- Reads data from PostgreSQL using SQLAlchemy
- Performs train-test split (typically 80-20)
- Saves raw, train, and test data to artifact directory
- Supports both CSV and Parquet formats

#### Data Transformation (`components/data_transformation.py`)
- Handles missing values
- Encodes categorical variables
- Scales numerical features
- Applies feature engineering
- Creates preprocessing pipelines

#### Model Training (`components/model_training.py`)
- Trains multiple ML models
- Performs hyperparameter tuning
- Model selection based on performance metrics
- Saves best model to artifacts

#### Model Monitoring (`components/model_monitoring.py`)
- Tracks model performance over time
- Detects data drift
- Generates monitoring reports
- Alerts for performance degradation

---

## Database Setup

### PostgreSQL Connection

The project uses SQLAlchemy with psycopg2 driver for database operations:

```python
from source.mlproject.database.postgres import read_sql_data, save_to_sql
import pandas as pd

# Read data from database
df = read_sql_data()

# Save processed data back to database
save_to_sql(df, table_name='predictions')
```

### Database Configuration

Update your `.env` file:
```env
DB_USER=postgres
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=mlproject
```

Or use a single URL:
```env
DATABASE_URL=postgresql+psycopg://postgres:password@localhost:5432/mlproject
```

---

## Logging & Error Handling

### Custom Logging

The project uses a centralized logging system in `source/mlproject/logger.py`:

```python
from source.mlproject.logger import logging

logging.info("Starting data ingestion process")
logging.error("Error occurred during processing", exc_info=True)
```

### Custom Exceptions

Handle errors with custom exceptions in `source/mlproject/expection.py`:

```python
from source.mlproject.expection import CustomException

try:
    # Your code here
    pass
except Exception as e:
    raise CustomException(e, sys)
```

---

## Utilities

The `source/mlproject/utils.py` module provides helper functions:

- `save_pickle_object(filename, obj)` - Serialize Python objects to disk
- Other utility functions for common operations

---

## Data Versioning

The project uses DVC (Data Version Control) for tracking data:

```bash
# Initialize DVC
dvc init

# Track CSV files
dvc add artifact/raw.csv
dvc add artifact/train.csv
dvc add artifact/test.csv

# Push to remote storage
dvc push
```

---

## Development Setup

### Install in Development Mode

```bash
pip install -e .
# or with uv
uv add -e .
```

### Running Tests

```bash
# Tests will be added in future versions
pytest tests/
```

---

## Dependencies

Key dependencies (see `requirements.txt`):

- **pandas** - Data manipulation and analysis
- **numpy** - Numerical computations
- **scikit-learn** - ML algorithms
- **sqlalchemy** - ORM and database connection
- **psycopg2** - PostgreSQL adapter
- **python-dotenv** - Environment variable management
- **DVC** - Data version control
- **Flask/FastAPI** - (Optional) For API deployment

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## Troubleshooting

### Import Errors
- Ensure `.env` is in project root
- Run with `python -m` from project root
- Activate virtual environment

### Database Connection Issues
- Verify PostgreSQL is running
- Check `.env` credentials
- Ensure database exists
- Test connection: `psql -U postgres -d mlproject`

### Module Not Found Errors
```bash
# Reinstall in development mode
pip install -e .
```

---

## License

This project is licensed under the MIT License - see LICENSE file for details.

---

## Contact & Support

**Author**: Hara Prasad

For issues, questions, or suggestions, please open an issue in the repository.