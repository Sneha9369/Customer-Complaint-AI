from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

import mysql.connector
from mysql.connector import Error

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from config import DB_CONFIG, SECRET_KEY

import uuid
import re


# ==================================================
# COMPLAINT AI ANALYSIS
# ==================================================

def analyze_complaint(subject, description):

    text = f"{subject} {description}".lower().strip()


    # ----------------------------------------------
    # CATEGORY KEYWORDS
    # ----------------------------------------------

    categories = {

        "Payment & Billing": [
            "payment",
            "charged",
            "charge",
            "billing",
            "bill",
            "money deducted",
            "amount deducted",
            "transaction failed",
            "payment failed",
            "double charged",
            "charged twice"
        ],

        "Refund & Cancellation": [
            "refund",
            "cancel",
            "cancelled",
            "cancellation",
            "money back",
            "return money",
            "refund pending"
        ],

        "Delivery & Shipping": [
            "delivery",
            "delivered",
            "shipping",
            "shipment",
            "parcel",
            "package",
            "order late",
            "late order",
            "not arrived",
            "not delivered"
        ],

        "Product Quality": [
            "damaged",
            "defective",
            "broken",
            "wrong product",
            "poor quality",
            "replacement",
            "product quality",
            "item damaged",
            "item broken"
        ],

        "Technical Issues": [
            "website",
            "app",
            "application",
            "technical",
            "server",
            "error",
            "crash",
            "not working",
            "network",
            "internet",
            "software",
            "page not loading"
        ],

        "Account & Login": [
            "login",
            "log in",
            "password",
            "account",
            "sign in",
            "otp",
            "locked",
            "cannot access",
            "unable to login"
        ],

        "Customer Service": [
            "customer service",
            "customer support",
            "support team",
            "staff",
            "employee",
            "rude",
            "behaviour",
            "behavior",
            "no response",
            "not responding"
        ],

        "Fraud & Security": [
            "fraud",
            "unauthorized",
            "unauthorised",
            "scam",
            "hacked",
            "security",
            "suspicious",
            "stolen",
            "unknown transaction",
            "did not make this transaction"
        ]
    }


    # ----------------------------------------------
    # IRRELEVANT INPUT
    # ----------------------------------------------

    irrelevant_patterns = [

        "python notes",
        "java notes",
        "exam notes",
        "give me notes",

        "weather today",
        "what is the weather",

        "cricket match",
        "football match",
        "who won",

        "give me a job",
        "need a job",
        "looking for a job",

        "hello how are you",
        "how are you",

        "write a program",
        "write code",

        "what is 2+2",
        "tell me a joke",

        "testing testing",
        "just testing",

        "my exam",
        "college exam",

        "my friend is not talking",
        "friend not talking"
    ]


    # ----------------------------------------------
    # CHECK CATEGORY SCORES
    # ----------------------------------------------

    category_scores = {}

    for category, keywords in categories.items():

        score = 0

        for keyword in keywords:

            if keyword in text:
                score += 1

        category_scores[category] = score


    best_category = max(
        category_scores,
        key=category_scores.get
    )

    best_score = category_scores[best_category]


    # ----------------------------------------------
    # IRRELEVANCE CHECK
    # ----------------------------------------------

    irrelevant_match = any(
        pattern in text
        for pattern in irrelevant_patterns
    )


    if irrelevant_match and best_score == 0:

        return {
            "relevance": "Irrelevant",
            "category": "Out of Scope",
            "confidence": 95.00,
            "sentiment": "N/A",
            "priority": "N/A",
            "department": "N/A"
        }


    # ----------------------------------------------
    # NO CATEGORY FOUND
    # Genuine complaint may still be "Other"
    # ----------------------------------------------

    if best_score == 0:

        complaint_words = [
            "problem",
            "issue",
            "complaint",
            "service",
            "bad",
            "poor",
            "failed",
            "help",
            "resolve"
        ]

        looks_like_complaint = any(
            word in text
            for word in complaint_words
        )


        if looks_like_complaint:

            relevance = "Relevant"
            category = "Other"

        else:

            return {
                "relevance": "Irrelevant",
                "category": "Out of Scope",
                "confidence": 80.00,
                "sentiment": "N/A",
                "priority": "N/A",
                "department": "N/A"
            }

    else:

        relevance = "Relevant"
        category = best_category


    # ----------------------------------------------
    # CONFIDENCE
    # ----------------------------------------------

    if best_score >= 3:
        confidence = 96.00

    elif best_score == 2:
        confidence = 91.00

    elif best_score == 1:
        confidence = 84.00

    else:
        confidence = 70.00


    # ----------------------------------------------
    # SENTIMENT
    # ----------------------------------------------

    negative_words = [

        "bad",
        "poor",
        "worst",
        "angry",
        "disappointed",
        "terrible",
        "horrible",
        "damaged",
        "broken",
        "failed",
        "fraud",
        "unauthorized",
        "not working",
        "not received",
        "not delivered",
        "problem",
        "issue"
    ]


    positive_words = [

        "good",
        "great",
        "excellent",
        "happy",
        "satisfied",
        "thank",
        "thanks"
    ]


    negative_score = sum(
        1 for word in negative_words
        if word in text
    )

    positive_score = sum(
        1 for word in positive_words
        if word in text
    )


    if negative_score > positive_score:

        sentiment = "Negative"

    elif positive_score > negative_score:

        sentiment = "Positive"

    else:

        sentiment = "Neutral"


    # ----------------------------------------------
    # PRIORITY
    # ----------------------------------------------

    urgent_words = [

        "fraud",
        "unauthorized",
        "unauthorised",
        "hacked",
        "stolen",
        "emergency",
        "urgent",
        "immediately",
        "unknown transaction"
    ]


    high_words = [

        "money deducted",
        "charged twice",
        "double charged",
        "payment failed",
        "not received",
        "damaged",
        "broken",
        "refund pending"
    ]


    if any(word in text for word in urgent_words):

        priority = "Urgent"

    elif any(word in text for word in high_words):

        priority = "High"

    elif sentiment == "Negative":

        priority = "Medium"

    else:

        priority = "Low"


    # ----------------------------------------------
    # DEPARTMENT ROUTING
    # ----------------------------------------------

    department_map = {

        "Payment & Billing":
            "Billing Department",

        "Refund & Cancellation":
            "Refund Department",

        "Delivery & Shipping":
            "Logistics Department",

        "Product Quality":
            "Product Support",

        "Technical Issues":
            "Technical Support",

        "Account & Login":
            "Account Support",

        "Customer Service":
            "Customer Support",

        "Fraud & Security":
            "Security Department",

        "Other":
            "General Support"
    }


    department = department_map.get(
        category,
        "General Support"
    )


    return {

        "relevance": relevance,

        "category": category,

        "confidence": confidence,

        "sentiment": sentiment,

        "priority": priority,

        "department": department
    }

app = Flask(__name__)
app.secret_key = SECRET_KEY


# ==================================================
# DATABASE
# ==================================================

def get_db_connection():

    return mysql.connector.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"],
        port=DB_CONFIG["port"]
    )


# ==================================================
# HOME
# ==================================================

@app.route("/")
def home():

    return render_template("index.html")


# ==================================================
# REGISTER
# ==================================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get("name", "").strip()

        email = request.form.get(
            "email", ""
        ).strip().lower()

        password = request.form.get(
            "password", ""
        )

        confirm_password = request.form.get(
            "confirm_password", ""
        )


        if not name or not email or not password:

            flash(
                "Please fill all fields.",
                "danger"
            )

            return redirect(
                url_for("register")
            )


        if password != confirm_password:

            flash(
                "Passwords do not match.",
                "danger"
            )

            return redirect(
                url_for("register")
            )


        if len(password) < 6:

            flash(
                "Password must be at least 6 characters.",
                "danger"
            )

            return redirect(
                url_for("register")
            )


        connection = get_db_connection()

        cursor = connection.cursor(
            dictionary=True
        )


        cursor.execute(
            "SELECT id FROM users WHERE email=%s",
            (email,)
        )

        existing = cursor.fetchone()


        if existing:

            cursor.close()
            connection.close()

            flash(
                "Email already registered.",
                "danger"
            )

            return redirect(
                url_for("register")
            )


        hashed_password = generate_password_hash(
            password
        )


        cursor.execute(
            """
            INSERT INTO users
            (name,email,password,role)

            VALUES (%s,%s,%s,'customer')
            """,

            (
                name,
                email,
                hashed_password
            )
        )


        connection.commit()

        cursor.close()
        connection.close()


        flash(
            "Registration successful. Please login.",
            "success"
        )


        return redirect(
            url_for("login")
        )


    return render_template(
        "register.html"
    )


# ==================================================
# LOGIN
# ==================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get(
            "email", ""
        ).strip().lower()

        password = request.form.get(
            "password", ""
        )


        connection = get_db_connection()

        cursor = connection.cursor(
            dictionary=True
        )


        cursor.execute(
            "SELECT * FROM users WHERE email=%s",
            (email,)
        )

        user = cursor.fetchone()


        cursor.close()
        connection.close()


        if user and check_password_hash(
            user["password"],
            password
        ):

            session.clear()

            session["user_id"] = user["id"]

            session["name"] = user["name"]

            session["email"] = user["email"]

            session["role"] = user["role"]

            session["department"] = user.get("department")


            if user["role"] == "admin":

                return redirect(
                    url_for(
                        "admin_dashboard"
                    )
                )


            elif user["role"] == "employee":

                return redirect(
                    url_for(
                        "employee_dashboard"
                    )
                )


            return redirect(
                url_for(
                    "customer_dashboard"
                )
            )


        flash(
            "Invalid email or password.",
            "danger"
        )


    return render_template(
        "login.html"
    )


# ==================================================
# CUSTOMER DASHBOARD
# ==================================================

@app.route("/customer/dashboard")
def customer_dashboard():

    if (
        "user_id" not in session
        or session.get("role") != "customer"
    ):

        return redirect(
            url_for("login")
        )


    connection = get_db_connection()

    cursor = connection.cursor(
        dictionary=True
    )


    cursor.execute(
        """
        SELECT COUNT(*) total
        FROM complaints
        WHERE user_id=%s
        """,
        (session["user_id"],)
    )

    total = cursor.fetchone()["total"]


    cursor.execute(
        """
        SELECT COUNT(*) total
        FROM complaints

        WHERE user_id=%s
        AND status='Pending'
        """,
        (session["user_id"],)
    )

    pending = cursor.fetchone()["total"]


    cursor.execute(
        """
        SELECT COUNT(*) total
        FROM complaints

        WHERE user_id=%s
        AND status IN ('Assigned','In Progress')
        """,
        (session["user_id"],)
    )

    in_progress = cursor.fetchone()["total"]


    cursor.execute(
        """
        SELECT COUNT(*) total
        FROM complaints

        WHERE user_id=%s
        AND status='Resolved'
        """,
        (session["user_id"],)
    )

    resolved = cursor.fetchone()["total"]


    cursor.execute(
        """
        SELECT *
        FROM complaints

        WHERE user_id=%s

        ORDER BY created_at DESC

        LIMIT 5
        """,
        (session["user_id"],)
    )

    recent_complaints = cursor.fetchall()


    cursor.close()
    connection.close()


    return render_template(
        "customer_dashboard.html",

        name=session["name"],
        email=session["email"],

        total=total,
        pending=pending,
        in_progress=in_progress,
        resolved=resolved,

        recent_complaints=recent_complaints
    )


# ==================================================
# SUBMIT COMPLAINT
# ==================================================
# ==================================================
# SUBMIT COMPLAINT
# ==================================================

@app.route("/submit-complaint", methods=["GET", "POST"])
def submit_complaint():

    # ----------------------------------------------
    # LOGIN CHECK
    # ----------------------------------------------

    if (
        "user_id" not in session
        or session.get("role") != "customer"
    ):
        return redirect(url_for("login"))


    # ----------------------------------------------
    # FORM SUBMITTED
    # ----------------------------------------------

    if request.method == "POST":

        subject = request.form.get(
            "subject", ""
        ).strip()

        description = request.form.get(
            "description", ""
        ).strip()


        # ------------------------------------------
        # VALIDATION
        # ------------------------------------------

        if not subject or not description:

            flash(
                "Please fill all fields.",
                "danger"
            )

            return redirect(
                url_for("submit_complaint")
            )


        # ------------------------------------------
        # AI ANALYSIS
        # ------------------------------------------

        analysis = analyze_complaint(
            subject,
            description
        )


        relevance = analysis["relevance"]

        category = analysis["category"]

        confidence = analysis["confidence"]

        sentiment = analysis["sentiment"]

        priority = analysis["priority"]

        department = analysis["department"]


        # ------------------------------------------
        # DEBUG
        # ------------------------------------------

        print("\n==============================")
        print("SMARTCOMPLAINT AI ANALYSIS")
        print("==============================")

        print("Subject:", subject)

        print(
            "Description:",
            description
        )

        print(
            "Relevance:",
            relevance
        )

        print(
            "Category:",
            category
        )

        print(
            "Confidence:",
            confidence
        )

        print(
            "Sentiment:",
            sentiment
        )

        print(
            "Priority:",
            priority
        )

        print(
            "Department:",
            department
        )

        print("==============================\n")


        # ------------------------------------------
        # CREATE COMPLAINT ID
        # ------------------------------------------

        complaint_id = (
            "CMP-"
            + uuid.uuid4().hex[:8].upper()
        )


        # ------------------------------------------
        # STATUS
        # ------------------------------------------

        # Irrelevant complaints are automatically
        # rejected.

        if relevance == "Irrelevant":

            status = "Rejected"

        else:

            status = "Pending"


        connection = None
        cursor = None


        try:

            # --------------------------------------
            # DATABASE CONNECTION
            # --------------------------------------

            connection = get_db_connection()

            cursor = connection.cursor()


            # --------------------------------------
            # SAVE COMPLAINT
            # --------------------------------------

            sql = """
                INSERT INTO complaints
                (
                    complaint_id,
                    user_id,
                    subject,
                    description,
                    category,
                    confidence,
                    sentiment,
                    priority,
                    department,
                    status
                )

                VALUES
                (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
            """


            values = (

                complaint_id,

                session["user_id"],

                subject,

                description,

                category,

                confidence,

                sentiment,

                priority,

                department,

                status
            )


            cursor.execute(
                sql,
                values
            )


            connection.commit()


            # --------------------------------------
            # SUCCESS MESSAGE
            # --------------------------------------

            if relevance == "Irrelevant":

                flash(
                    (
                        f"Input submitted with ID "
                        f"{complaint_id}, but it was "
                        f"detected as Irrelevant / "
                        f"Out of Scope."
                    ),
                    "warning"
                )

            else:

                flash(
                    (
                        f"Complaint submitted successfully! "
                        f"ID: {complaint_id} | "
                        f"Category: {category}"
                    ),
                    "success"
                )


            return redirect(
                url_for("track_complaints")
            )


        # ------------------------------------------
        # ERROR
        # ------------------------------------------

        except Exception as e:

            if connection:

                connection.rollback()


            print(
                "COMPLAINT ERROR:",
                e
            )


            flash(
                (
                    "Complaint could not be "
                    "submitted. "
                    + str(e)
                ),
                "danger"
            )


            return redirect(
                url_for("submit_complaint")
            )


        # ------------------------------------------
        # CLOSE DATABASE
        # ------------------------------------------

        finally:

            if cursor:

                cursor.close()


            if connection:

                connection.close()


    # ----------------------------------------------
    # GET REQUEST
    # ----------------------------------------------

    return render_template(
        "submit_complaint.html",
        name=session.get("name")
    )
# ==================================================
# TRACK COMPLAINTS
# ==================================================

@app.route("/track-complaints")
def track_complaints():

    if "user_id" not in session:
        return redirect(url_for("login"))

    try:

        connection = get_db_connection()

        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT *
            FROM complaints
            WHERE user_id = %s
            ORDER BY created_at DESC
            """,
            (session["user_id"],)
        )

        complaints = cursor.fetchall()

        print("COMPLAINTS FOUND:", len(complaints))
        print(complaints)

        cursor.close()
        connection.close()

        return render_template(
            "track_complaint.html",
            complaints=complaints,
            name=session.get("name")
        )

    except Exception as e:

        print("TRACK COMPLAINT ERROR:", e)

        return f"""
        <h2>Track Complaint Error</h2>
        <p>{str(e)}</p>
        """

# ==================================================
# SEARCH COMPLAINT
# ==================================================

@app.route(
    "/track-complaint",
    methods=["POST"]
)
def track_single_complaint():

    if (
        "user_id" not in session
        or session.get("role") != "customer"
    ):

        return redirect(
            url_for("login")
        )


    complaint_id = request.form.get(
        "complaint_id", ""
    ).strip().upper()


    connection = get_db_connection()

    cursor = connection.cursor(
        dictionary=True
    )


    cursor.execute(
        """
        SELECT *
        FROM complaints

        WHERE complaint_id=%s
        AND user_id=%s
        """,

        (
            complaint_id,
            session["user_id"]
        )
    )


    complaint = cursor.fetchone()


    cursor.close()
    connection.close()


    if not complaint:

        flash(
            "Complaint not found.",
            "danger"
        )

        return redirect(
            url_for("track_complaints")
        )


    return render_template(
        "track_complaint.html",

        complaints=[complaint],

        name=session["name"]
    )


# ==================================================
# EMPLOYEE DASHBOARD
# ==================================================

@app.route("/employee/dashboard")
def employee_dashboard():

    if (
        "user_id" not in session
        or session.get("role") != "employee"
    ):

        return redirect(
            url_for("login")
        )


    connection = get_db_connection()

    cursor = connection.cursor(
        dictionary=True
    )


    cursor.execute(
        """
        SELECT
            complaints.*,
            users.name AS customer_name

        FROM complaints

        JOIN users
        ON complaints.user_id=users.id

        WHERE
            complaints.assigned_employee=%s

        ORDER BY
            complaints.created_at DESC
        """,

        (session["user_id"],)
    )


    complaints = cursor.fetchall()


    cursor.close()
    connection.close()


    return render_template(
        "employee_dashboard.html",

        name=session["name"],

        department=session.get(
            "department"
        ),

        complaints=complaints
    )


# ==================================================
# EMPLOYEE UPDATE
# ==================================================

@app.route(
    "/employee/update/<int:complaint_id>",
    methods=["POST"]
)
def employee_update(complaint_id):

    if session.get("role") != "employee":

        return redirect(
            url_for("login")
        )


    status = request.form.get("status")

    response = request.form.get(
        "employee_response", ""
    ).strip()


    allowed_status = [
        "Assigned",
        "In Progress",
        "Resolved"
    ]


    if status not in allowed_status:

        flash(
            "Invalid status.",
            "danger"
        )

        return redirect(
            url_for("employee_dashboard")
        )


    connection = get_db_connection()

    cursor = connection.cursor()


    # Employee can update only assigned complaint

    cursor.execute(
        """
        UPDATE complaints

        SET
            status=%s,
            employee_response=%s

        WHERE id=%s
        AND assigned_employee=%s
        """,

        (
            status,
            response,
            complaint_id,
            session["user_id"]
        )
    )


    connection.commit()

    cursor.close()
    connection.close()


    flash(
        "Complaint updated.",
        "success"
    )


    return redirect(
        url_for("employee_dashboard")
    )


# ==================================================
# ADMIN DASHBOARD
# ==================================================

@app.route("/admin-dashboard")
def admin_dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session.get("role") != "admin":
        flash("Admin access required.", "danger")
        return redirect(url_for("login"))

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # -------------------------------
    # ALL COMPLAINTS
    # -------------------------------

    cursor.execute("""
        SELECT
            c.*,
            u.name AS customer_name,
            u.email AS customer_email,
            e.name AS employee_name
        FROM complaints c
        JOIN users u
            ON c.user_id = u.id
        LEFT JOIN users e
            ON c.assigned_employee = e.id
        ORDER BY c.created_at DESC
    """)

    complaints = cursor.fetchall()


    # -------------------------------
    # EMPLOYEES
    # -------------------------------

    cursor.execute("""
        SELECT id, name, department
        FROM users
        WHERE role = 'employee'
        ORDER BY name
    """)

    employees = cursor.fetchall()


    # -------------------------------
    # DASHBOARD COUNTS
    # -------------------------------

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM complaints
    """)
    total = cursor.fetchone()["total"]


    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM complaints
        WHERE status = 'Pending'
    """)
    pending = cursor.fetchone()["total"]


    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM complaints
        WHERE status = 'In Progress'
    """)
    in_progress = cursor.fetchone()["total"]


    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM complaints
        WHERE status = 'Resolved'
    """)
    resolved = cursor.fetchone()["total"]


    # -------------------------------
    # CATEGORY CHART
    # -------------------------------

    cursor.execute("""
        SELECT
            COALESCE(category, 'Unclassified') AS label,
            COUNT(*) AS total
        FROM complaints
        GROUP BY category
    """)

    category_data = cursor.fetchall()


    # -------------------------------
    # STATUS CHART
    # -------------------------------

    cursor.execute("""
        SELECT
            status AS label,
            COUNT(*) AS total
        FROM complaints
        GROUP BY status
    """)

    status_data = cursor.fetchall()


    # -------------------------------
    # PRIORITY CHART
    # -------------------------------

    cursor.execute("""
        SELECT
            COALESCE(priority, 'Not Analysed') AS label,
            COUNT(*) AS total
        FROM complaints
        GROUP BY priority
    """)

    priority_data = cursor.fetchall()


    # -------------------------------
    # SENTIMENT CHART
    # -------------------------------

    cursor.execute("""
        SELECT
            COALESCE(sentiment, 'Not Analysed') AS label,
            COUNT(*) AS total
        FROM complaints
        GROUP BY sentiment
    """)

    sentiment_data = cursor.fetchall()


    # -------------------------------
    # DEPARTMENT CHART
    # -------------------------------

    cursor.execute("""
        SELECT
            COALESCE(department, 'Not Assigned') AS label,
            COUNT(*) AS total
        FROM complaints
        GROUP BY department
    """)

    department_data = cursor.fetchall()


    # -------------------------------
    # MONTHLY TREND
    # -------------------------------

    cursor.execute("""
        SELECT
            DATE_FORMAT(created_at, '%b %Y') AS label,
            DATE_FORMAT(created_at, '%Y-%m') AS sort_month,
            COUNT(*) AS total
        FROM complaints
        GROUP BY
            DATE_FORMAT(created_at, '%b %Y'),
            DATE_FORMAT(created_at, '%Y-%m')
        ORDER BY sort_month
    """)

    monthly_data = cursor.fetchall()


    cursor.close()
    connection.close()


    # -------------------------------
    # RESOLUTION RATE
    # -------------------------------

    resolution_rate = 0

    if total > 0:
        resolution_rate = round(
            (resolved / total) * 100,
            1
        )


    return render_template(
        "admin_dashboard.html",

        name=session.get("name"),

        complaints=complaints,
        employees=employees,

        total=total,
        pending=pending,
        in_progress=in_progress,
        resolved=resolved,

        resolution_rate=resolution_rate,

        category_data=category_data,
        status_data=status_data,
        priority_data=priority_data,
        sentiment_data=sentiment_data,
        department_data=department_data,
        monthly_data=monthly_data
    )

# ==================================================
# ADMIN ASSIGN COMPLAINT
# ==================================================

@app.route(
    "/admin/assign/<int:complaint_id>",
    methods=["POST"]
)
def assign_complaint(complaint_id):

    if session.get("role") != "admin":

        return redirect(
            url_for("login")
        )


    employee_id = request.form.get(
        "employee_id"
    )


    if not employee_id:

        flash(
            "Please select an employee.",
            "danger"
        )

        return redirect(
            url_for("admin_dashboard")
        )


    connection = get_db_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        UPDATE complaints

        SET
            assigned_employee=%s,
            status='Assigned'

        WHERE id=%s
        """,

        (
            employee_id,
            complaint_id
        )
    )


    connection.commit()

    cursor.close()
    connection.close()


    flash(
        "Complaint assigned successfully.",
        "success"
    )


    return redirect(
        url_for("admin_dashboard")
    )


# ==================================================
# ADMIN UPDATE
# ==================================================

@app.route(
    "/admin/update/<int:complaint_id>",
    methods=["POST"]
)
def admin_update(complaint_id):

    if session.get("role") != "admin":

        return redirect(
            url_for("login")
        )


    status = request.form.get("status")

    response = request.form.get(
        "admin_response", ""
    ).strip()


    allowed_status = [
        "Pending",
        "Assigned",
        "In Progress",
        "Resolved",
        "Rejected"
    ]


    if status not in allowed_status:

        flash(
            "Invalid status.",
            "danger"
        )

        return redirect(
            url_for("admin_dashboard")
        )


    connection = get_db_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        UPDATE complaints

        SET
            status=%s,
            admin_response=%s

        WHERE id=%s
        """,

        (
            status,
            response,
            complaint_id
        )
    )


    connection.commit()

    cursor.close()
    connection.close()


    flash(
        "Complaint updated successfully.",
        "success"
    )


    return redirect(
        url_for("admin_dashboard")
    )


# ==================================================
# LOGOUT
# ==================================================

@app.route("/logout")
def logout():

    session.clear()

    flash(
        "Logged out successfully.",
        "success"
    )

    return redirect(
        url_for("login")
    )


# ==================================================
# RUN
# ==================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )

    