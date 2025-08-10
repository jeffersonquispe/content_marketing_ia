# IAGen Project for Digital Marketing 🤖

This project is a functional solution that uses Generative Artificial Intelligence (GenAI) to automate and accelerate content creation and feedback analysis for a new product launch. The prototype is developed with Streamlit and connects to Amazon Bedrock to generate product descriptions, promotional images, and customer comment summaries.

---

### 📋 Prerequisites

Make sure you have the following installed on your **Windows** system:
* **Python 3.8+**
* **Visual Studio Code**
* **Git**

---

### 🛠️ Setup and Execution

Follow these steps to get the project up and running:

1.  **Clone the Repository**
    Open your Git Bash or CMD terminal and download the project:
    ```bash
    git clone [https://github.com/your-username/reto_alicorp_iagen.git](https://github.com/your-username/reto_alicorp_iagen.git)
    cd reto_alicorp_iagen
    ```

2.  **Configure Environment Variables**
    Create a new file named `.env` in the project's root folder and add your AWS credentials and ngrok token. Replace the example values with your own:
    ```ini
    AWS_ACCESS_KEY_ID=your_aws_access_key_id
    AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
    AWS_REGION=us-east-1
    NGROK_AUTH_TOKEN=your_ngrok_authtoken
    ```

3.  **Install Dependencies**
    It is recommended to create a virtual environment for the project.
    * Create and activate the virtual environment:
        ```bash
        python -m venv venv
        venv\Scripts\activate
        ```
    * Install the necessary libraries:
        ```bash
        pip install -r requirements.txt
        ```

4.  **Run the Application**
    To start the Streamlit application, make sure the virtual environment is active and run the following command:
    ```bash
    streamlit run src/app/app.py
    ```

---

### 📂 Project Structure

The solution is organized in a modular way for better scalability and maintenance.