
![Logo](assets/logo.jpg)

[![codecov](https://codecov.io/github/Achronus/zentra-api/graph/badge.svg?token=Y2G1RM4WFO)](https://codecov.io/github/Achronus/zentra-api)
![Python Version](https://img.shields.io/pypi/pyversions/zentra-api)
![License](https://img.shields.io/github/license/Achronus/zentra-api)
![Issues](https://img.shields.io/github/issues/Achronus/zentra-api)
![Last Commit](https://img.shields.io/github/last-commit/Achronus/zentra-api)


🚧 _In development_ 🚧

Zentra API, your CLI tool for building [FastAPI](https://fastapi.tiangolo.com/) projects faster.

# Zentra API

Streamline your workflow, automate repetitive tasks, and generate high-quality code in minutes. Whether you're a seasoned developer or just starting out, Zentra API empowers you to build robust, scalable, and production-ready [FastAPI](https://fastapi.tiangolo.com/) applications with unparalleled speed and efficiency. 

Say goodbye to the hassles of manual setup and configuration, and say hello to a smoother, more productive coding experience.

Zentra API isn't just about speed - it's about enhancing your entire development process. Its intuitive CLI simplifies project creation, allowing you to focus on what truly matters: crafting exceptional APIs. 

With built-in templates, automated code generation, and seamless integration with popular tools and frameworks, Zentra API ensures your projects are not only fast to build but also maintain the highest standards of quality and performance. Elevate your FastAPI development game today!

# What's Great About It?

Our goal with Zentra API is to provide a suite of useful commands that improve the efficiency of building FastAPI apps. API development doesn't need to be a long winded process!

Here's some of the commands you can expect to see:

- [X] `init` - a quick way to initialize projects with a predefined template so you can dive straight into route building. You'll need to run this first!
- [ ] `add-table` - adds a SQL Base class template to the project, automatically configuring it for use in routes
- [ ] `add-route` - adds a new route to the project with a starter template, automatically linking it to the FastAPI app
- [ ] `build` - creates a production ready version of your app with docker files
- [X] `new_key` - a quick way to generate a new authentication secret key

But, that's not all! We've also added a few extra features to make development a breeze:

- [ ] `Unit test templates` - when running one of the `add` commands, you'll automatically get some relevant [pytest](https://docs.pytest.org/en/stable/) unit tests added to the project
- [X] `Route outputs` - we've added a standardized template for API responses that follow best practices making your APIs a joy to work with
- [X] `Response models` - we provide utilities for quickly building response models from status codes that can be added to your routes in seconds

And so much more...

# Getting Started

To get started, install the `API` package with [Poetry](https://python-poetry.org/):

```bash
pip install zentra_api poetry
```

We use Poetry for managing our project packages and using custom commands, such as `run-dev` for the development environment.

Then create a new project with:

```bash
zentra-api init <project_name>
```

With one command you'll have a working app in minutes with:

- Built-in user authentication with JWT token protection
- Preconfigured CORs middleware
- A [SQLite](https://www.sqlite.org/) database configured with [Alembic](https://alembic.sqlalchemy.org/en/latest/)
- Built-in templated route responses following best practices
- A simple folder structure to make project navigation a breeze
- And, access to our package filled with other goodies

Read more about it in our [documentation](#) (🔜 _Coming soon!_ 🔜).

## Zentra SDK

Zentra API is part of the `Zentra SDK` project. You can read more about it on [GitHub](https://github.com/Achronus/zentra).
