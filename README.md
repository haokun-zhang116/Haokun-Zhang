# Haokun-Zhang
Financial 10-K Chatbot_Team_5
# 1. Prepare your tools

Feel free to skip these steps if you have already installed the tools.

## 1.1 Install Visual Studio Code (VSCode)

1. Go to the [VSCode download page](https://code.visualstudio.com/download)
2. Download the appropriate version for your operating system (Windows, macOS, or Linux)
3. Follow the installation instructions for your platform
4. Launch VSCode after installation

## 1.2 Download and Open This Repository

1. Download this repository by clicking the green "Code" button on the GitHub page and selecting "Download ZIP"
2. Extract the ZIP file to a location on your computer
3. In VSCode, go to File > Open Folder and select the extracted folder

## 1.3 Opening the Terminal in VSCode

1. In VSCode, press `` Ctrl+` `` (Windows/Linux) or `` Cmd+` `` (macOS) to open the integrated terminal
2. Alternatively, go to View > Terminal from the menu bar

## 1.4 Install Miniconda

1. Go to the [Miniconda download page](https://www.anaconda.com/docs/getting-started/miniconda/install)
2. Download the appropriate installer for your operating system
3. Run the installer and follow the installation instructions
4. Verify the installation by opening a new terminal and typing `conda --version`



# 2. Install Environment 


You will create a new conda environment and install the packages.
The environment will be named `chatbot`.

```bash
# Create a new conda environment
conda create -n chatbot python=3.11

# Activate the environment
conda activate chatbot

# Install packages available in conda-forge
conda install -c conda-forge streamlit faiss-cpu pdf2image pytesseract pillow

# Install the remaining packages using pip
pip install langchain
pip install langchain-community
pip install langchain-core
pip install langchain-ollama
pip install pypdf
```

In the vscode terminal, use following command to confirm the environment is working:

```bash
conda activate chatbot
which python # should return /Users/your_username/miniconda3/envs/chatbot/bin/python
```


# 3. Download and Install Ollama

Ollama allows you to run large language models locally on your computer. To install Ollama:

1. Visit the official Ollama website at [https://ollama.com/download](https://ollama.com/download)
2. Download the appropriate installer for your operating system (Windows, macOS, or Linux)
3. Run the installer and follow the on-screen instructions
4. After installation, Ollama will run as a service in the background
5. Verify the installation by opening a terminal (you can open it in VSCode) and running `ollama --version`

Use the following command in the vscode terminal to make sure it's working:

```bash
ollama --version # should return a version number like 0.5.12
```


# 4. Pull the LLM & Embedding Model:

First, Pull the LLM Model

```bash
ollama pull llama3.1
```

You can start to chat with the model by running the following command:

```bash
ollama run llama3.1 # should return a prompt to enter a message # entry /bye to exit
```

Besides the LLM, we also need to install the embedding model. Here we use the `mxbai-embed-large` model.

```bash
ollama pull mxbai-embed-large
```
# 5. Run the Chatbot App 

Now you have the ollama model and the embedding model. 


You can run the chatbot.

```bash
streamlit run chat_with_team5bot.py
```
