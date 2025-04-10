# Smart Gallery — Frontend

___
## About

___
## Usage

___
## Project Structure

<details>
  <summary>📂 frontend/</summary>
  <ul>
    <li>📄 <code>.dockerignore</code> — Files and folders excluded from Docker build context</li>
    <li>📄 <code>Dockerfile</code> — Instructions for building the frontend Docker image</li>
    <li>📄 <code>requirements.txt</code> — Python dependencies for the frontend</li>
    <details>
      <summary>📂 app/</summary>
      <ul>
        <li>📄 <code>main.py</code> — Entry point of the Flet-based UI application</li>
        <li>📄 <code>config.py</code> — Application configuration and constants</li>
        <li>📄 <code>routes.py</code> — Route management for page navigation</li>
        <details>
          <summary>📂 api/</summary>
          <ul>
            <li>📄 <code>__init__.py</code> — Marks the API module</li>
            <li>📄 <code>images_api.py</code> — API calls for bulk image operations</li>
            <li>📄 <code>image_api.py</code> — API calls for single image operations</li>
          </ul>
        </details>
        <details>
          <summary>📂 data/</summary>
          <ul>
            <li>📄 <code>__init__.py</code> — Marks the data module</li>
            <li>📄 <code>image_data.py</code> — Data structures and image-related logic</li>
          </ul>
        </details>
        <details>
          <summary>📂 views/</summary>
          <ul>
            <li>📄 <code>__init__.py</code> — Marks the views module</li>
            <li>📄 <code>base_view.py</code> — Base class for all views with shared logic</li>
            <li>📄 <code>home_view.py</code> — Home page layout with image grid</li>
            <li>📄 <code>images_view.py</code> — View for multiple images</li>
            <li>📄 <code>image_view.py</code> — View for a single image</li>
            <li>📄 <code>delete_images_view.py</code> — View for selecting and deleting images</li>
            <li>📄 <code>search_images_view.py</code> — View for searching images by text</li>
            <details>
              <summary>📂 mixins/</summary>
              <ul>
                <li>📄 <code>__init__.py</code> — Marks the mixins module</li>
                <li>📄 <code>app_bar_mixin.py</code> — Mixin for top app bar UI</li>
                <li>📄 <code>grid_mixin.py</code> — Mixin for image grid layout</li>
                <li>📄 <code>nav_bar_mixin.py</code> — Mixin for navigation bar UI</li>
              </ul>
            </details>
          </ul>
        </details>
      </ul>
    </details>
  </ul>
</details>


___
## Technologies Used
