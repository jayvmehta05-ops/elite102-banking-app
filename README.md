Vault Banking — Elite 102 Final Project
A banking app built with Python and MySQL. Supports a web UI (Gradio) and a terminal UI.
Files

# 1. Install dependencies
pip install mysql-connector-python gradio pandas

# 2. Open config.py and set your MySQL password

# 3. Create the database and tables
python setup_db.py

# 4. Run the web app
python app.py
# Open http://localhost:7860

# 5. Or run the terminal version
python main.py

# 6. Run the tests
python tests.py
