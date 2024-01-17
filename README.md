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