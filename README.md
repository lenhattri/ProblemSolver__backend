# OVERVIEW
Đây là một dự án nghiên cứu khoa học cấp trường(do sinh viên làm) Đại Học An Giang do tôi chủ nhiệm và phát triển chính 

# TECHNOLOGIES
  - Django REST
  - Autogen
  - LLMs

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
  
  ```
  git clone https://github.com/lenhattri/ProblemSolver__backend
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
- Finally, run
  ```
  python manage.py runserver
  ```
  
