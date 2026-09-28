# Anonymous Student Complaint Portal

## Files
- `app.py`: Flask website and MySQL connection
- `database.sql`: creates the three complaint tables
- `requirements.txt`: Python dependencies

## Categories
- Complaint about teachers (Accountancy, Economics, Computer Science, IP,
  English Commerce, English, Maths, Physics, Biology, Chemistry, PT)
- Complaint against principal
- School playground / environment

No name, email, or feelings field is collected.

## Run locally
1. Install Python and MySQL.
2. Run `database.sql` in MySQL Workbench.
3. In a terminal in this folder, run:
   `pip install -r requirements.txt`
4. Set environment variables for the database (examples below), then run:
   `python app.py`
5. Open http://127.0.0.1:5000

Windows PowerShell example:
```powershell
$env:DB_HOST="localhost"
$env:DB_PORT="3306"
$env:DB_USER="root"
$env:DB_PASSWORD="your-local-password"
$env:DB_NAME="student_complaints"
$env:DB_SSL="false"
python app.py
```

## Deploy publicly (Render + managed MySQL)
1. Create a private GitHub repository and upload these files.
2. Create a managed MySQL database with a provider such as Aiven.
3. Run `database.sql` on that database using its SQL connection details.
4. Create a Render Web Service connected to the repository.
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn app:app`
5. In the Render service's Environment settings, add:
   `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`.
   Set `DB_SSL=true` (default). If your provider supplies a CA certificate,
   save it as a secret file and set `DB_SSL_CA` to its path.
6. Deploy. Render will provide a public `https://...onrender.com` URL.

Do not commit database credentials, CA certificates, or real complaint data.
Keep the database private and grant access only to the web service.
For production, disable debug mode (this app uses Gunicorn), add rate limiting
and a school-approved process for handling sensitive complaints.

## Important privacy limitation
The form does not request or store names or email addresses. A public hosting
provider may still process IP addresses and request logs. Do not promise
absolute anonymity. Use sample complaints for testing and obtain school
permission before collecting real complaints.
