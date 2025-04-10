# Smart Gallery — CLIP Fine-Tuning

___
## About

___
## Usage

___
## Project Structure

<details>
  <summary>📂 clip_fine_tuning/</summary>
  <ul>
    <li>📄 <code>pyproject.toml</code> — Project metadata and build system configuration</li>
    <li>📄 <code>requirements.txt</code> — Python dependencies for fine-tuning and experiments</li>
    <details>
      <summary>📂 dataset/</summary>
      <ul>
        <details>
          <summary>📂 src/</summary>
          <ul>
            <li>📄 <code>database.py</code> — Interface for accessing and querying the SQLite dataset</li>
            <li>📄 <code>models.py</code> — Pydantic/ORM models used for dataset structure</li>
            <li>📄 <code>repository.py</code> — Logic for loading and managing image-text pairs</li>
            <li>📄 <code>ruclip_dataset.py</code> — Dataset wrapper for training with ruCLIP</li>
          </ul>
        </details>
        <li>📄 <code>1. qwen25_test.ipynb</code> — Notebook for verifying Qwen-2.5 API keys</li>
        <li>📄 <code>2. clip993.ipynb</code> — Captioning images with Qwen-2.5 for ruCLIP dataset</li>
        <li>📄 <code>clip.db</code> — SQLite database with image-text pairs</li>
        <li>📄 <code>qwen_api_keys.json</code> — API keys for Qwen model access</li>
      </ul>
    </details>
    <details>
      <summary>📂 models/</summary>
      <ul>
        <details>
          <summary>📂 fine-tuning/</summary>
          <ul>
            <li>📄 <code>1. ruclip_clip993.ipynb</code> — Notebook for training ruCLIP on custom dataset</li>
          </ul>
        </details>
        <li>📄 <code>1. open_clip.ipynb</code> — Experiment with OpenCLIP model</li>
        <li>📄 <code>2. ruclip.ipynb</code> — Loading and using ruCLIP</li>
        <li>📄 <code>3. ruclip_tiny.ipynb</code> — Experiment with ruCLIP tiny version</li>
        <li>📄 <code>4. ruclip_clip993.ipynb</code> — Loading and using ruClip finetuned clip993</li>
        <li>📄 <code>base_clip.py</code> — Abstract class for CLIP-like models</li>
      </ul>
    </details>
  </ul>
</details>

___
## Technologies Used
