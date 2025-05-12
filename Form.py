from flask import Flask, render_template, request, redirect
import pandas as pd
import os

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
EXCEL_FILE = r"C:\Users\Yz (work)\Desktop\SPMS Logs\Code for shirt form\Form.xlsx"

if not os.path.exists(EXCEL_FILE):
    df = pd.DataFrame(columns=["Name", "NTU Email", "Telegram Handle", "Shirt Orders", "PayNow", "Payment Method", "Payment Proof"])
    df.to_excel(EXCEL_FILE, index=False)

@app.route("/", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        telegram = request.form["telegram"]
        paynow = request.form["paynow"]
        payment_method = request.form.get("payment_method", "N/A")
        
        # Collect Shirt Orders
        shirts = []
        shirt_count = int(request.form["shirt_count"])
        for i in range(shirt_count):
            material = request.form.get(f"material_{i}")
            size = request.form.get(f"size_{i}")
            color = request.form.get(f"color_{i}")
            if material and size and color:
                shirts.append(f"{material} {size} {color}")
        
        # Handle file upload
        payment_proof = request.files["payment_proof"]
        payment_filename = ""
        if payment_proof:
            payment_filename = os.path.join(UPLOAD_FOLDER, payment_proof.filename)
            payment_proof.save(payment_filename)
        
        # Save to Excel
        df = pd.read_excel(EXCEL_FILE)
        new_data = pd.DataFrame({
            "Name": [name], "NTU Email": [email], "Telegram Handle": [telegram],
            "Shirt Orders": ["; ".join(shirts)], "PayNow": [paynow], "Payment Method": [payment_method],
            "Payment Proof": [payment_filename]
        })
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_excel(EXCEL_FILE, index=False)
        
        return redirect("/")
    
    return render_template("form.html")

if __name__ == "__main__":
    app.run(debug=True)