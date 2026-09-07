"""
Run the Quiz Master app locally:

    pip install -r requirements.txt
    python run.py

Then open http://localhost:5000

On first run this will automatically import the quiz datasets from
app/data_source/ into the database — this can take a minute or two
because of the large CSV files. Subsequent runs are instant.
"""
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
