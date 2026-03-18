from flask import Flask, render_template, request, redirect, session, url_for, flash, Response
import os
import json
import uuid
import urllib.request
import urllib.parse
from werkzeug.utils import secure_filename
from typing import Dict, Any, List, TypedDict, cast

class UserDict(TypedDict):
    password: str
    role: str
    name: str

class IconDict(TypedDict, total=False):
    id: str
    word: str
    type: str
    is_emoji: bool
    content: str

class CategoryDict(TypedDict):
    id: str
    name: str

class SentenceDict(TypedDict):
    id: str
    text: str

class AppDataRequired(TypedDict):
    users: Dict[str, UserDict]
    icons: List[IconDict]

class AppData(AppDataRequired, total=False):
    categories: List[CategoryDict]
    sentences: List[SentenceDict]

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Setup Storage Paths
DATA_FILE = "data.json"
UPLOAD_FOLDER = os.path.join('static', 'images')
CUSTOM_UPLOAD_FOLDER = os.path.join(UPLOAD_FOLDER, 'custom')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CUSTOM_UPLOAD_FOLDER'] = CUSTOM_UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Ensure the upload folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CUSTOM_UPLOAD_FOLDER, exist_ok=True)

def load_data() -> AppData:
    if not os.path.exists(DATA_FILE):
        return {"users": {}, "icons": [], "categories": []}
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = cast(AppData, json.load(f))
        if "categories" not in data:
            data["categories"] = cast(List[CategoryDict], [
                {"id": str(uuid.uuid4()), "name": "Vehicles"},
                {"id": str(uuid.uuid4()), "name": "Colors"},
                {"id": str(uuid.uuid4()), "name": "Flowers"},
                {"id": str(uuid.uuid4()), "name": "Human Body Parts"},
                {"id": str(uuid.uuid4()), "name": "Animals"},
                {"id": str(uuid.uuid4()), "name": "Fruits"}
            ])
            save_data(data)
        return data

def save_data(data: AppData) -> None:
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/register", methods=["GET", "POST"])
def register():
    if "user" in session:
        if session.get("role") == "user":
            return redirect(url_for("user_home"))
        else:
            return redirect(url_for("caregiver_home"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        role_type = request.form.get("role_type", "").strip()
        name = request.form.get("name", "").strip()

        if not username or not password or not role_type or not name:
            flash("എല്ലാ വിവരങ്ങളും നിർബന്ധമാണ്. (All fields are required.)", "error")
            return redirect(url_for("register"))

        data = load_data()
        
        if username in data["users"]:
            flash("ഈ യൂസർനെയിം നിലവിലുണ്ട്. ദയവായി മറ്റൊന്ന് തിരഞ്ഞെടുക്കുക. (Username already exists. Please choose a different one.)", "error")
            return redirect(url_for("register"))

        data["users"][username] = UserDict(
            password=password,
            role=role_type,
            name=name
        )
        
        save_data(data)
        flash("രജിസ്ട്രേഷൻ വിജയിച്ചു! നിങ്ങൾക്ക് ഇപ്പോൾ ലോഗിൻ ചെയ്യാം. (Registration successful! You can now sign in.)", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/", methods=["GET", "POST"])
def login():
    if "user" in session:
        if session.get("role") == "user":
            return redirect(url_for("user_home"))
        else:
            return redirect(url_for("caregiver_home"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        login_type = request.form.get("login_type", "").strip()

        data = load_data()
        user = data["users"].get(username)

        if user and user["password"] == password:
            if user["role"] == login_type:
                session["user"] = username
                session["role"] = login_type
                session["name"] = user["name"]
                if login_type == "user":
                    return redirect(url_for("user_home"))
                else:
                    return redirect(url_for("caregiver_home"))
            else:
                flash(f"അക്കൗണ്ട് നിലവിലുണ്ട്, പക്ഷേ ഒരു {login_type.capitalize()} ആയിട്ടല്ല. (Account exists, but not as a {login_type.capitalize()}.)", "error")
        else:
            flash("തെറ്റായ യൂസർനെയിം അല്ലെങ്കിൽ പാസ്‌വേഡ്. (Invalid username or password.)", "error")

    return render_template("login.html")


@app.route("/user")
def user_dashboard():
    if "user" not in session or session.get("role") != "user":
        flash("ഈ പേജ് ആക്സസ് ചെയ്യാൻ ഒരു ഉപയോക്താവായി ലോഗിൻ ചെയ്യുക. (Please log in as a User to access this page.)", "error")
        return redirect(url_for("login"))
    
    data = load_data()
    return render_template("user_dashboard.html", name=session["name"], icons=data["icons"], categories=data.get("categories", []))

@app.route("/user_home")
def user_home():
    if "user" not in session or session.get("role") != "user":
        flash("ഈ പേജ് ആക്സസ് ചെയ്യാൻ ഒരു ഉപയോക്താവായി ലോഗിൻ ചെയ്യുക. (Please log in as a User to access this page.)", "error")
        return redirect(url_for("login"))
    
    return render_template("user_home.html", name=session["name"])

@app.route("/caregiver_content")
def caregiver_content():
    if "user" not in session or session.get("role") != "user":
        flash("ഈ പേജ് ആക്സസ് ചെയ്യാൻ ഒരു ഉപയോക്താവായി ലോഗിൻ ചെയ്യുക. (Please log in as a User to access this page.)", "error")
        return redirect(url_for("login"))
    
    data = load_data()
    sentences = data.get("sentences", [])
    return render_template("caregiver_custom.html", icons=data["icons"], sentences=sentences, name=session["name"])


@app.route("/home")
def home():
    # Anyone can view the home page
    data = load_data()
    return render_template("home.html", icons=data["icons"])

@app.route("/communication_board")
def communication_board():
    if "user" not in session or session.get("role") != "user":
        flash("ഈ പേജ് ആക്സസ് ചെയ്യാൻ ഒരു ഉപയോക്താവായി ലോഗിൻ ചെയ്യുക. (Please log in as a User to access this page.)", "error")
        return redirect(url_for("login"))
    data = load_data()
    icons = data["icons"]
    return render_template("communication_board.html", icons=icons, categories=data.get("categories", []))

@app.route("/sentence_builder")
def sentence_builder():
    if "user" not in session or session.get("role") != "user":
        flash("ഈ പേജ് ആക്സസ് ചെയ്യാൻ ഒരു ഉപയോക്താവായി ലോഗിൻ ചെയ്യുക. (Please log in as a User to access this page.)", "error")
        return redirect(url_for("login"))
    return render_template("sentence_builder.html", name=session.get("name", "User"))

@app.route("/text_to_speech")
def text_to_speech():
    if "user" not in session or session.get("role") != "user":
        flash("ഈ പേജ് ആക്സസ് ചെയ്യാൻ ഒരു ഉപയോക്താവായി ലോഗിൻ ചെയ്യുക. (Please log in as a User to access this page.)", "error")
        return redirect(url_for("login"))
    return render_template("tts.html", name=session.get("name", "User"))

@app.route("/speech_to_text")
def speech_to_text():
    if "user" not in session or session.get("role") != "user":
        flash("ഈ പേജ് ആക്സസ് ചെയ്യാൻ ഒരു ഉപയോക്താവായി ലോഗിൻ ചെയ്യുക. (Please log in as a User to access this page.)", "error")
        return redirect(url_for("login"))
    return render_template("stt.html", name=session.get("name", "User"))

@app.route("/categories")
def categories():
    if "user" not in session or session.get("role") != "user":
        flash("ഈ പേജ് ആക്സസ് ചെയ്യാൻ ഒരു ഉപയോക്താവായി ലോഗിൻ ചെയ്യുക. (Please log in as a User to access this page.)", "error")
        return redirect(url_for("login"))
    data = load_data()
    return render_template("categories.html", categories=data.get("categories", []))

@app.route("/category/<category_name>")
def category_items(category_name):
    if "user" not in session or session.get("role") != "user":
        flash("ഈ പേജ് ആക്സസ് ചെയ്യാൻ ഒരു ഉപയോക്താവായി ലോഗിൻ ചെയ്യുക. (Please log in as a User to access this page.)", "error")
        return redirect(url_for("login"))
    data = load_data()
    # Filter only custom icons that belong to this particular category
    category_icons = [icon for icon in data["icons"] if icon["type"] == category_name]
    
    # We pass the category_name to tell the template which hardcoded fallbacks to show
    return render_template("category_items.html", category=category_name, icons=category_icons)

@app.route("/caregiver_home")
def caregiver_home():
    if "user" not in session or session.get("role") != "caregiver":
        flash("ഈ പേജ് ആക്സസ് ചെയ്യാൻ ഒരു പരിചാരകനായി ലോഗിൻ ചെയ്യുക. (Please log in as a Caregiver to access this page.)", "error")
        return redirect(url_for("login"))
    
    return render_template("caregiver_home.html", name=session["name"])

@app.route("/caregiver")
def caregiver_dashboard():
    if "user" not in session or session.get("role") != "caregiver":
        flash("ഈ പേജ് ആക്സസ് ചെയ്യാൻ ഒരു പരിചാരകനായി ലോഗിൻ ചെയ്യുക. (Please log in as a Caregiver to access this page.)", "error")
        return redirect(url_for("login"))
    
    data = load_data()
    return render_template("caregiver_dashboard.html", name=session["name"], icons=data["icons"], categories=data.get("categories", []))


@app.route("/caregiver/view_content")
def view_content():
    if "user" not in session or session.get("role") != "caregiver":
        flash("ഈ പേജ് ആക്സസ് ചെയ്യാൻ ഒരു പരിചാരകനായി ലോഗിൻ ചെയ്യുക. (Please log in as a Caregiver to access this page.)", "error")
        return redirect(url_for("login"))
    
    data = load_data()
    return render_template("view_uploaded_content.html", name=session["name"], icons=data["icons"], sentences=data.get("sentences", []), categories=data.get("categories", []))


@app.route("/caregiver/add", methods=["POST"])
def add_icon():
    if "user" not in session or session.get("role") != "caregiver":
        return redirect(url_for("login"))
        
    word = request.form.get("word", "").strip()
    category = request.form.get("category", "").strip()
    
    if not word or not category:
        flash("വാക്കും വിഭാഗവും നിർബന്ധമാണ്. (Word and category are required.)", "error")
        return redirect(url_for("caregiver_dashboard"))
        
    data = load_data()
    new_id = str(uuid.uuid4())
    
    # Check if a file was uploaded
    if 'image' in request.files and request.files['image'].filename != '':
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(f"{new_id}_{file.filename}")
            # Save strictly to custom upload folder as requested
            file.save(os.path.join(app.config['CUSTOM_UPLOAD_FOLDER'], filename))
            
            data["icons"].append({
                "id": new_id,
                "word": word,
                "type": category,
                "is_emoji": False,
                # Include the leading path so rendering templates still find it properly from the static/images/ root
                "content": f"custom/{filename}"
            })
            save_data(data)
            flash(f"'{word}' എന്നതിനായുള്ള ചിത്രം വിജയകരമായി ചേർത്തു. (Successfully added image for '{word}')", "success")
        else:
            flash("അസാധുവായ ഫയൽ തരം. അനുവദനീയമായവ: png, jpg, jpeg, gif. (Invalid file type. Allowed types are png, jpg, jpeg, gif.)", "error")
    else:
        # Fallback to emoji input if they didn't provide a file but provided an emoji string
        emoji_text = request.form.get("emoji_text", "").strip()
        if emoji_text:
            data["icons"].append({
                "id": new_id,
                "word": word,
                "type": category,
                "is_emoji": True,
                "content": emoji_text
            })
            save_data(data)
            flash(f"'{word}' എന്നതിനായുള്ള ഇമോജി വിജയകരമായി ചേർത്തു. (Successfully added emoji for '{word}')", "success")
            flash("നിങ്ങൾ ഒരു ചിത്രമോ ഇമോജി ചിഹ്നമോ നൽകണം. (You must provide either an image file or an emoji symbol.)", "error")
            
    return redirect(url_for("caregiver_dashboard"))

@app.route("/caregiver/edit_icon/<item_id>", methods=["POST"])
def edit_icon(item_id):
    if "user" not in session or session.get("role") != "caregiver":
        return redirect(url_for("login"))
        
    word = request.form.get("word", "").strip()
    category = request.form.get("category", "").strip()
    
    if not word or not category:
        flash("വാക്കും വിഭാഗവും നിർബന്ധമാണ്. (Word and category are required.)", "error")
        return redirect(request.referrer or url_for("caregiver_dashboard"))
        
    data = load_data()
    
    for item in data["icons"]:
        if str(item.get("id")) == str(item_id):
            item["word"] = word
            item["type"] = category
            save_data(data)
            flash(f"'{word}' വിജയകരമായി അപ്ഡേറ്റ് ചെയ്തു. (Updated '{word}' successfully.)", "success")
            break
            
    return redirect(request.referrer or url_for("caregiver_dashboard"))

@app.route("/caregiver/delete/<item_id>", methods=["POST"])
def delete_icon(item_id):
    if "user" not in session or session.get("role") != "caregiver":
        return redirect(url_for("login"))
        
    data = load_data()
    
    # Find the item to potentially delete its image file
    item_to_delete = next((item for item in data["icons"] if str(item.get("id")) == str(item_id)), None)
    
    if item_to_delete:
        if not item_to_delete.get("is_emoji"):
            # Attempt to delete the physical image file
            try:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], item_to_delete["content"]))
            except OSError:
                pass # File might already be gone
                
        # Remove from array and save
        data["icons"] = [item for item in data["icons"] if str(item.get("id")) != str(item_id)]
        save_data(data)
        flash(f"'{item_to_delete['word']}' വിജയകരമായി ഇല്ലാതാക്കി. (Deleted '{item_to_delete['word']}' successfully.)", "success")
        
    return redirect(url_for("caregiver_dashboard"))

@app.route("/caregiver/sentences")
def add_sentences():
    if "user" not in session or session.get("role") != "caregiver":
        flash("ഈ പേജ് ആക്സസ് ചെയ്യാൻ ഒരു പരിചാരകനായി ലോഗിൻ ചെയ്യുക. (Please log in as a Caregiver to access this page.)", "error")
        return redirect(url_for("login"))
    
    data = load_data()
    sentences = data.get("sentences", [])
    return render_template("add_sentences.html", name=session["name"], sentences=sentences)

@app.route("/caregiver/sentences/add", methods=["POST"])
def save_sentence():
    if "user" not in session or session.get("role") != "caregiver":
        return redirect(url_for("login"))
        
    sentence_text = request.form.get("sentence_text", "").strip()
    
    if not sentence_text:
        flash("വാചകം നൽകുക. (Please enter a sentence.)", "error")
        return redirect(url_for("add_sentences"))
        
    data = load_data()
    if "sentences" not in data:
        data["sentences"] = []
        
    new_id = str(uuid.uuid4())
    data["sentences"].append({
        "id": new_id,
        "text": sentence_text
    })
    
    save_data(data)
    flash("വാചകം വിജയകരമായി ചേർത്തു. (Sentence added successfully.)", "success")
    return redirect(url_for("add_sentences"))

@app.route("/caregiver/sentences/edit/<sentence_id>", methods=["POST"])
def edit_sentence(sentence_id):
    if "user" not in session or session.get("role") != "caregiver":
        return redirect(url_for("login"))
        
    new_text = request.form.get("new_text", "").strip()
    if not new_text:
        flash("വാചകം നൽകുക. (Please enter a sentence.)", "error")
        return redirect(url_for("add_sentences"))
        
    data = load_data()
    if "sentences" in data:
        for sentence in data["sentences"]:
            if str(sentence.get("id")) == str(sentence_id):
                sentence["text"] = new_text
                save_data(data)
                flash("വാചകം അപ്ഡേറ്റ് ചെയ്തു. (Sentence updated successfully.)", "success")
                break
                
    return redirect(url_for("add_sentences"))

@app.route("/caregiver/sentences/delete/<sentence_id>", methods=["POST"])
def delete_sentence(sentence_id):
    if "user" not in session or session.get("role") != "caregiver":
        return redirect(url_for("login"))
        
    data = load_data()
    
    if "sentences" in data:
        original_length = len(data["sentences"])
        data["sentences"] = [s for s in data["sentences"] if str(s.get("id")) != str(sentence_id)]
        
        if len(data["sentences"]) < original_length:
            save_data(data)
            flash("വാചകം ഇല്ലാതാക്കി. (Sentence deleted successfully.)", "success")
            
    return redirect(url_for("add_sentences"))


@app.route("/caregiver/categories")
def manage_categories():
    if "user" not in session or session.get("role") != "caregiver":
        flash("ഈ പേജ് ആക്സസ് ചെയ്യാൻ ഒരു പരിചാരകനായി ലോഗിൻ ചെയ്യുക. (Please log in as a Caregiver to access this page.)", "error")
        return redirect(url_for("login"))
    
    data = load_data()
    categories_list = data.get("categories", [])
    return render_template("manage_categories.html", name=session["name"], categories=categories_list)

@app.route("/caregiver/categories/add", methods=["POST"])
def save_category():
    if "user" not in session or session.get("role") != "caregiver":
        return redirect(url_for("login"))
        
    category_name = request.form.get("category_name", "").strip()
    
    if not category_name:
        flash("വിഭാഗത്തിന്റെ പേര് നൽകുക. (Please enter a category name.)", "error")
        return redirect(url_for("manage_categories"))
        
    data = load_data()
    if "categories" not in data:
        data["categories"] = []
        
    new_id = str(uuid.uuid4())
    data["categories"].append({
        "id": new_id,
        "name": category_name
    })
    
    save_data(data)
    flash("വിഭാഗം വിജയകരമായി ചേർത്തു. (Category added successfully.)", "success")
    return redirect(url_for("manage_categories"))

@app.route("/caregiver/categories/edit/<category_id>", methods=["POST"])
def edit_category(category_id):
    if "user" not in session or session.get("role") != "caregiver":
        return redirect(url_for("login"))
        
    new_name = request.form.get("new_name", "").strip()
    if not new_name:
        flash("വിഭാഗത്തിന്റെ പേര് നൽകുക. (Please enter a category name.)", "error")
        return redirect(url_for("manage_categories"))
        
    data = load_data()
    if "categories" in data:
        old_name = None
        for category in data["categories"]:
            if str(category.get("id")) == str(category_id):
                old_name = category["name"]
                category["name"] = new_name
                break
                
        # If the category name was changed, update all icons associated with old_name
        if old_name and old_name != new_name and "icons" in data:
            for icon in data["icons"]:
                if icon.get("type") == old_name:
                    icon["type"] = new_name
                    
        save_data(data)
        flash("വിഭാഗം അപ്ഡേറ്റ് ചെയ്തു. (Category updated successfully.)", "success")
                
    return redirect(url_for("manage_categories"))

@app.route("/caregiver/categories/delete/<category_id>", methods=["POST"])
def delete_category(category_id):
    if "user" not in session or session.get("role") != "caregiver":
        return redirect(url_for("login"))
        
    data = load_data()
    
    if "categories" in data:
        original_length = len(data["categories"])
        data["categories"] = [c for c in data["categories"] if str(c.get("id")) != str(category_id)]
        
        if len(data["categories"]) < original_length:
            save_data(data)
            flash("വിഭാഗം ഇല്ലാതാക്കി. (Category deleted successfully.)", "success")
            
    return redirect(url_for("manage_categories"))


@app.route("/logout")
def logout():
    session.clear()
    flash("നിങ്ങൾ വിജയകരമായി ലോഗ് ഔട്ട് ചെയ്തു. (You have been successfully logged out.)", "success")
    return redirect(url_for("login"))


@app.route("/tts")
def tts():
    """Proxy route to fetch TTS audio securely from the backend to bypass browser restrictions."""
    text = request.args.get("text", "").strip()
    lang = request.args.get("lang", "ml").strip()
    if not text:
        return "", 400
    
    # Use tw-ob client for stable audio retrieval
    url = f"https://translate.googleapis.com/translate_tts?ie=UTF-8&q={urllib.parse.quote(text)}&tl={lang}&client=tw-ob"

    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    
    try:
        with urllib.request.urlopen(req) as response:
            audio_data = response.read()
            return Response(audio_data, mimetype="audio/mpeg")
    except Exception as e:
        print("TTS Error:", e)
        return "Audio Generation Failed", 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)