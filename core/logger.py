import json
import sqlite3
import datetime
from config.config import DATA_DIR, LOGS_DIR

SUCCESS_LOG = LOGS_DIR / "success.log"
ERROR_LOG = LOGS_DIR / "error.log"
POST_LOG = DATA_DIR / "post_log.jsonl"
DB_PATH = DATA_DIR / "history.db"

# Initialize Database
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        date TEXT,
        day TEXT,
        topic TEXT,
        content TEXT,
        status TEXT,
        image_path TEXT,
        post_id TEXT,
        image_prompt TEXT
    )
    """)
    conn.commit()
    conn.close()

init_db()

def log_success(entry: dict):
    entry["status"] = "SUCCESS"
    timestamp = datetime.datetime.now().isoformat()
    entry["timestamp"] = timestamp
    
    # Save to JSONL
    with open(SUCCESS_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")
    with open(POST_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")
    
    # Save to SQLite
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO posts (timestamp, date, day, topic, content, status, image_path, post_id, image_prompt) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            timestamp,
            datetime.date.today().isoformat(),
            datetime.datetime.now().strftime("%A"),
            entry.get("topic"),
            entry.get("post"), # From formatter/summarizer
            "SUCCESS",
            entry.get("image"),
            entry.get("post_id"),
            entry.get("image_prompt")
        )
    )
    conn.commit()
    conn.close()

def delete_post(timestamp: str):
    """Deletes a post from history database and log files."""
    # 1. Delete from SQLite
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM posts WHERE timestamp = ?", (timestamp,))
    conn.commit()
    conn.close()

    # 2. Delete from post_log.jsonl
    if POST_LOG.exists():
        with open(POST_LOG, 'r') as f:
            lines = f.readlines()
        with open(POST_LOG, 'w') as f:
            for line in lines:
                try:
                    data = json.loads(line)
                    if data.get('timestamp') != timestamp:
                        f.write(line)
                except:
                    if timestamp not in line:
                        f.write(line)
    
    # 3. Delete from success.log
    if SUCCESS_LOG.exists():
        with open(SUCCESS_LOG, 'r') as f:
            lines = f.readlines()
        with open(SUCCESS_LOG, 'w') as f:
            for line in lines:
                try:
                    data = json.loads(line)
                    if data.get('timestamp') != timestamp:
                        f.write(line)
                except:
                    if timestamp not in line:
                        f.write(line)
    print(f"🗑️ Post with timestamp {timestamp} deleted from history.")

def log_error(error_msg: str, context: dict = None):
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "status": "ERROR",
        "error": error_msg,
        "context": context
    }
    with open(ERROR_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")
    print(f"❌ Error logged: {error_msg}")

def is_duplicate(topic: str) -> bool:
    if not DB_PATH.exists():
        return False
        
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id FROM posts WHERE topic = ? AND status = 'SUCCESS'", (topic,))
    result = c.fetchone()
    conn.close()
    if result:
        return True
    
    # Fallback to JSONL check
    if not POST_LOG.exists():
        return False
    with open(POST_LOG, "r") as f:
        return topic.lower() in f.read().lower()

def get_last_post_date():
    if not DB_PATH.exists():
        return None
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT timestamp FROM posts WHERE status = 'SUCCESS' ORDER BY id DESC LIMIT 1")
        result = c.fetchone()
        conn.close()
        if result:
            return datetime.datetime.fromisoformat(result[0]).date()
    except Exception:
        pass
        
    # Fallback to JSONL
    try:
        with open(POST_LOG, "r") as f:
            lines = f.readlines()
            if not lines: return None
            last_line = json.loads(lines[-1])
            return datetime.datetime.fromisoformat(last_line["timestamp"]).date()
    except Exception as e:
        log_error(f"Failed to read last post date: {e}")
        return None
