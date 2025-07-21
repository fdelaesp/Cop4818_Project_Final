from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from .models import db, Indicator, QueryLog

main_bp = Blueprint("main", __name__)

@main_bp.route("/", methods=["GET", "POST"])
def index():
    indicators = Indicator.query.order_by(Indicator.name).all()
    if request.method == "POST":
        indicator_id = request.form.get("indicator")
        ind = Indicator.query.get(indicator_id)
        if not ind:
            flash("Indicator not found.", "danger")
            return render_template("index.html", indicators=indicators)

        # Log the query (for analytics)
        if current_user.is_authenticated:
            log = QueryLog(user_id=current_user.id, indicator=ind.name)
            db.session.add(log)
            db.session.commit()

        return render_template("results.html", indicator=ind)

    return render_template("index.html", indicators=indicators)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)

