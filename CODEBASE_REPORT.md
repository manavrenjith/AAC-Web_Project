# AAC Web Project Codebase Report

## 1. Project Overview
This project is a web-based AAC (Augmentative and Alternative Communication) system designed to help Malayalam-speaking children communicate using symbols, text, and speech. Users can browse communication cards, build sentences, and use text-to-speech/speech-to-text features. Caregivers can manage categories, upload custom icons, and add/edit predefined sentences.

### Tech Stack Detected
- Backend: Python + Flask ([app.py](app.py#L1), [app.py](app.py#L38))
- Frontend: HTML (Jinja templates), CSS, JavaScript ([templates/base.html](templates/base.html#L1), [static/css/style.css](static/css/style.css#L1), [static/js/script.js](static/js/script.js#L1))
- Storage: JSON file persistence ([data.json](data.json#L1), [app.py](app.py#L53))
- File handling: Werkzeug secure file naming ([app.py](app.py#L7))
- External integrations:
  - Emoji picker CDN ([templates/base.html](templates/base.html#L10))
  - ResponsiveVoice CDN ([templates/base.html](templates/base.html#L100))
  - Google Translate TTS proxied via backend ([app.py](app.py#L524))
- Build/package tools: None detected (no package manifest/requirements file present)

## 2. Project Structure
### Annotated Directory Tree (Top Levels)
- `app.py` - Main Flask server with routes, auth, CRUD, and TTS proxy
- `data.json` - Application data store (users, icons, sentences, categories)
- `add_images.py` - Utility script to bulk-copy images and append icon records
- `templates/` - Jinja HTML pages
  - `base.html` - Shared layout/navigation/scripts
  - `login.html`, `register.html` - Authentication pages
  - `user_home.html`, `caregiver_home.html` - Role landing pages
  - `communication_board.html`, `categories.html`, `category_items.html` - User communication views
  - `caregiver_dashboard.html`, `view_uploaded_content.html`, `add_sentences.html`, `manage_categories.html` - Caregiver management views
  - `sentence_builder.html`, `tts.html`, `stt.html`, `caregiver_custom.html` - Feature-specific pages
- `static/` - Client assets
  - `css/style.css` - Main application stylesheet
  - `js/script.js` - Main client behavior script
  - `images/` + `images/custom/` - Static and uploaded images
- Root legacy static prototype files:
  - `index.html`, `script.js`, `style.css`
- `.vscode/launch.json` - VS Code debug launch profiles
- `users.db` - Present in repo, not used by current code

### Purpose of Major Folders and Key Files
- Backend logic and routing are centralized in [app.py](app.py#L1).
- UI rendering is handled by templates under [templates/base.html](templates/base.html#L1).
- Shared browser interactivity lives in [static/js/script.js](static/js/script.js#L1).
- Visual system/theme and responsive styling are in [static/css/style.css](static/css/style.css#L1).
- Persistent runtime data is read/written in [app.py](app.py#L53) and [app.py](app.py#L70) to [data.json](data.json#L1).

## 3. Core Modules / Components
### A. Flask Application Core
- File path: [app.py](app.py#L1)
- What it does:
  - Initializes Flask app, session secret, storage paths
  - Handles authentication and role-based access
  - Serves feature pages for user/caregiver
  - Processes caregiver CRUD actions
  - Proxies TTS audio requests
- Key functions/classes exposed:
  - Data TypedDicts: [UserDict](app.py#L10), [IconDict](app.py#L15), [CategoryDict](app.py#L22), [SentenceDict](app.py#L26), [AppDataRequired](app.py#L30)
  - Data layer: [load_data](app.py#L53), [save_data](app.py#L70), [allowed_file](app.py#L74)
  - Auth: [register](app.py#L78), [login](app.py#L114), [logout](app.py#L517)
  - Caregiver CRUD: [add_icon](app.py#L259), [edit_icon](app.py#L311), [delete_icon](app.py#L335), [save_sentence](app.py#L370), [edit_sentence](app.py#L395), [delete_sentence](app.py#L416), [save_category](app.py#L444), [edit_category](app.py#L469), [delete_category](app.py#L499)
  - TTS proxy: [tts](app.py#L524)
- Dependencies:
  - Flask and Werkzeug ([app.py](app.py#L1), [app.py](app.py#L7))
  - Python stdlib os/json/uuid/urllib

### B. Frontend Behavior Layer
- File path: [static/js/script.js](static/js/script.js#L1)
- What it does:
  - Word selection and sentence chip rendering
  - TTS audio playback via backend `/tts`
  - Keyboard input and view toggles
  - Category filtering and sidebar control
  - Caregiver edit modal handling
  - STT mic recognition handling
- Key functions exposed:
  - [speakText](static/js/script.js#L60), [speakSentence](static/js/script.js#L91), [window.speakWord](static/js/script.js#L115)
  - [window.filterCategory](static/js/script.js#L228), [window.toggleMobileMenu](static/js/script.js#L267)
  - [window.openEditModal](static/js/script.js#L304), [window.closeEditModal](static/js/script.js#L329)
  - [speakTTSConverterText](static/js/script.js#L349), [startRecognition](static/js/script.js#L360)
- Dependencies:
  - Browser APIs: Audio, SpeechSynthesis, SpeechRecognition
  - Backend `/tts` endpoint in [app.py](app.py#L523)

### C. Shared Layout Template
- File path: [templates/base.html](templates/base.html#L1)
- What it does:
  - Defines global page shell, nav/sidebar, script/style includes
  - Switches nav links by session role
- Key interfaces:
  - Jinja blocks: title/head/content/scripts
  - Shared JS include: [templates/base.html](templates/base.html#L101)
- Dependencies:
  - Flask template context (`session`, `request`, `url_for`)

### D. Styling System
- File path: [static/css/style.css](static/css/style.css#L1)
- What it does:
  - Defines theme variables, component styles, keyboard/modal/card classes
  - Handles responsive menu behaviors and role visual themes
- Key style anchors:
  - Theme variables: [static/css/style.css](static/css/style.css#L2)
  - Sidebar styles: [static/css/style.css](static/css/style.css#L230)
  - Word cards and category color classes: [static/css/style.css](static/css/style.css#L595), [static/css/style.css](static/css/style.css#L795)
  - Keyboard key styles: [static/css/style.css](static/css/style.css#L1104)

### E. Data Store
- File path: [data.json](data.json#L1)
- What it does:
  - Stores users, icons, sentences, and categories in a single JSON document
- Interfaces:
  - Read/write by [load_data](app.py#L53) and [save_data](app.py#L70)

### F. Bulk Image Import Utility
- File path: [add_images.py](add_images.py#L1)
- What it does:
  - Copies predefined image files and appends generated icon entries to `data.json`
- Key methods:
  - Paths configured in [add_images.py](add_images.py#L7) and [add_images.py](add_images.py#L8)
  - Copy + append loop in [add_images.py](add_images.py#L37)

## 4. Entry Points & Data Flow
### Entry Point(s)
- Primary server entry:
  - Flask app creation at [app.py](app.py#L38)
  - Run command at [app.py](app.py#L546)
- Legacy static entry (not current Flask flow):
  - [index.html](index.html#L1)

### High-Level Data/Control Flow
1. Browser requests a route (example: [app.py](app.py#L113), [app.py](app.py#L180), [app.py](app.py#L238)).
2. Route validates role/session where required (multiple guards such as [app.py](app.py#L147), [app.py](app.py#L231)).
3. Route reads app state from JSON via [load_data](app.py#L53).
4. Backend renders a Jinja template with context (for example [app.py](app.py#L187), [app.py](app.py#L246)).
5. Client-side interactions run via [static/js/script.js](static/js/script.js#L1).
6. Caregiver form submissions hit POST endpoints, mutate JSON through [save_data](app.py#L70), and redirect.
7. TTS requests from JS hit backend `/tts` ([app.py](app.py#L523)); backend fetches audio and streams MPEG response.

## 5. Key APIs / Interfaces
### HTTP Endpoints (Public Interfaces)
- Auth:
  - `GET/POST /register` ([app.py](app.py#L77))
  - `GET/POST /` login ([app.py](app.py#L113))
  - `GET /logout` ([app.py](app.py#L516))
- User functionality:
  - `/user_home` ([app.py](app.py#L155))
  - `/communication_board` ([app.py](app.py#L180))
  - `/sentence_builder` ([app.py](app.py#L189))
  - `/text_to_speech` ([app.py](app.py#L196))
  - `/speech_to_text` ([app.py](app.py#L203))
  - `/categories` ([app.py](app.py#L210))
  - `/category/<category_name>` ([app.py](app.py#L218))
  - `/caregiver_content` ([app.py](app.py#L163))
- Caregiver functionality:
  - `/caregiver_home` ([app.py](app.py#L230))
  - `/caregiver` ([app.py](app.py#L238))
  - `/caregiver/view_content` ([app.py](app.py#L248))
  - `POST /caregiver/add` ([app.py](app.py#L258))
  - `POST /caregiver/edit_icon/<item_id>` ([app.py](app.py#L310))
  - `POST /caregiver/delete/<item_id>` ([app.py](app.py#L334))
  - `GET /caregiver/sentences` ([app.py](app.py#L359))
  - `POST /caregiver/sentences/add` ([app.py](app.py#L369))
  - `POST /caregiver/sentences/edit/<sentence_id>` ([app.py](app.py#L394))
  - `POST /caregiver/sentences/delete/<sentence_id>` ([app.py](app.py#L415))
  - `GET /caregiver/categories` ([app.py](app.py#L433))
  - `POST /caregiver/categories/add` ([app.py](app.py#L443))
  - `POST /caregiver/categories/edit/<category_id>` ([app.py](app.py#L468))
  - `POST /caregiver/categories/delete/<category_id>` ([app.py](app.py#L498))
- Utility API:
  - `GET /tts?text=...&lang=...` ([app.py](app.py#L523))

### Frontend Interfaces Used by Templates
- Menu toggle: [window.toggleMobileMenu](static/js/script.js#L267) used in [templates/base.html](templates/base.html#L19)
- Category filter: [window.filterCategory](static/js/script.js#L228) used in [templates/communication_board.html](templates/communication_board.html#L20)
- Modal editing API: [window.openEditModal](static/js/script.js#L304) used in [templates/view_uploaded_content.html](templates/view_uploaded_content.html#L47)
- STT start trigger: [startRecognition](static/js/script.js#L360) used in [templates/stt.html](templates/stt.html#L19)

## 6. Configuration & Environment
- Flask/session config:
  - Dynamic secret key: [app.py](app.py#L39)
- Storage/file config:
  - Data path constant: [app.py](app.py#L42)
  - Upload folder constants: [app.py](app.py#L43), [app.py](app.py#L44)
  - Allowed extensions: [app.py](app.py#L47)
  - Folder bootstrap: [app.py](app.py#L50)
- Runtime mode:
  - Debug mode and port hardcoded in [app.py](app.py#L546)
- VS Code environment setup:
  - Launch profiles in [.vscode/launch.json](.vscode/launch.json#L1)
  - Workspace file in [AAC-Web_Project.code-workspace](AAC-Web_Project.code-workspace#L1)
- Environment variables / build variants:
  - No explicit environment variable loading found
  - No debug/release profile split beyond `debug=True` in script run mode

## 7. Known Patterns & Design Decisions
- Monolithic backend architecture: routing, auth, storage, and integration in one module ([app.py](app.py#L1)).
- Role-based access control implemented via session checks inside each route ([app.py](app.py#L147), [app.py](app.py#L239)).
- File-based persistence (JSON) chosen over DB/ORM for simplicity ([app.py](app.py#L53), [data.json](data.json#L1)).
- Server-side rendered pages with shared base layout and client-side enhancements ([templates/base.html](templates/base.html#L1), [static/js/script.js](static/js/script.js#L1)).
- TTS proxy route designed to improve reliability/cross-origin behavior compared to direct browser calls ([app.py](app.py#L524), [static/js/script.js](static/js/script.js#L69)).
- Category rename propagates to icon `type` values to preserve associations ([app.py](app.py#L469)).
- Mixed-generation codebase exists:
  - Active path: Flask + templates + static assets
  - Legacy path: root static prototype files ([index.html](index.html#L1), [script.js](script.js#L1), [style.css](style.css#L1))
- Potential maintenance flags:
  - `users.db` present but unused by code search
  - `add_images.py` uses machine-specific absolute paths ([add_images.py](add_images.py#L7), [add_images.py](add_images.py#L8))
