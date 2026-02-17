# ANALYTICS PRODUCT: ENVIRONMENTAL IMPACT OF NEW VEHICLES

![Python](https://img.shields.io/badge/python-3.14+-3776AB?logo=python\&logoColor=white)

---

## Context

### Climate Challenge

Road transport emits CO₂, the main greenhouse gas responsible for climate change.
To help consumers make more responsible purchasing decisions, the European Union requires:

* Clear display of fuel consumption
* Clear display of CO₂ emissions
* Comparison of vehicles based on emission levels

The objective is to steer demand toward lower-emission vehicles by making climate impact visible at the point of purchase.

---

### Air Quality Challenge: Reducing Pollutants

In major cities, road traffic is a significant source of pollution (NOx, fine particulate matter, etc.).
The European Union sets reduction targets for several pollutants to protect public health.

Beyond climate concerns, this is also a public health issue: reducing diseases linked to urban air pollution.

---

### Noise Pollution: Improving Quality of Life

Road noise is a major urban nuisance.
New European standards progressively lower vehicle noise limits (down to 68 dB from 2026 for standard passenger cars).

Noise level labeling is becoming mandatory.

The ecological transition is not limited to CO₂ emissions; it also concerns comfort and daily well-being.

---

## Target Audience

This tool is designed for private consumers seeking clear, structured information to compare new vehicles and make environmentally responsible purchasing decisions.

---

## Dataset

The dataset is provided by **ADEME (French Agency for Ecological Transition)**, a public organization actively engaged in combating climate change.

[https://data.ademe.fr/datasets/ademe-car-labelling](https://data.ademe.fr/datasets/ademe-car-labelling)

The dataset contains over 60 variables describing new passenger vehicles under the WLTP standard.

Key variables include:

* Identification: Brand, Model, Group, Energy type, Body type, Segment
* Technical specifications: Engine displacement, Maximum power, Fiscal power, Curb weight, Transmission type
* Environmental performance: WLTP cycle consumption, CO₂ emissions (combined cycle), regulated pollutants such as NOx and particulate matter
* Electric vehicle data: Electric consumption, Electric range
* Economic indicators: Bonus-malus scheme, Fiscal scale, Vehicle price

This dataset enables joint analysis of vehicle performance, environmental impact, and economic positioning.

---

## Code Structure

The project follows the **src layout**, which isolates source code from external tools and configuration files.

This structure enhances modularity and security while supporting a collaborative workflow.
It allows the creation of multiple sub-packages to clearly separate responsibilities and maintain scalability.

---

## Dependency Management

The project uses **Poetry and uv** as Python package managers to adopt an industry-grade approach to dependency management.

A centralized configuration is defined in `pyproject.toml`, with a corresponding lock file ensuring reproducibility and version consistency across environments.

---

## Unit Testing

Unit tests are implemented using **pytest**, alongside Python’s built-in `unittest` framework when necessary.

---

## Code Quality Control

Code formatting and linting are handled by **Ruff**.

Code validation is automated via **pre-commit hooks**, configured in the `pre-commit-config.yaml` file.

---

## Reproducible Development Environment

To ensure a fully reproducible development environment for all contributors, the project includes a `.devcontainer` configuration.

This setup includes:

* A `Dockerfile` defining the development environment
* A `docker-compose.yml` file to orchestrate and run multiple containers simultaneously

This guarantees consistency across development setups and simplifies onboarding.

















