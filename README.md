# Smart-Gallery

___
## About
*Smart Gallery is an offline-capable photo management system that integrates:*
- A responsive multi-page UI built with Flet for browsing, searching, and deleting images
- A robust FastAPI-based backend with support for PostgreSQL, MinIO, and Qdrant
- A dedicated ML microservice using CLIP/ruCLIP to enable text-based image search
- A flexible fine-tuning module for generating image captions and training custom CLIP models using Qwen-2.5
- The entire system is fully containerized with Docker, and designed to work without an internet connection — making it ideal for local or secure environments

___
## Installation
Clone the Smart-Gallery repository from GitHub:
```bash
git clone https://github.com/GrishaTS/Smart-Gallery
```
Navigate to the project directory:
```bash
cd Smart-Gallery
```
Install the required version of huggingface_hub to load the custom CLIP model:
```bash
pip install huggingface_hub==0.23.3 --force-reinstall --no-deps
```
Download the fine-tuned ruCLIP model:
```bash
huggingface-cli download bezGriga/ruclip-finetuned-clip993 ruclip_clip993.pt --cache-dir ml_api/app/sm_clip/hugface/ruclip_clip993
```

___
## Usage
Launch the application using Docker Compose:
```bash
docker compose --env-file .env.dev up --build
```
- **Frontend:** [http://localhost](http://localhost)  
- **Backend:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ML API:** [http://localhost:8001/docs](http://localhost:8001/docs)
- **MinIO:** [http://localhost:9001](http://localhost:9001) — login with `minio` / `secretpass`  
- **Qdrant:** [http://localhost:6334](http://localhost:6333/dashboard)  

___
## Architecture
![Smart Gallery - Frame 1 (1)](https://github.com/user-attachments/assets/4e70a845-1029-46fb-8342-096d2249f331)
![Smart Gallery - Frame 2 (2)](https://github.com/user-attachments/assets/0602964c-3c33-4bbd-be99-9d1360518ddd)


___
## Project Structure

<details open>
  <summary>📂 Smart-Gallery</summary>

  <ul>
    <li>📄 <code>.env.dev</code> — Development environment variables</li>
    <li>📄 <code>docker-compose.yml</code> — Docker services configuration</li>
    <li>📄 <code>nginx.conf</code> — NGINX reverse proxy configuration</li>
  </ul>

  <details>
    <summary>📂 <a href="https://github.com/GrishaTS/Smart-Gallery/tree/main/backend" target="_blank">backend/</a> — Backend</summary>
    <ul>
      <li>📄 .dockerignore</li>
      <li>📄 Dockerfile</li>
      <li>📄 requirements.txt</li>
      <details>
        <summary>📂 app/</summary>
        <ul>
          <li>📄 main.py</li>
          <li>📄 config.py</li>
          <li>📄 models.py</li>
          <li>📄 router.py</li>
          <li>📄 schemas.py</li>
          <details>
            <summary>📂 api/</summary>
            <ul>
              <li>📄 __init__.py</li>
              <li>📄 ml_api.py</li>
            </ul>
          </details>
          <details>
            <summary>📂 database/</summary>
            <ul>
              <li>📄 __init__.py</li>
              <li>📄 minio_client.py</li>
              <li>📄 postgres_client.py</li>
              <li>📄 qdrant_client.py</li>
              <li>📄 test_data.py</li>
            </ul>
          </details>
          <details>
            <summary>📂 repository/</summary>
            <ul>
              <li>📄 __init__.py</li>
              <li>📄 base_repository.py</li>
              <li>📄 postgres_repository.py</li>
              <li>📄 minio_repository.py</li>
              <li>📄 qdrant_repository.py</li>
              <li>📄 repository.py</li>
            </ul>
          </details>
        </ul>
      </details>
    </ul>
  </details>

  <details>
    <summary>📂 <a href="https://github.com/GrishaTS/Smart-Gallery/tree/main/frontend" target="_blank">frontend/</a> — User Interface</summary>
    <ul>
      <li>📄 .dockerignore</li>
      <li>📄 Dockerfile</li>
      <li>📄 requirements.txt</li>
      <details>
        <summary>📂 app/</summary>
        <ul>
          <li>📄 main.py</li>
          <li>📄 config.py</li>
          <li>📄 routes.py</li>
          <details>
            <summary>📂 api/</summary>
            <ul>
              <li>📄 __init__.py</li>
              <li>📄 images_api.py</li>
              <li>📄 image_api.py</li>
            </ul>
          </details>
          <details>
            <summary>📂 data/</summary>
            <ul>
              <li>📄 __init__.py</li>
              <li>📄 image_data.py</li>
            </ul>
          </details>
          <details>
            <summary>📂 views/</summary>
            <ul>
              <li>📄 __init__.py</li>
              <li>📄 base_view.py</li>
              <li>📄 home_view.py</li>
              <li>📄 images_view.py</li>
              <li>📄 image_view.py</li>
              <li>📄 delete_images_view.py</li>
              <li>📄 search_images_view.py</li>
              <details>
                <summary>📂 mixins/</summary>
                <ul>
                  <li>📄 __init__.py</li>
                  <li>📄 app_bar_mixin.py</li>
                  <li>📄 grid_mixin.py</li>
                  <li>📄 nav_bar_mixin.py</li>
                </ul>
              </details>
            </ul>
          </details>
        </ul>
      </details>
    </ul>
  </details>

  <details>
    <summary>📂 <a href="https://github.com/GrishaTS/Smart-Gallery/tree/main/ml_api" target="_blank">ml_api/</a> — ML Service</summary>
    <ul>
      <li>📄 .dockerignore</li>
      <li>📄 Dockerfile</li>
      <li>📄 requirements.txt</li>
      <details>
        <summary>📂 app/</summary>
        <ul>
          <li>📄 main.py</li>
          <li>📄 config.py</li>
          <li>📄 router.py</li>
          <li>📄 schemas.py</li>
          <details>
            <summary>📂 sm_clip/</summary>
            <ul>
              <li>📄 __init__.py</li>
              <li>📄 base_clip.py</li>
              <li>📄 clip_vit_b_32.py</li>
            </ul>
          </details>
        </ul>
      </details>
    </ul>
  </details>

  <details>
    <summary>📂 <a href="https://github.com/GrishaTS/Smart-Gallery/tree/main/clip_fine_tuning" target="_blank">clip_fine_tuning/</a> — Model Fine-tuning</summary>
    <ul>
      <li>📄 pyproject.toml</li>
      <li>📄 requirements.txt</li>
      <details>
        <summary>📂 dataset/</summary>
        <ul>
          <details>
            <summary>📂 src/</summary>
            <ul>
              <li>📄 database.py</li>
              <li>📄 models.py</li>
              <li>📄 repository.py</li>
              <li>📄 ruclip_dataset.py</li>
            </ul>
          </details>
          <li>📄 1. qwen25_test.ipynb</li>
          <li>📄 2. clip993.ipynb</li>
          <li>📄 clip.db</li>
          <li>📄 qwen_api_keys.json</li>
        </ul>
      </details>
      <details>
        <summary>📂 models/</summary>
        <ul>
          <details>
            <summary>📂 fine-tuning/</summary>
            <ul>
              <li>📄 1. ruclip_clip993.ipynb</li>
            </ul>
          </details>
          <li>📄 1. open_clip.ipynb</li>
          <li>📄 2. ruclip.ipynb</li>
          <li>📄 3. ruclip_tiny.ipynb</li>
          <li>📄 base_clip.py</li>
        </ul>
      </details>
    </ul>
  </details>

</details>

___
## Technologies Used
![FastAPI](https://img.shields.io/badge/FastAPI-API-009688?logo=fastapi) ![Uvicorn](https://img.shields.io/badge/Uvicorn-ASGI-333333?logo=uvicorn) ![Pydantic](https://img.shields.io/badge/Pydantic-Validation-4B8BBE?logo=pydantic) ![SQLAlchemy](https://img.shields.io/badge/ORM-SQLAlchemy-000000?logo=sqlalchemy) ![Asyncpg](https://img.shields.io/badge/PostgreSQL-Asyncpg-00599C) ![MinIO](https://img.shields.io/badge/ObjectStorage-MinIO-F05032?logo=minio) ![Qdrant](https://img.shields.io/badge/VectorDB-Qdrant-FF6F00) ![Pillow](https://img.shields.io/badge/Images-Pillow-316192?logo=python) ![NumPy](https://img.shields.io/badge/Numerics-NumPy-013243?logo=numpy) ![HTTPX](https://img.shields.io/badge/HTTP-Client-0E8AC8) ![Requests](https://img.shields.io/badge/Requests-SyncClient-20232A?logo=python) ![Python-Multipart](https://img.shields.io/badge/Uploads-Multipart-FFD43B) ![Aiofiles](https://img.shields.io/badge/Async-FileIO-6A5ACD) ![Flet](https://img.shields.io/badge/Flet-UI_Framework-007ACC) ![Websockets](https://img.shields.io/badge/Realtime-Websockets-FFA500) ![WSProto](https://img.shields.io/badge/Protocol-WSProto-6A5ACD) ![ruCLIP](https://img.shields.io/badge/Model-ruCLIP-orange) ![OpenCLIP](https://img.shields.io/badge/Model-OpenCLIP-FF8C00) ![Torch](https://img.shields.io/badge/Fine--tuning-PyTorch-EE4C2C?logo=pytorch) ![HuggingFace](https://img.shields.io/badge/Hub-HuggingFace-FF4C7B?logo=huggingface) ![Qwen](https://img.shields.io/badge/Captioning-Qwen--2%2E5-0064FF) ![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite) ![LiveLossPlot](https://img.shields.io/badge/Monitoring-LiveLossPlot-44CC11) ![YouTokenToMe](https://img.shields.io/badge/Tokenizer-YouTokenToMe-blue) ![Docker](https://img.shields.io/badge/Container-Docker-2496ED?logo=docker) ![NGINX](https://img.shields.io/badge/Proxy-NGINX-009639?logo=nginx)

___
## Contacts
- **Mail**: `gabezrukov@edu.hse.ru`
- **Telegram**: [@bezGriga](https://t.me/bezGriga)  
