# Real Time Flood Monitoring Tool

## Description

This tool is a web application that utilizes the Real Time flood-monitoring API provided by the Environmental Agency (UK) to display flood readings from individual measurement stations.  It allows users to select a station and view a line graph and tabular data of the station's readings over the last 24 hours.

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

*   **Docker Desktop** (if running with Docker):  [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)
*   **Python 3.12** (if running locally without Docker): [https://www.python.org/downloads/](https://www.python.org/downloads/)

### Installation and Setup

There are two main ways to run this tool: using Docker or running it directly with Python.

**1. Using Docker (Recommended)**

   a. **Clone the repository (if you haven't already):**

      ```bash
      git clone https://github.com/y-h-chan/UK_flood_monitor_tool.git
      cd UK_flood_monitor_tool  # Navigate to the project directory
      ```

   b. **Build the Docker image:**

      ```bash
      docker build -t flood-tool-app .
      ```

   c. **Run the Docker container:**

      ```bash
      docker run -d -p 8000:8000 flood-tool-app
      ```

      This will start the application in detached mode on port 8000.

**2. Running Locally with Python**

   a. **Clone the repository (if you haven't already):**

      ```bash
      git clone https://github.com/y-h-chan/UK_flood_monitor_tool.git 
      cd UK_flood_monitor_tool  # Navigate to the project directory
      ```

   b. **Create a virtual environment (recommended):**

      ```bash
      python3 -m venv venv
      source venv/bin/activate  # On macOS/Linux
      # venv\Scripts\activate  # On Windows
      ```

   c. **Install Python dependencies:**

      ```bash
      pip install -r requirements.txt
      ```

   d. **Run the FastAPI application:**

      ```bash
      uvicorn flood_monitor:app --reload --host 0.0.0.0 --port 8000
      ```


### Accessing the Tool

Once the application is running (either via Docker or locally), you can access it in your web browser by navigating to:

http://localhost:8000

## Usage

1.  **Station Selection:** Upon opening the webpage, you will see a dropdown menu labeled "Select Station".
2.  **Choose a Station:** Click on the dropdown and select a flood measurement station from the list. The list is populated from the Environmental Agency API.
3.  **View Readings:** After selecting a station, click the "Show Readings" button.
4.  **Data Display:** The page will update to display:
    *   **Line Graph:** A line graph visualizing the station's readings over the last 24 hours. The graph shows time in UTC on the x-axis and the reading value on the y-axis.
    *   **Data Table:**  A table below the graph displaying the raw readings data, including `dateTime`, `value`, and `unit`.

## Docker Information

This tool is Dockerized for easy deployment and to ensure consistent execution environments. The `Dockerfile` is included in the project root directory.

*   **Building the Docker Image:**  Use `docker build -t flood-tool-app .` in the project root.
*   **Running the Docker Container:** Use `docker run -d -p 8000:8000 flood-tool-app`.
*   **Stopping the Container:**  Use `docker stop <container_id>` (find the container ID using `docker ps`).

Docker ensures that all dependencies are correctly installed and that the application runs in a consistent environment, regardless of the host operating system.

## Requirements

The Python dependencies for this project are listed in the `requirements.txt` file.  You can install them using `pip install -r requirements.txt`.

The key dependencies are:

*   `fastapi`
*   `uvicorn`
*   `requests` or `httpx`
*   `pandas`
*   `matplotlib`
*   `Jinja2`
*   `markupsafe`
*   `python-dateutil`
*   `python-multipart`

## License

Copyright [2025] [Yin Hei Chan]

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

## Contact

https://github.com/y-h-chan