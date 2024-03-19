# OVERVIEW
This is an multi-agents project

# TECHNOLOGIES
  - Django REST
  - Autogen
  - LLMs
# IDEA
  - Áp dụng mô hình ngôn ngữ lớn LLMs(Large Language Models) vào hệ thống đa tác tử MAS(Multi-Agents System) để giải quyết các vấn đề phức tạp. Áp dụng thực tiễn vào một website giúp phân tích và giải quyết vấn đề giải thuật bằng AI
# INSTALLATION

- Create venv:

  ```
  python -m venv venv
   ```
- Activate venv

  - On Windows:
  
     ```
    venv\Scripts\activate
     ```
    Or

    ```
    cd venv\Scripts
    .\activate
    ```
    
  - On Unix or MacOS:
  
      ```
    source venv/bin/activate
      ```

- Create src folder

  ```
  cd venv
  mkdir src
  cd src
  ```
- Clone git repository
  
  Fork this repository and run this command:
  
  ```
  git clone https://github.com/{your-user-name}/ProblemSolver__backend
  ```

- Install requirements

  ```
  python -m pip install -r requirements.txt
  ```

- Migrations

  ```
  python manage.py makemigrations
  python manage.py migrate
  ```
- Create .env
  ```
  cd ProblemSolver__Backend
  cp .example.env .env
  ```
  And replace content with your api key
  
  
- Finally, run
  ```
  python manage.py runserver
  ```

# CONVENTIONS

(updating)
  
