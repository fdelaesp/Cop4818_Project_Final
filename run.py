# run.py
from app import create_app

app = create_app()

if __name__ == "__main__":
    # debug=True only for local testing
    app.run(debug=True)

from app import create_app

app = create_app()
