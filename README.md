# TJM Project — BotCity Desktop Automation

Automates the process of fetching posts from an API and saving them as `.txt` files using Windows Notepad.

---

## 📁 Project Structure

```
tjm-project/
│
├── main.py                  # Entry point
├── config.py                # All constants and settings
├── pyproject.toml           # Project metadata and dependencies (uv)
├── uv.lock                  # Exact dependency versions (uv)
├── requirements.txt         # Fallback for non-uv environments
├── .gitignore
│
├── bot/
│   ├── __init__.py
│   ├── actions.py           # open_notepad, terminate_notepad, show_desktop
│   ├── grounding.py         # ground_notepad_icon, validate_notepad_window, ensure_notepad_is_open
│   └── writer.py            # write_post_to_notepad
│
├── services/
│   ├── __init__.py
│   └── api_client.py        # fetch_posts
│
├── utils/
│   ├── __init__.py
│   ├── logger.py            # setup_logger
│   └── file_manager.py      # create_project_folder, get_project_path
│
└── resources/
    └── notepad_icon.png     # Place your Notepad icon screenshot here
```

---

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/mahmoudalsharkawy572/tjm-project.git
```

### 2. Add your Notepad icon image

- Take a screenshot of the Notepad icon on **your machine's desktop**
- Crop tightly around the icon with minimal padding
- Save it as `notepad_icon.png` inside the `resources/` folder

> ⚠️ The icon image must be taken from your own machine since icons may look different across Windows versions and screen resolutions.

---

## 🚀 Running the Project

### ✅ Recommended — Using uv (modern, fast)

`uv` is the recommended way to run this project. It handles the virtual environment and dependencies automatically.

**Install uv (Windows):**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Install dependencies and run:**

```bash
uv sync
uv run main.py
```

That's it — `uv` creates the virtual environment and installs everything automatically.

---

### 🔁 Alternative — Using pip + venv (if uv is not supported)

If your environment does not support `uv`, you can fall back to the classic approach using `requirements.txt`:

```bash
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate        # Windows

# Install dependencies
pip install -r requirements.txt

# Run the project
python main.py
```

---

## 📝 Output

- Text files `post_1.txt`, `post_....txt`, `post_n.txt` are saved to `Desktop/tjm-project/`
- A log file `automation.log` is also created in the same folder

---

## 🔧 Configuration

All settings are in `config.py`:

| Variable                 | Description                             | Default             |
| ------------------------ | --------------------------------------- | ------------------- |
| `API_URL`                | The posts API endpoint                  | dummyjson.com/posts |
| `POSTS_LIMIT`            | How many posts to process               | 3                   |
| `MAX_GROUNDING_ATTEMPTS` | Retries to find the Notepad icon        | 3                   |
| `IMAGE_MATCH_THRESHOLD`  | Confidence for image matching (0.0–1.0) | 0.85                |
| `NOTEPAD_WINDOW_TIMEOUT` | Seconds to wait for Notepad to open     | 5                   |

---

## 📌 Notes

- This automation is designed for **Windows only**
- Make sure Notepad is visible as an icon on your Desktop before running
- If the icon is not found, the bot will automatically fall back to launching Notepad via the OS