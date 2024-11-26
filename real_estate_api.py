from flask import Flask, jsonify, request
import json
import pandas as pd


app = Flask(__name__)

@app.route("/get_data", methods=["GET"])
def get_data():
    try:
        # Διαβάζουμε το αρχείο csv που έχει τα δεδομένα για τα ακίνητα στη Μανδρίτη.
        estateData = pd.read_csv("./houses_Madrid.csv")

        # Μετατρεπούμε τα δεδομένα αρχικά σε λεξικό και έπειτα σε json.
        estateDataJson = estateData.to_dict(orient="records")
        
        # Επιστρέφουμε τα δεδομένα σε json με κωδικό 200(OK status).
        return jsonify(estateDataJson), 200
    except Exception as e:
        # Εμφανίζουμε κατάλληλο μήνυμα αν προέκυψε σφάλμα.
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Τρέχουμε το API στο port 5000.
    app.run(port = 5000, debug = True)