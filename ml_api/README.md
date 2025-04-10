# Smart Gallery — ML Api

___
## About

___
## Usage

___
## Project Structure

<details>
  <summary>📂 ml_api/</summary>
  <ul>
    <li>📄 <code>.dockerignore</code> — Files and folders excluded from Docker build context</li>
    <li>📄 <code>Dockerfile</code> — Instructions for building the ML service Docker image</li>
    <li>📄 <code>requirements.txt</code> — Python dependencies for the ML microservice</li>
    <details>
      <summary>📂 app/</summary>
      <ul>
        <li>📄 <code>main.py</code> — Entry point of the FastAPI ML service</li>
        <li>📄 <code>config.py</code> — Configuration for model and app settings</li>
        <li>📄 <code>router.py</code> — API routes for text-to-image search and embeddings</li>
        <li>📄 <code>schemas.py</code> — Pydantic models for request/response validation</li>
        <details>
          <summary>📂 sm_clip/</summary>
          <ul>
            <li>📄 <code>__init__.py</code> — Marks the sm_clip module</li>
            <li>📄 <code>base_clip.py</code> — Abstract base class for CLIP models</li>
            <li>📄 <code>clip_vit_b_32.py</code> — CLIP ViT-B/32 model wrapper implementation</li>
          </ul>
        </details>
      </ul>
    </details>
  </ul>
</details>

___
## Technologies Used
