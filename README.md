<p align="center">
  <a href="https://www.maaz.global/client/">
    <img src="images/intro.png" height="300px">
  </a>
</p>

<h1 align="center"> MaaZ Copilot </h1> <br>


Maaz Copilot is a project designed to enhance user productivity in coding through advanced features such as:

- **Code Autocompletion:** Automatically completes code based on context.
- **Code Generation:** Generates code from user requirements.
- **Chat Interaction:** Interacts with users to answer technical questions.
- **Code Analysis:** Analyzes code and provides detailed feedback.
- **Xtend File Generation:** Supports generating Xtend files from rule file, which is one of the most important roles of Maaz Copilot.

And more feature will be coming soon .

---
## Project structure


```
root 
├── data_storage // To store all file upload from client/server side to server/client
├── images // To show image in README.md
├── llm_api // To place interface api for each framwork, example FastAPI
├── llm_core // To place the core LLM 
    ├── copilot // The interface will call this to implement
    ├── llm_model // To place all models use in the core
    ├── llm_tech // To place tool use with LLM
    ├── llm_utils // To place utilities for support only LLM
    └── prompt_template // To place system prompt for LLM
├── logs // To place the log file for server
├── static // To place the icon/image to render home icon (not important)
├── templates // To place the html to render home page (not important)
└── utils // To place common utilities for project
```



## Getting Started

### Prerequisites

Install <a href="https://www.anaconda.com/download/"> Anaconda </a> or <a href="https://docs.anaconda.com/miniconda/"> Miniconda</a> to easy-to-use distribution/management of Python packages.

### Setup environment

To install the necessary dependencies for the project, you need to use `conda` to install from the `requirements.txt` file.

##### Step 1: Create a conda environment

```bash
conda create --name maaz_copilot
```

##### Step 2: Activate the environment
```bash
conda activate maaz_copilot
```

##### Step 3: Install dependencies
```bash
pip install -r requirements.txt
```

##### Step 4: Add API key to .env file
Create your .env file in the root directory and push your key in that file.

```python
GROQ_API_KEY = "Enter your API key here"
```

To get your API key, please visit <a href="https://console.groq.com/keys"> here </a>.

---

## Running The Application

To start the API routes, use uvicorn:
```bash
uvicorn app:app
```

or 

```bash
python3 app.py
```

This will start the server, and the API routes will be accessible at the default url http://127.0.0.1:8000

---

## Testing API

Go to the URL http://127.0.0.1:8000/docs to test all available APIs

---

## License

This belong to FPT Software - FA.AES department. Please contact if you need more information.

<p align="center">
  <a href="https://fptsoftware.com/">
    <img src="images/logo.png">
  </a>
</p>

---

## To do
- [x] Feature 1
- [ ] Feature 2
- [ ] Feature 3
