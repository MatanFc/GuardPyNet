# GuardPyNet

GuardPyNet is a Python web service designed to identify packages or their dependencies with suspicious contributors of unknown origin. It leverages data from PyPI and GitHub to provide comprehensive lists of contributors.

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Database Configuration](#database-configuration)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Features

- Fetch contributors for a specified package and its dependencies.
- Asynchronous fetching for efficient data retrieval.
- Support for caching to minimize latency on repetitive requests.

## Getting Started

### Prerequisites

Make sure you have the following installed:

- Python 3.x
- [pip](https://pip.pypa.io/en/stable/)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/matanfc/GuardPyNet.git
   cd GuardPyNet
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the FastAPI app:

   ```bash
   uvicorn main:app --reload
   ```

2. Open your browser and visit http://127.0.0.1:8000/docs to explore the Swagger UI and test the API endpoints.

## API Endpoints

- GET /contributors/{package_name}: Fetch contributors for a specified package and its dependencies.

Example:

```bash
http://127.0.0.1:8000/contributors/your_package_name
```

## Database Configuration

The application uses a PostgreSQL database. Configure your database connection in app/db/config.py.

## Contributing

1. Fork the project.
2. Create a new branch (git checkout -b feature/new-feature).
3. Commit your changes (git commit -am 'Add new feature').
4. Push to the branch (git push origin feature/new-feature).
5. Create a new Pull Request.
