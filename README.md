# Smart-Gallery

___
## About

___
## Installation
```shell
docker compose --env-file .env.dev up --build
```

___
## Architecture
![Smart Gallery - Frame 1 (1)](https://github.com/user-attachments/assets/4e70a845-1029-46fb-8342-096d2249f331)
![Smart Gallery - Frame 2 (2)](https://github.com/user-attachments/assets/0602964c-3c33-4bbd-be99-9d1360518ddd)

___
## Usage

___
## Project Structure

<details>
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
            <summary>📂 fine-tuned/</summary>
            <ul>
              <li>📄 __init__.py</li>
              <li>📄 ruclip_clip993.pt</li>
            </ul>
          </details>
          <details>
            <summary>📂 fine-tuning/</summary>
            <ul>
              <li>📄 1. ruclip_clip993.ipynb</li>
              <li>📄 test.ipynb</li>
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

___
## Contacts
- **Mail**: `gabezrukov@edu.hse.ru`
- **Telegram**: [@bezGriga](https://t.me/bezGriga)  
