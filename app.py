from flask import Flask, render_template, request
import pandas as pd
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    df = pd.read_csv(file)

    summary = []
    for emp_id in df['EmpID'].unique():
        emp_data = df[df['EmpID'] == emp_id].sort_values(by='CheckIn-CheckOut Time')
        name = emp_data.iloc[0]['Name']
        first_in = emp_data[emp_data['Attendance'].str.upper() == 'IN'].iloc[0]['CheckIn-CheckOut Time']
        last_out = emp_data[emp_data['Attendance'].str.upper() == 'OUT'].iloc[-1]['CheckIn-CheckOut Time']

        total_out = emp_data[emp_data['Attendance'].str.upper() == 'OUT'].shape[0]
        total_minutes = 0

        time_format = "%d-%m-%Y %H:%M"
        logs = emp_data.values.tolist()

        for i in range(0, len(logs) - 1, 2):
            if logs[i][3].upper() == 'IN' and logs[i+1][3].upper() == 'OUT':
                in_time = datetime.strptime(logs[i][2], time_format)
                out_time = datetime.strptime(logs[i+1][2], time_format)
                total_minutes += int((out_time - in_time).total_seconds() / 60)

        hours = total_minutes // 60
        minutes = total_minutes % 60
        work_duration = f"{hours:02}:{minutes:02}"

        summary.append({
            "EmpID": emp_id,
            "Name": name,
            "FirstCheckIn": first_in,
            "LastCheckOut": last_out,
            "OutCount": total_out,
            "TotalWorkHours": work_duration
        })

    return render_template('result.html', data=summary)

if __name__ == "__main__":
    app.run()
