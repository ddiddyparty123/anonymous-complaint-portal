import os
from flask import Flask, request, render_template_string
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024  # Limit request size

SUBJECTS = [
    "Accountancy", "Economics", "Computer Science", "IP",
    "English Commerce", "English", "Maths", "Physics",
    "Biology", "Chemistry", "PT"
]
CATEGORIES = {
    "teacher": "teacher_complaints",
    "principal": "principal_complaints",
    "environment": "environment_complaints"
}

def get_db():
    # Set these values as environment variables in your hosting provider.
    config = {
        "host": os.environ["DB_HOST"],
        "port": int(os.environ.get("DB_PORT", "3306")),
        "user": os.environ["DB_USER"],
        "password": os.environ["DB_PASSWORD"],
        "database": os.environ["DB_NAME"],
        "connection_timeout": 10,
    }
    # Aiven and many managed MySQL providers require TLS.
    ca_path = os.environ.get("DB_SSL_CA")
    if ca_path:
        config["ssl_ca"] = ca_path
        config["ssl_verify_cert"] = True
        config["ssl_verify_identity"] = True
    elif os.environ.get("DB_SSL", "true").lower() == "true":
        config["ssl_disabled"] = False
    return mysql.connector.connect(**config)

HTML = """
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Student Complaint Portal</title>
<style>
*{box-sizing:border-box}
body{margin:0;padding:28px 16px;background:#f1f5f9;color:#172033;font-family:Arial,sans-serif}
.card{max-width:660px;margin:20px auto;background:#fff;padding:32px;border-radius:16px;box-shadow:0 8px 30px #0f172a12}
h1{text-align:center;color:#1d4ed8;margin:0 0 8px}
.subtitle{text-align:center;color:#64748b;line-height:1.5;margin:0 0 26px}
label{display:block;font-weight:700;margin:20px 0 8px}
select,textarea{width:100%;padding:13px;border:1px solid #cbd5e1;border-radius:8px;background:#fff;font:15px Arial}
textarea{min-height:160px;resize:vertical}
select:focus,textarea:focus{outline:2px solid #93c5fd;border-color:#2563eb}
button{width:100%;margin-top:24px;padding:14px;border:0;border-radius:8px;background:#2563eb;color:#fff;font-size:16px;font-weight:700;cursor:pointer}
button:hover{background:#1e40af}
.note{margin-top:20px;padding:13px;border-radius:8px;background:#eff6ff;color:#1e40af;font-size:13px;line-height:1.5}
.success,.error{padding:13px;border-radius:8px;margin:0 0 18px;text-align:center}
.success{background:#dcfce7;color:#166534}.error{background:#fee2e2;color:#991b1b}
.hidden{display:none}
</style>
</head>
<body><main class="card">
<h1>Student Complaint Portal</h1>
<p class="subtitle">Share your concerns anonymously. Your voice matters.</p>
{% if success %}<div class="success" role="status">Your complaint was submitted successfully.</div>{% endif %}
{% if error %}<div class="error" role="alert">{{ error }}</div>{% endif %}
<form method="post" action="/" autocomplete="off">
<label for="category">Complaint Category</label>
<select name="category" id="category" required>
<option value="">Choose a category</option>
<option value="teacher">Complaint about teachers</option>
<option value="principal">Complaint against principal</option>
<option value="environment">School playground / environment</option>
</select>
<div id="subject-box" class="hidden">
<label for="subject">Select Subject</label>
<select name="subject" id="subject">
<option value="">Choose a subject</option>
{% for item in subjects %}<option value="{{ item }}">{{ item }}</option>{% endfor %}
</select></div>
<label for="complaint">Describe Your Complaint</label>
<textarea name="complaint" id="complaint" maxlength="5000" required
placeholder="Explain your concern here. Please avoid including names or other identifying details."></textarea>
<button type="submit">Submit Complaint</button>
</form>
<div class="note">This form does not ask for your name or email. Avoid including identifying personal information in your complaint.</div>
</main>
<script>
const category=document.getElementById("category");
const subjectBox=document.getElementById("subject-box");
const subject=document.getElementById("subject");
function updateSubject(){
  const isTeacher=category.value==="teacher";
  subjectBox.classList.toggle("hidden",!isTeacher);
  subject.required=isTeacher;
  if(!isTeacher) subject.value="";
}
category.addEventListener("change",updateSubject);
updateSubject();
</script>
</body></html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    success = False
    error = ""
    if request.method == "POST":
        category = request.form.get("category", "")
        subject = request.form.get("subject", "").strip()
        complaint = request.form.get("complaint", "").strip()

        if category not in CATEGORIES:
            error = "Please choose a valid complaint category."
        elif not complaint or len(complaint) > 5000:
            error = "Please enter a complaint of up to 5000 characters."
        elif category == "teacher" and subject not in SUBJECTS:
            error = "Please choose a valid subject."
        else:
            conn = None
            cursor = None
            try:
                conn = get_db()
                cursor = conn.cursor()
                table = CATEGORIES[category]  # Fixed allow-list, not user SQL.
                if category == "teacher":
                    cursor.execute(
                        f"INSERT INTO {table} (subject, complaint) VALUES (%s, %s)",
                        (subject, complaint)
                    )
                else:
                    cursor.execute(
                        f"INSERT INTO {table} (complaint) VALUES (%s)",
                        (complaint,)
                    )
                conn.commit()
                success = True
            except (Error, KeyError, ValueError):
                if conn:
                    conn.rollback()
                app.logger.exception("Complaint submission failed")
                error = "We could not save your complaint. Please try again later."
            finally:
                if cursor:
                    cursor.close()
                if conn and conn.is_connected():
                    conn.close()

    return render_template_string(HTML, subjects=SUBJECTS,
                                  success=success, error=error)

if __name__ == "__main__":
    # Local development only. Use Gunicorn in production.
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", "5000")))
