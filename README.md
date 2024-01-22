# Y_lab_1
FastAPI CRUD application with PostgreSQL

## Installation

### Prerequisites

#### Python

Before installing the package make sure you have Python version 3.10 or higher installed:

```bash
>> python --version
Python 3.10+
```

#### Docker

The project uses Docker to run the database. To install Docker use its [official instruction](https://docs.docker.com/get-docker/).

### Application

To use the application, you need to clone the repository to your computer. This is done using the `git clone` command. Clone the project:

```bash
git clone git@github.com:sergdemc/y_lab_1.git && cd y_lab_1
```

Then you have to install all necessary dependencies in your virtual environment:

```bash
make install
```

## Usage

Start the PostgreSQL database in the Docker container by running: 
```bash
make start_db
```

Start the application by running:
```bash
make server
```
_By default, the server will be available at http://127.0.0.1:8000._

Stop the database server:
```bash
make stop_db
```
