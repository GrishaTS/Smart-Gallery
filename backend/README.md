# Smart Gallery — Backend

___
## About

___
## Usage

___
## Project Structure

<details>
  <summary>📂 backend/</summary>
  <ul>
    <li>📄 <code>.dockerignore</code> — Files and folders to exclude from Docker build context</li>
    <li>📄 <code>Dockerfile</code> — Instructions to build the backend Docker image</li>
    <li>📄 <code>requirements.txt</code> — Python dependencies for the backend</li>
    <details>
      <summary>📂 app/</summary>
      <ul>
        <li>📄 <code>main.py</code> — FastAPI application entry point</li>
        <li>📄 <code>config.py</code> — Application settings and configuration</li>
        <li>📄 <code>models.py</code> — SQLAlchemy models and database schemas</li>
        <li>📄 <code>router.py</code> — API router combining all endpoints</li>
        <li>📄 <code>schemas.py</code> — Pydantic models for request and response validation</li>
        <details>
          <summary>📂 api/</summary>
          <ul>
            <li>📄 <code>__init__.py</code> — Marks the API module</li>
            <li>📄 <code>ml_api.py</code> — Routes for interacting with the ML microservice</li>
          </ul>
        </details>
        <details>
          <summary>📂 database/</summary>
          <ul>
            <li>📄 <code>__init__.py</code> — Marks the database module</li>
            <li>📄 <code>minio_client.py</code> — Client setup for MinIO object storage</li>
            <li>📄 <code>postgres_client.py</code> — Client setup for PostgreSQL database</li>
            <li>📄 <code>qdrant_client.py</code> — Client setup for Qdrant vector database</li>
            <li>📄 <code>test_data.py</code> — Test data and helper functions for development</li>
          </ul>
        </details>
        <details>
          <summary>📂 repository/</summary>
          <ul>
            <li>📄 <code>__init__.py</code> — Marks the repository module</li>
            <li>📄 <code>base_repository.py</code> — Abstract base class for all repositories</li>
            <li>📄 <code>postgres_repository.py</code> — PostgreSQL-specific database operations</li>
            <li>📄 <code>minio_repository.py</code> — MinIO-specific storage operations</li>
            <li>📄 <code>qdrant_repository.py</code> — Qdrant-specific vector operations</li>
            <li>📄 <code>repository.py</code> — Aggregated interface for using all repositories</li>
          </ul>
        </details>
      </ul>
    </details>
  </ul>
</details>

___
## Technologies Used
