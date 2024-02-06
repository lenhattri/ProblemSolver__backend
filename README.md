# OVERVIEW
Đây là một dự án nghiên cứu khoa học cấp trường(do sinh viên làm) Đại Học An Giang do tôi chủ nhiệm và phát triển chính 

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
- Change all api keys in ProblemSolver__Backend/.env to yours(Don't require APIFY_API_KEY)
  
- Finally, run
  ```
  python manage.py runserver
  ```

# CONVENTIONS
  - Phải xóa hết api key trong env trước khi commit(thay bằng "...")
  
