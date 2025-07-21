from flask import Blueprint, render_template, jsonify
from flask_login import login_required
from sqlalchemy import func
from .models import db, QueryLog

analytics_bp = Blueprint("analytics", __name__, url_prefix="/admin")

@analytics_bp.route("/analytics")
@login_required
def analytics():
    # Top 10 most‑queried indicators
    data = (
        db.session.query(QueryLog.indicator, func.count(QueryLog.id))
        .group_by(QueryLog.indicator)
        .order_by(func.count(QueryLog.id).desc())
        .limit(10)
        .all()
    )
    return render_template("analytics.html", data=data)

@analytics_bp.route("/api/indicator_counts")
@login_required
def indicator_counts():
    data = (
        db.session.query(QueryLog.indicator, func.count(QueryLog.id))
        .group_by(QueryLog.indicator)
        .all()
    )
    return jsonify({ind: cnt for ind, cnt in data})
