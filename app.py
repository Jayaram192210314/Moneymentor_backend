import os
import re
import json
import requests
import tempfile
from io import BytesIO
from flask import Flask, request, jsonify, session, send_file, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import cloudscraper
import mysql.connector
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
from mysql.connector import Error
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import numpy as np
import random
from flask_mail import Mail, Message
from apscheduler.schedulers.background import BackgroundScheduler

import matplotlib
matplotlib.use("Agg")
app = Flask(__name__) 
app.secret_key = "supersecretkey"  # required for session
# -----------------------------
# 1️⃣ Database Connection 
# -----------------------------
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",   # default XAMPP password is empty
            database="elearning_db"
        )

        if conn.is_connected():
            print("Database connected successfully")

        return conn

    except Error as e:
        print("Error while connecting to MySQL:", e)
        return None
# -----------------------------
# 1️⃣ Register 
# -----------------------------

@app.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    full_name = data.get("full_name")
    dob = data.get("dob")               
    mobile = data.get("mobile")         
    email = data.get("email")
    password = data.get("password")
    confirm_password = data.get("confirm_password")

    # -----------------------------
    # 1️⃣ Required Fields Validation
    # -----------------------------
    if not full_name or not dob or not mobile or not email or not password or not confirm_password:
        return jsonify({
            "status": "error",
            "message": "All fields are required"
        }), 400

    # -----------------------------
    # 2️⃣ Full Name Validation # Only letters and spaces allowed
    # -----------------------------
    if not re.match(r"^[A-Za-z\s]+$", full_name):
        return jsonify({
            "status": "error",
            "message": "Full name must contain only letters and spaces"
        }), 400
    # -----------------------------
    # 3️⃣ DOB Validation (YYYY-MM-DD)
    # -----------------------------
    try:
        datetime.strptime(dob, "%Y-%m-%d")
    except ValueError:
        return jsonify({
            "status": "error",
            "message": "DOB must be in YYYY-MM-DD format"
        }), 400
        # -----------------------------
    # 4️⃣ Mobile Number Validation (10 digits only)
    # -----------------------------
    if not re.match(r"^[0-9]{10}$", mobile):
        return jsonify({
            "status": "error",
            "message": "Mobile number must be exactly 10 digits"
        }), 400

    # -----------------------------
    # 5️⃣ Email Format Validation
    # -----------------------------
    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(email_pattern, email):
        return jsonify({
            "status": "error",
            "message": "Invalid email format"
        }), 400

    # -----------------------------
    # 6️⃣ Password Length Validation
    # -----------------------------
    password_pattern = r"^(?=.*[0-9])(?=.*[!@#$%^&*(),.?\":{}|<>]).{8,}$"

    if not re.match(password_pattern, password):
        return jsonify({
            "status": "error",
            "message": "Password must be at least 8 characters, include a number and a special character."
        }), 400

    # -----------------------------
    # 7️⃣ Password Match Validation
    # -----------------------------
    if password != confirm_password:
        return jsonify({
            "status": "error",
            "message": "Passwords do not match"
        }), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # -----------------------------
    # 8️⃣ Check if Email Already Exists
    # -----------------------------
    cursor.execute("SELECT * FROM register WHERE email = %s", (email,))
    existing_user = cursor.fetchone()

    if existing_user:
        cursor.close()
        conn.close()
        return jsonify({
            "status": "error",
            "message": "Email already registered"
        }), 409

    # -----------------------------
    # 9️⃣ Hash Password
    # -----------------------------
    hashed_password = generate_password_hash(password)

    # -----------------------------
    # 🔟 Insert User (UPDATED)
    # -----------------------------
    cursor.execute(
        """
        INSERT INTO register (full_name, dob, mobile, email, password)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (full_name, dob, mobile, email, hashed_password)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({
        "status": "success",
        "message": "User registered successfully"
    }), 201

# -----------------------------
# 1 login
# -----------------------------

@app.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    
    # 1️⃣ Required Fields Check
    
    if not email or not password:
        return jsonify({
            "status": "error",
            "message": "Email and password are required"
        }), 400

    # -----------------------------
    # 2️⃣ Email Format Validation
    # -----------------------------
    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(email_pattern, email):
        return jsonify({
            "status": "error",
            "message": "Invalid email format"
        }), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # -----------------------------
    # 3️⃣ Check if User Exists
    # -----------------------------
    cursor.execute("SELECT * FROM register WHERE email = %s", (email,))
    user = cursor.fetchone()

    if not user:
        cursor.close()
        conn.close()
        return jsonify({
            "status": "error",
            "message": "User not found"
        }), 404

    # -----------------------------
    # 4️⃣ Verify Password
    # -----------------------------
    if not check_password_hash(user["password"], password):
        cursor.close()
        conn.close()
        return jsonify({
            "status": "error",
            "message": "Invalid password"
        }), 401

    cursor.close()
    conn.close()

    return jsonify({
        "status": "success",
        "message": "Login successful",
        "user": {
            "id": user["id"],
            "full_name": user["full_name"],
            "email": user["email"]
        }
    }), 200


# -----------------------------
# 2️⃣ Mail Configuration (PUT HERE ✅)
# -----------------------------
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'sn3029769@gmail.com'
app.config['MAIL_PASSWORD'] = 'zfsysaebrurdzcdj'

mail = Mail(app)
# ----------------------------
# Forget password send otp
# ----------------------------
@app.route("/forgot-password", methods=["POST"])
def forgot_password():

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "status": "error",
            "message": "Invalid or missing JSON body"
        }), 400

    email = data.get("email")

    if not email:
        return jsonify({
            "status": "error",
            "message": "Email is required"
        }), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id FROM register WHERE email = %s", (email,))
    user = cursor.fetchone()

    if not user:
        cursor.close()
        conn.close()
        return jsonify({
            "status": "error",
            "message": "Email not registered"
        }), 404

    # Generate OTP
    otp = str(random.randint(1000, 9999))
    expiry_time = datetime.now() + timedelta(minutes=5)

    cursor.execute(
        "UPDATE register SET otp=%s, otp_expiry=%s WHERE id=%s",
        (otp, expiry_time, user["id"])
    )
    conn.commit()

    # ✅ Store email in session
    session["reset_email"] = email
    
    

    try:
        msg = Message(
            subject="Password Reset OTP",
            sender=app.config['MAIL_USERNAME'],
            recipients=[email]
        )
        msg.body = f"Your Reset Password OTP is: {otp}. It is valid for 5 minutes."

        mail.send(msg)

    except Exception as e:
        print("Mail Error:", e)
        return jsonify({
            "status": "error",
            "message": "Failed to send OTP"
        }), 500

    cursor.close()
    conn.close()

    return jsonify({
        "status": "success",
        "message": "OTP sent to registered email"
    }), 200

# ----------------------------
# verify-otp
# ----------------------------
@app.route("/verify-otp", methods=["POST"])
def verify_otp():

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"status": "error", "message": "Invalid JSON"}), 400

    otp = data.get("otp")

    if not otp:
        return jsonify({"status": "error", "message": "OTP required"}), 400

    # Get email from session
    email = session.get("reset_email")

    if not email:
        return jsonify({"status": "error", "message": "Session expired"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT otp, otp_expiry FROM register WHERE email=%s",
        (email,)
    )
    user = cursor.fetchone()

    if not user:
        cursor.close()
        conn.close()
        return jsonify({"status": "error", "message": "User not found"}), 404

    if user["otp"] != otp:
        cursor.close()
        conn.close()
        return jsonify({"status": "error", "message": "Invalid OTP"}), 400

    # 🔥 Fix datetime comparison properly
    expiry_time = user["otp_expiry"]

    if isinstance(expiry_time, str):
        expiry_time = datetime.strptime(expiry_time, "%Y-%m-%d %H:%M:%S.%f")

    if expiry_time < datetime.now():
        cursor.close()
        conn.close()
        return jsonify({
            "status": "error",
            "message": "OTP expired"
        }), 400

    cursor.close()
    conn.close()

    return jsonify({
        "status": "success",
        "message": "OTP verified. Ready to reset password."
    }), 200

from werkzeug.security import generate_password_hash

# ----------------------------
# Reset Password
# ----------------------------
@app.route("/reset-password", methods=["POST"])
def reset_password():

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "status": "error",
            "message": "Invalid JSON"
        }), 400

    new_password = data.get("new_password")
    confirm_password = data.get("confirm_password")

    if not new_password or not confirm_password:
        return jsonify({
            "status": "error",
            "message": "All fields are required"
        }), 400

    if new_password != confirm_password:
        return jsonify({
            "status": "error",
            "message": "Passwords do not match"
        }), 400

    if len(new_password) < 6:
        return jsonify({
            "status": "error",
            "message": "Password must be at least 6 characters"
        }), 400

    # ✅ Get email from session
    email = session.get("reset_email")

    if not email:
        return jsonify({
            "status": "error",
            "message": "Session expired"
        }), 400
    # Hash password before storing
    hashed_password = generate_password_hash(new_password)

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE register SET password=%s, otp=NULL, otp_expiry=NULL WHERE email=%s",
        (hashed_password, email)
    )

    conn.commit()
    cursor.close()
    conn.close()

    # Clear session after reset
    session.pop("reset_email", None)

    return jsonify({
        "status": "success",
        "message": "Password reset successfully"
    }), 200

# ----------------------------
# Daily Tip
# ----------------------------

@app.route("/daily-tip", methods=["GET"])
def daily_tip():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # 1️⃣ Get today's date
    today = datetime.now().date()

    # 2️⃣ Check if today's tip already exists
    cursor.execute("SELECT t.tip_text FROM tip_history h JOIN tips t ON h.tip_id = t.id WHERE h.shown_date = %s", (today,))
    today_tip = cursor.fetchone()

    if today_tip:
        cursor.close()
        conn.close()
        return jsonify({
            "status": "success",
            "daily_tip": today_tip["tip_text"]
        })

    # 3️⃣ Get tips NOT shown yet
    cursor.execute("""
        SELECT id, tip_text FROM tips 
        WHERE id NOT IN (SELECT tip_id FROM tip_history)
    """)
    remaining_tips = cursor.fetchall()

    # 4️⃣ If all tips used → reset history
    if not remaining_tips:
        cursor.execute("DELETE FROM tip_history")
        conn.commit()

        cursor.execute("SELECT id, tip_text FROM tips")
        remaining_tips = cursor.fetchall()

    # 5️⃣ Pick a random tip
    import random
    selected_tip = random.choice(remaining_tips)

    # 6️⃣ Save to history
    cursor.execute("INSERT INTO tip_history (tip_id, shown_date) VALUES (%s, %s)",
                   (selected_tip["id"], today))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        "status": "success",
        "daily_tip": selected_tip["tip_text"]
    }),200

# ----------------------------
# Daily Terms
# ----------------------------

@app.route("/daily-term", methods=["GET"])
def daily_term():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    today = datetime.now().date()

    # 1️⃣ Check if today's term already exists
    cursor.execute("""
        SELECT t.term_text 
        FROM term_history h 
        JOIN terms t ON h.term_id = t.id 
        WHERE h.shown_date = %s
    """, (today,))
    today_term = cursor.fetchone()

    if today_term:
        cursor.close()
        conn.close()
        return jsonify({
            "status": "success",
            "daily_term": today_term["term_text"]
        })

    # 2️⃣ Get terms NOT shown yet
    cursor.execute("""
        SELECT id, term_text FROM terms 
        WHERE id NOT IN (SELECT term_id FROM term_history)
    """)
    remaining_terms = cursor.fetchall()

    # 3️⃣ If all terms used → reset history
    if not remaining_terms:
        cursor.execute("DELETE FROM term_history")
        conn.commit()

        cursor.execute("SELECT id, term_text FROM terms")
        remaining_terms = cursor.fetchall()

    # 4️⃣ Pick a random term
    import random
    selected_term = random.choice(remaining_terms)

    # 5️⃣ Insert today's term into history
    cursor.execute(
        "INSERT INTO term_history (term_id, shown_date) VALUES (%s, %s)",
        (selected_term["id"], today)
    )
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        "status": "success",
        "daily_term": selected_term["term_text"]
    }),200


# ----------------------------
# Add Goals (Updated with user_id)
# ----------------------------
@app.route("/add-goal", methods=["POST"])
def add_goal():
    import re
    from datetime import datetime

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"status": "error", "message": "Invalid JSON"}), 400

    user_id = data.get("user_id")             # NEW
    goal_name = data.get("goal_name")
    target_amount = data.get("target_amount")
    already_saved_amount = data.get("already_saved_amount")
    deadline = data.get("deadline")

    # 1️⃣ Required Fields
    if not user_id or not goal_name or not target_amount or not already_saved_amount or not deadline:
        return jsonify({
            "status": "error",
            "message": "user_id, goal_name, target_amount, already_saved_amount, and deadline are required"
        }), 400

    # 2️⃣ goal_name validation
    if not re.match(r"^[A-Za-z\s]+$", goal_name):
        return jsonify({
            "status": "error",
            "message": "Goal name must contain only letters and spaces"
        }), 400

    # 3️⃣ target_amount validation
    if not str(target_amount).replace('.', '', 1).isdigit():
        return jsonify({
            "status": "error",
            "message": "Target amount must be a valid number"
        }), 400

    # 4️⃣ already_saved_amount validation
    if not str(already_saved_amount).replace('.', '', 1).isdigit():
        return jsonify({
            "status": "error",
            "message": "Already saved amount must be a valid number"
        }), 400

    # 5️⃣ deadline validation
    try:
        datetime.strptime(deadline, "%Y-%m-%d")
    except ValueError:
        return jsonify({
            "status": "error",
            "message": "Deadline must be in YYYY-MM-DD format"
        }), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO goals (user_id, goal_name, target_amount, already_saved_amount, deadline)
            VALUES (%s, %s, %s, %s, %s)
        """, (user_id, goal_name, target_amount, already_saved_amount, deadline))

        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({
            "status": "success",
            "message": "Goal added successfully"
        }), 201

    except Exception as e:
        cursor.close()
        conn.close()
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# ----------------------------
# Fetch all the goals data
# ----------------------------

@app.route("/get-goals", methods=["GET"])
def get_goals():
    user_id = request.args.get("user_id")   # 👈 login person's id

    if not user_id:
        return jsonify({
            "status": "error",
            "message": "user_id is required"
        }), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT id, goal_name, target_amount, already_saved_amount, deadline 
            FROM goals
            WHERE user_id = %s
        """, (user_id,))

        goals = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify({
            "status": "success",
            "goals": goals
        }), 200

    except Exception as e:
        cursor.close()
        conn.close()
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# ----------------------------
# Get Goal by ID
# ----------------------------
@app.route("/get-goal/<int:goal_id>", methods=["GET"])
def get_goal_by_id(goal_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT goal_name, target_amount, already_saved_amount, deadline FROM goals WHERE id = %s", (goal_id,))
        goal = cursor.fetchone()

        cursor.close()
        conn.close()

        if not goal:
            return jsonify({
                "status": "error",
                "message": "Goal not found"
            }), 404

        return jsonify({
            "status": "success",
            "goal": goal
        }), 200

    except Exception as e:
        cursor.close()
        conn.close()

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# ----------------------------
# Update Goal by ID
# ----------------------------
@app.route("/update-goal/<int:goal_id>", methods=["PUT"])
def update_goal(goal_id):
    import re
    from datetime import datetime

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"status": "error", "message": "Invalid JSON"}), 400

    goal_name = data.get("goal_name")
    target_amount = data.get("target_amount")
    already_saved_amount = data.get("already_saved_amount")
    deadline = data.get("deadline")

    # ---------------------------
    # VALIDATIONS
    # ---------------------------

    if goal_name and not re.match(r"^[A-Za-z\s]+$", goal_name):
        return jsonify({"status": "error", "message": "Goal name must contain only letters & spaces"}), 400

    if target_amount and not str(target_amount).replace('.', '', 1).isdigit():
        return jsonify({"status": "error", "message": "Target amount must be a valid number"}), 400

    if already_saved_amount and not str(already_saved_amount).replace('.', '', 1).isdigit():
        return jsonify({"status": "error", "message": "Already saved amount must be a valid number"}), 400

    if deadline:
        try:
            datetime.strptime(deadline, "%Y-%m-%d")
        except ValueError:
            return jsonify({"status": "error", "message": "Deadline must be YYYY-MM-DD format"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Check if goal exists by id only
    cursor.execute("SELECT id FROM goals WHERE id = %s", (goal_id,))
    exists = cursor.fetchone()

    if not exists:
        return jsonify({"status": "error", "message": "Goal ID not found"}), 404

    # ---------------------------
    # Build Dynamic Update Query
    # ---------------------------
    update_fields = []
    update_values = []

    if goal_name:
        update_fields.append("goal_name = %s")
        update_values.append(goal_name)

    if target_amount:
        update_fields.append("target_amount = %s")
        update_values.append(target_amount)

    if already_saved_amount:
        update_fields.append("already_saved_amount = %s")
        update_values.append(already_saved_amount)

    if deadline:
        update_fields.append("deadline = %s")
        update_values.append(deadline)

    if not update_fields:
        return jsonify({"status": "error", "message": "No fields to update"}), 400

    update_values.append(goal_id)

    query = f"UPDATE goals SET {', '.join(update_fields)} WHERE id = %s"
    cursor.execute(query, tuple(update_values))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        "status": "success",
        "message": "Goal updated successfully"
    }), 200


# ----------------------------
# Delete Goal by ID 
# ----------------------------
@app.route("/delete-goal/<int:goal_id>", methods=["DELETE"])
def delete_goal(goal_id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Check if goal exists
    cursor.execute("SELECT id FROM goals WHERE id = %s", (goal_id,))
    exists = cursor.fetchone()

    if not exists:
        cursor.close()
        conn.close()
        return jsonify({"status": "error", "message": "Goal not found"}), 404

    # Delete goal
    cursor.execute("DELETE FROM goals WHERE id = %s", (goal_id,))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        "status": "success",
        "message": "Goal deleted successfully"
    }), 200


# ----------------------------
# Update extra_amount + auto add to saved
# ----------------------------
@app.route("/update-extra/<int:goal_id>", methods=["PUT"])
def update_extra_amount(goal_id):
    import re

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"status": "error", "message": "Invalid JSON"}), 400

    extra_amount = data.get("extra_amount")

    # Validate number
    if extra_amount is None or not str(extra_amount).replace('.', '', 1).isdigit():
        return jsonify({
            "status": "error",
            "message": "extra_amount must be a valid number"
        }), 400

    extra_amount = float(extra_amount)

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Fetch target & saved from correct table: goals
        cursor.execute(
            "SELECT target_amount, already_saved_amount FROM goals WHERE id = %s",
            (goal_id,)
        )
        goal = cursor.fetchone()

        if not goal:
            cursor.close()
            conn.close()
            return jsonify({"status": "error", "message": "Goal not found"}), 404

        target_amount = float(goal["target_amount"])
        current_saved = float(goal["already_saved_amount"])

        updated_saved = current_saved + extra_amount

        # Limit check
        if updated_saved > target_amount:
            cursor.close()
            conn.close()
            return jsonify({
                "status": "error",
                "message": "Extra amount exceeds target amount."
            }), 400

        # Update in goals table
        cursor.execute("""
            UPDATE goals
            SET extra_amount = %s,
                already_saved_amount = %s
            WHERE id = %s
        """, (extra_amount, updated_saved, goal_id))

        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({
            "status": "success",
            "message": "Extra amount updated successfully",
            "updated_saved_amount": updated_saved
        }), 200

    except Exception as e:
        cursor.close()
        conn.close()
        return jsonify({"status": "error", "message": str(e)}), 500



# ----------------------------
# Withdraw amount (reduce saved amount)
# ----------------------------
@app.route("/withdraw/<int:goal_id>", methods=["PUT"])
def withdraw_amount(goal_id):
    import re

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"status": "error", "message": "Invalid JSON"}), 400

    withdraw_amount = data.get("withdraw_amount")

    # Validate number
    if withdraw_amount is None or not str(withdraw_amount).replace('.', '', 1).isdigit():
        return jsonify({
            "status": "error",
            "message": "withdraw_amount must be a valid number"
        }), 400

    withdraw_amount = float(withdraw_amount)

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Fetch saved amount from correct table: goals
        cursor.execute(
            "SELECT already_saved_amount FROM goals WHERE id = %s",
            (goal_id,)
        )
        goal = cursor.fetchone()

        if not goal:
            cursor.close()
            conn.close()
            return jsonify({"status": "error", "message": "Goal not found"}), 404

        current_saved = float(goal["already_saved_amount"])

        # Checks
        if current_saved <= 0:
            cursor.close()
            conn.close()
            return jsonify({
                "status": "error",
                "message": "No saving amount available"
            }), 400

        if withdraw_amount > current_saved:
            cursor.close()
            conn.close()
            return jsonify({
                "status": "error",
                "message": "Withdraw amount cannot exceed saved amount"
            }), 400

        updated_saved = current_saved - withdraw_amount

        # Update in goals table
        cursor.execute("""
            UPDATE goals 
            SET withdraw_amount = %s,
                already_saved_amount = %s
            WHERE id = %s
        """, (withdraw_amount, updated_saved, goal_id))

        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({
            "status": "success",
            "message": "Withdraw successful",
            "remaining_saved_amount": updated_saved
        }), 200

    except Exception as e:
        cursor.close()
        conn.close()
        return jsonify({"status": "error", "message": str(e)}), 500
# ----------------------------
# Get Profile by User ID
# ----------------------------
@app.route("/get-profile/<int:user_id>", methods=["GET"])
def get_profile(user_id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT full_name, email, mobile, dob FROM register WHERE id = %s",
        (user_id,)
    )
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if not user:
        return jsonify({
            "status": "error",
            "message": "User not found"
        }), 404

    return jsonify({
        "status": "success",
        "data": user
    }), 200
# ----------------------------
# Profile editing function
# ----------------------------
@app.route("/update-profile/<int:user_id>", methods=["PUT"])
def update_profile(user_id):

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"status": "error", "message": "Invalid JSON"}), 400

    full_name = data.get("full_name")
    email = data.get("email")
    mobile = data.get("mobile")
    dob = data.get("dob")

    # ----------------------------
    # 1️⃣ Validate Full Name (optional update)
    # ----------------------------
    if full_name and not re.match(r"^[A-Za-z\s]+$", full_name):
        return jsonify({
            "status": "error",
            "message": "Full name must contain only letters and spaces"
        }), 400

    # ----------------------------
    # 2️⃣ Validate Email (optional update)
    # ----------------------------
    if email:
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_pattern, email):
            return jsonify({
                "status": "error",
                "message": "Invalid email format"
            }), 400

    # ----------------------------
    # 3️⃣ Validate Mobile Number (optional update)
    # ----------------------------
    if mobile:
        if not re.match(r"^[0-9]{10}$", mobile):
            return jsonify({
                "status": "error",
                "message": "Mobile number must be exactly 10 digits"
            }), 400

    # ----------------------------
    # 4️⃣ Validate DOB (optional update)
    # ----------------------------
    if dob:
        try:
            datetime.strptime(dob, "%Y-%m-%d")
        except ValueError:
            return jsonify({
                "status": "error",
                "message": "DOB must be in YYYY-MM-DD format"
            }), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Check if user exists
    cursor.execute("SELECT * FROM register WHERE id = %s", (user_id,))
    existing_user = cursor.fetchone()

    if not existing_user:
        cursor.close()
        conn.close()
        return jsonify({"status": "error", "message": "User not found"}), 404

    # Check duplicate email (if updating)
    if email:
        cursor.execute(
            "SELECT id FROM register WHERE email = %s AND id != %s",
            (email, user_id)
        )
        email_exists = cursor.fetchone()
        if email_exists:
            cursor.close()
            conn.close()
            return jsonify({
                "status": "error",
                "message": "Email is already in use by another account"
            }), 409

    # Build dynamic query
    update_fields = []
    update_values = []

    if full_name:
        update_fields.append("full_name = %s")
        update_values.append(full_name)

    if email:
        update_fields.append("email = %s")
        update_values.append(email)

    if mobile:
        update_fields.append("mobile = %s")
        update_values.append(mobile)

    if dob:
        update_fields.append("dob = %s")
        update_values.append(dob)

    if not update_fields:
        return jsonify({"status": "error", "message": "No valid fields to update"}), 400

    update_values.append(user_id)

    query = f"UPDATE register SET {', '.join(update_fields)} WHERE id = %s"

    cursor.execute(query, tuple(update_values))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        "status": "success",
        "message": "Profile updated successfully"
    }), 200
# --------------------------------------------------
# GOLD SCRAPER
# --------------------------------------------------
def get_gold_price(place="chennai"):

    place = place.lower().strip()
    url_gold = f"https://www.goodreturns.in/gold-rates/{place}.html"

    scraper = cloudscraper.create_scraper()

    try:
        gold_response = scraper.get(url_gold)
        if gold_response.status_code != 200:
            return None, f"Failed with status {gold_response.status_code}"

        soup_gold = BeautifulSoup(gold_response.text, "html.parser")

        # 24K Price Today
        price_24k_element = soup_gold.find("span", id="24K-price")
        if not price_24k_element:
            return None, "24K price not found"

        price_24k = price_24k_element.text.strip().replace("₹", "").replace(",", "")

        # Extract last 10 days table
        last10_json = []
        tables = soup_gold.find_all("table")

        target_table = None
        for tbl in tables:
            headers = [th.get_text(strip=True).lower() for th in tbl.find_all("th")]
            if any("24" in h for h in headers) and any("22" in h for h in headers):
                target_table = tbl
                break

        if not target_table:
            return {"24K": price_24k, "table": []}, None

        rows = target_table.find("tbody").find_all("tr")

        for row in rows:
            cols = row.find_all("td")
            if len(cols) < 3:
                continue

            date = cols[0].get_text(strip=True)

            # 24K
            col_24k_raw = cols[1].get_text(" ", strip=True).replace("₹", "").replace(",", "")
            p24 = col_24k_raw.split()
            price_24k_day = p24[0]
            change_24k_day = p24[1].strip("()") if len(p24) > 1 else "0"

            # 22K
            col_22k_raw = cols[2].get_text(" ", strip=True).replace("₹", "").replace(",", "")
            p22 = col_22k_raw.split()
            price_22k_day = p22[0]
            change_22k_day = p22[1].strip("()") if len(p22) > 1 else "0"

            last10_json.append({
                "date": date,
                "24k": price_24k_day,
                "24k_change": change_24k_day,
                "22k": price_22k_day,
                "22k_change": change_22k_day
            })

        return {
            "24K": price_24k,
            "table": last10_json
        }, None

    except Exception as e:
        return None, str(e)
# --------------------------------------------------
# GOLD API
# --------------------------------------------------
@app.route("/gold", methods=["GET"])
def gold_rate():

    place = request.args.get("place", "chennai")
    prices, error = get_gold_price(place)

    if error:
        return jsonify({"status": "error", "message": error}), 400

    table = prices["table"]
    today = table[0] if len(table) > 0 else {}

    return jsonify({
        "status": "success",
        "place": place,
        "gold_price_24k_per_gram": prices["24K"],
        "gold_price_22k_per_gram": today.get("22k", "NA"),
        "change_24k_today": today.get("24k_change", "0"),
        "change_22k_today": today.get("22k_change", "0"),
        "currency": "INR",
        "table": prices["table"],
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

# --------------------------------------------------
# Silver Scrapper
# --------------------------------------------------
def fetch_silver_data(place="chennai"):
    place = place.lower().strip()
    url = f"https://www.goodreturns.in/silver-rates/{place}.html"

    scraper = cloudscraper.create_scraper()

    try:
        response = scraper.get(url, timeout=10)

        if response.status_code != 200:
            return None, f"HTTP {response.status_code}"

        soup = BeautifulSoup(response.text, "html.parser")

        # ---------------------------------------------------------
        # 1) Extract today's silver price (1 gram)
        # ---------------------------------------------------------
        silver_element = soup.find("span", id="silver-1g-price")
        if not silver_element:
            silver_today = "0"
        else:
            silver_today = (
                silver_element.text.strip()
                .replace("₹", "")
                .replace(",", "")
            )

        # ---------------------------------------------------------
        # 2) Extract last 10-day table + today_change
        # ---------------------------------------------------------
        tables = soup.find_all("table")
        target_table = None

        for tbl in tables:
            headers = [th.get_text(strip=True).lower() for th in tbl.find_all("th")]
            if any("10 gram" in h for h in headers):
                target_table = tbl
                break

        last10 = []
        today_change = "0"

        if target_table:
            tbody = target_table.find("tbody")
            if tbody:
                rows = tbody.find_all("tr")

                for idx, r in enumerate(rows):
                    cols = r.find_all("td")
                    if len(cols) < 4:
                        continue

                    date = cols[0].get_text(strip=True)

                    # 10g → convert to 1g
                    price_10g = (
                        cols[1].get_text(strip=True)
                        .replace("₹", "")
                        .replace(",", "")
                    )

                    # 1KG column contains change
                    kg_raw = cols[3].get_text(" ", strip=True)
                    kg_clean = kg_raw.replace("₹", "").replace(",", "")
                    kg_split = kg_clean.split()

                    change = "0"
                    if len(kg_split) > 1:
                        change = kg_split[1].strip("()")

                    if idx == 0:
                        today_change = change

                    last10.append({
                        "date": date,
                        "rate": float(price_10g) / 10,
                        "change": float(change) / 1000 if change != "0" else 0
                    })

        return {
            "silver_today": silver_today,
            "today_change": float(today_change) / 1000 if change != "0" else 0,
            "table": last10
        }, None

    except Exception as e:
        return None, str(e)
# --------------------------------------------------
# SILVER API
# --------------------------------------------------
@app.route("/silver", methods=["GET"])
def silver_rate():
    place = request.args.get("place", "chennai")

    data, err = fetch_silver_data(place)

    if err:
        return jsonify({"status": "error", "message": err}), 400

    return jsonify({
        "status": "success",
        "place": place,
        "silver_today": data["silver_today"],
        "today_change": data["today_change"],
        "table": data["table"],
        "currency": "INR",
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
# --------------------------------------------------
# LEARNING PROGRESS UPDATE
# --------------------------------------------------
@app.route('/progress/update', methods=['POST'])
def update_progress():
    data = request.json
    user_id = data['user_id']
    article_no = data['article_no']  # frontend sends static article number

    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        INSERT INTO user_article_progress (user_id, article_no, is_completed, completed_at)
        VALUES (%s, %s, 1, NOW())
        ON DUPLICATE KEY UPDATE is_completed=1, completed_at=NOW();
    """

    cursor.execute(query, (user_id, article_no))
    conn.commit()

    return jsonify({"status": "success"})


@app.route('/progress/<int:user_id>', methods=['GET'])
def get_progress(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Fetch the actual article numbers that are completed
    cursor.execute("""
        SELECT article_no FROM user_article_progress
        WHERE user_id=%s AND is_completed=1
    """, (user_id,))
    
    # 2. Extract into a simple list [1, 2, 5, ...]
    rows = cursor.fetchall()
    completed_articles = [row[0] for row in rows]

    # 3. Calculate stats
    completed_count = len(completed_articles)
    total_articles = 84 
    
    # Avoid division by zero just in case
    progress = (completed_count / total_articles * 100) if total_articles > 0 else 0

    return jsonify({
        "completed": completed_count,
        "total": total_articles,
        "progress_percent": round(progress, 2),
        "completed_articles": completed_articles
    })
def insert_notification(user_id, title, message, notif_type):
    """Internal helper to insert a notification into the database."""
    from datetime import datetime
    conn = get_db_connection()
    if not conn:
        return
    cursor = conn.cursor()
    try:
        display_time = datetime.now().strftime("%I:%M %p")
        cursor.execute("""
            INSERT INTO notifications (user_id, title, message, time_value, type, is_unread, created_at)
            VALUES (%s, %s, %s, %s, %s, 1, NOW())
        """, (user_id, title, message, display_time, notif_type))
        conn.commit()
    except Exception as e:
        print(f"Error inserting notification: {e}")
    finally:
        cursor.close()
        conn.close()

# --------------------------------------------------
# Notifications 
# --------------------------------------------------
@app.route("/enable-daily", methods=["POST"])
def enable_daily():
    data = request.json
    user_id = data.get("user_id")
    time_value = data.get("time")

    if not user_id or not time_value:
        return jsonify({"status": "error", "message": "user_id & time required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO user_notifications (user_id, type, time_value, status)
            VALUES (%s, 'daily', %s, 1)
            ON DUPLICATE KEY UPDATE time_value=%s, status=1
        """, (user_id, time_value, time_value))
        conn.commit()
        return jsonify({"status": "success", "message": "Daily reminder enabled"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route("/enable-monthly-flexible", methods=["POST"])
def enable_monthly_flexible():
    data = request.json
    user_id = data.get("user_id")
    day = data.get("day")
    time_value = data.get("time")

    if not user_id or day is None or not time_value:
        return jsonify({"status": "error", "message": "user_id, day & time required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO user_notifications (user_id, type, day_value, time_value, status)
            VALUES (%s, 'monthly', %s, %s, 1)
            ON DUPLICATE KEY UPDATE day_value=%s, time_value=%s, status=1
        """, (user_id, day, time_value, day, time_value))
        conn.commit()
        return jsonify({"status": "success", "message": "Monthly reminder enabled"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route("/disable-notification", methods=["POST"])
def disable_notification():
    data = request.json
    user_id = data.get("user_id")
    notif_type = data.get("type")

    if not user_id or not notif_type:
        return jsonify({"status": "error", "message": "user_id & type required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE user_notifications SET status = 0 
            WHERE user_id = %s AND type = %s
        """, (user_id, notif_type))
        conn.commit()
        return jsonify({"status": "success", "message": f"{notif_type} reminder disabled"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route("/get-notifications", methods=["GET"])
def get_notifications():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"status": "error", "message": "user_id is required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT id, title, message, time_value as time, type, is_unread 
            FROM notifications WHERE user_id = %s ORDER BY created_at DESC
        """, (user_id,))
        notifications = cursor.fetchall()
        for n in notifications:
            n['is_unread'] = bool(n['is_unread'])
        return jsonify({"status": "success", "notifications": notifications})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route("/delete-notification/<int:notification_id>", methods=["DELETE"])
def delete_notification(notification_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM notifications WHERE id = %s", (notification_id,))
        conn.commit()
        return jsonify({"status": "success", "message": "Notification deleted"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

def process_notifications():
    from datetime import datetime
    now = datetime.now()
    # Current time in "09:00 AM" or "9:00 AM" format. 
    # Python's %I adds a leading zero (09:00 AM). 
    # We strip it to match database format (9:00 AM).
    current_time = now.strftime("%I:%M %p").lstrip("0")
    current_day = now.day
    
    print(f"--- Scheduler Running at {current_time} (System: {now.strftime('%I:%M %p')}, Day {current_day}) ---")
    
    conn = get_db_connection()
    if not conn: return
    cursor = conn.cursor(dictionary=True)
    try:
        # Daily
        cursor.execute("SELECT user_id FROM user_notifications WHERE type = 'daily' AND time_value = %s AND status = 1", (current_time,))
        daily_users = cursor.fetchall()
        print(f"Found {len(daily_users)} daily reminders to send")
        for row in daily_users:
            insert_notification(row['user_id'], "Daily Tip", "Check out your daily financial tip!", "daily")
            
        # Monthly
        cursor.execute("SELECT user_id FROM user_notifications WHERE type = 'monthly' AND day_value = %s AND time_value = %s AND status = 1", (current_day, current_time))
        monthly_users = cursor.fetchall()
        print(f"Found {len(monthly_users)} monthly reminders to send")
        for row in monthly_users:
            insert_notification(row['user_id'], "Monthly Goal", "It's time to update your savings goal!", "monthly")
    except Exception as e:
        print(f"Scheduler Error: {e}")
    finally:
        cursor.close()
        conn.close()

@app.route("/debug-notifications", methods=["GET"])
def debug_notifications():
    from datetime import datetime # Import datetime here as well for this function
    conn = get_db_connection()
    if not conn: return jsonify({"error": "DB connection failed"}), 500
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM user_notifications")
        user_notifs = cursor.fetchall()
        cursor.execute("SELECT * FROM notifications ORDER BY created_at DESC LIMIT 20")
        recent_notifs = cursor.fetchall()
        return jsonify({
            "user_settings": user_notifs,
            "recent_actual_notifications": recent_notifs,
            "server_current_time_debug": datetime.now().strftime("%I:%M %p")
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route("/trigger-scheduler", methods=["GET"])
def trigger_scheduler():
    process_notifications()
    return jsonify({"status": "success", "message": "Scheduler triggered manually"})

scheduler = BackgroundScheduler()
scheduler.add_job(process_notifications, 'interval', minutes=1)
scheduler.start()


@app.route("/test-notification", methods=["POST"])
def test_notification():
    data = request.json
    user_id = data.get("user_id")
    if not user_id:
        return jsonify({"status": "error", "message": "user_id required"}), 400
    
    insert_notification(user_id, "Test Alert", "This is a test notification from the server!", "test")
    return jsonify({"status": "success", "message": "Test notification created"})



# --------------------------------------------------
# RUN SERVER
# --------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)