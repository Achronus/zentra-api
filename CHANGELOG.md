# Changelog

All notable changes to this project will be documented in this file.

## [0.1.14] - 2024-09-27

### 🚀 Features

- *(config)* Added config file for managing project structure.
- *(routeset)* Added route set group creation logic.
- *(routeset)* Expanded created route methods to have content.
- *(routeset)* Added `responses` content creation.
- *(routeset)* Added `schema` content creation.

### 🚜 Refactor

- *(route)* Simplified and expanded `Route` creation.
- *(routeset)* Simplified route creation.
- *(cors)* Refactored `parse_cors` method to return `strings`.

### 📚 Documentation

- *(responses)* Improved docstrings for responses module.
- *(crud)* Improved docstrings for CRUD classes.
- *(core)* Improved docstrings for `core` module.
- *(auth)* Improved docstrings for `auth` module.

### 🎨 Styling

- *(auth)* Updated dependencies to constants for usability.

### 🧪 Testing

- *(validation)* Added tests for missing validation methods.
- *(routes)* Add tests for `add-routeset` command.
- *(template)* Fixed broken template authentication tests.
- *(routeset)* Added tests for `add-routeset` command.
- *(route)* Added tests for expected `__init__` route output.
- *(routeset)* Fix broken tests and add some for coverage.

### Build

- *(poetry)* Updated packages to latest.

## [0.1.13] - 2024-09-09

### 🚀 Features

- *(add-route)* Added set name handling using `inflect`.
- *(auth)* Added refresh tokens to auth routes.

### 🚜 Refactor

- *(tests)* Refactored test names for `TestSetup` to simplify.
- *(add)* Replaced `add` command with `add-route`.

### 🧪 Testing

- *(auth)* Updated failing tests based on new `auth` changes.

## [0.1.12] - 2024-08-29

### 🐛 Bug Fixes

- *(alembic)* Added  missing`ini` template file.

## [0.1.11] - 2024-08-23

### 🚀 Features

- *(init)* Added `--hide-output` flag for omitting console output.

### 🧪 Testing

- *(templates)* Updated template tests to pass.
- *(output)* Added tests for logging and output messages.
- *(init)* Added error test cases for coverage.

## [0.1.10] - 2024-08-22

### 🚀 Features

- *(alembic)* Added `alembic` integration.

### 🐛 Bug Fixes

- *(template)* Fixed invalid imports and config bugs.

### 🚜 Refactor

- *(poetry)* Simplified Poetry script creation.
- *(scripts)* Moved Poetry scripts to separate directory.

### ⚙️ Miscellaneous Tasks

- *(workflows)* Moved codecov into separate workflow

## [0.1.9] - 2024-08-22

### 🚀 Features

- *(template)* Added deployment template files with build command

### 🐛 Bug Fixes

- *(build)* Fixed build issues with Django projects

### 🚜 Refactor

- *(template)* Moved template files to separate directory
- *(setup)* Simplified template directory retrieval
- *(msgs)* Updated output messages for `init` command for clarity
- *(config)* Expanded configuration settings for usability
- *(template)* Updated template config file structure to simplify
- *(config)* Updated algorithm type to specific options
- *(cli)* Updated `new-key` command logic to simplify
- *(env)* Expanded environment variable template
- *(setup)* Enhanced dynamic env file updates
- *(setup)* Updated `init` command logic to include Django projects
- *(setup)* Removed Django templates and settings - discontinued

### 🧪 Testing

- *(msgs)* Fixed broken message tests
- *(config)* Added and updated tests for config
- *(cli)* Refactored `key_length` method to fixture

### Build

- *(poetry)* Updated FastAPI to latest package version

## [0.1.8] - 2024-08-03

### 🚜 Refactor

- *(auth)* Added `Field` declarations to model attributes for docs

### Build

- *(poetry)* Removed `Poetry` as required dependency in package

## [0.1.7] - 2024-08-01

### 🐛 Bug Fixes

- *(auth)* Fix broken `config` import in templates

### 🚜 Refactor

- *(template)* Removed redundant code

### 🧪 Testing

- *(poetry)* Refactor poetry file builder tests to pass
- *(coverage)* Added coverage settings with omits for API tested files
- *(template)* Added `init` project tests (99% coverage) for quickstart

## [0.1.6] - 2024-08-01

### 🐛 Bug Fixes

- *(auth)* Update `token` route output to fix bug
- *(poetry)* Fixed Poetry `dev` dependencies group assignment

### 🚜 Refactor

- *(db)* Moved `db` models to separate folder for scalability
- *(auth)* Refactor route output responses for best practice

### 🧪 Testing

- *(auth)* Refactor time-based tests to pass

## [0.1.5] - 2024-07-31

### 🚀 Features

- *(settings)* Add `TOKEN_URL` parameter to `AuthConfig`

### 🐛 Bug Fixes

- *(auth)* Token authentication bug in `auth` router

### 🚜 Refactor

- *(auth)* Update token method name for clarity
- *(db)* Add `DB` prefix to DB model class names for clarity
- *(auth)* Add response models to methods

## [0.1.4] - 2024-07-31

### 🧪 Testing

- *(setup)* Fix broken tests
- *(setup)* Fix secret key length error

## [0.1.3] - 2024-07-31

### 🚀 Features

- *(command)* Add `new-key` for secret key generation with tests
- *(setup)* Add automatic secret key creation during `init`

### 🐛 Bug Fixes

- *(bcrypt)* Remove passlib and add custom bcrypt alternative
- *(command)* Convert port to string in `run-dev`

### 🚜 Refactor

- *(auth)* Apply `BcryptContext` to `Settings`

### Build

- *(poetry)* Update toml file

<!-- generated by git-cliff -->
