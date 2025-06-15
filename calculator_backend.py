from flask import Flask, request, render_template
from datetime import datetime

app = Flask(__name__)

def format_currency(value):
    return "{:,}".format(round(value, 3))

def calculate_simple_interest(principal, rate, time):
    return (principal * rate * time) / 100

def calculate_compound_interest(principal, rate, time):
    return principal * ((1 + rate / 100) ** time) - principal

def format_duration(days):
    if days <= 0:
        return "0 Years 0 Months 0 Days"

    years = days // 365
    months = (days % 365) // 30
    remaining_days = (days % 365) % 30
    return f"{years} Year{'s' if years > 1 else ''} {months} Month{'s' if months > 1 else ''} {remaining_days} Day{'s' if remaining_days > 1 else ''}"

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        interest_type = request.form['interest_type']  # Get interest type
        principal = float(request.form['amount'].replace(',', ''))
        rate = float(request.form['interest_rate'].replace(',', ''))

        duration_type = request.form['duration_type']
        
        if duration_type == 'time_period':
            time = float(request.form.get('time_period', 0))  # Get time in years
            duration_text = f"{int(time)} Years"

        else:
            start_date = request.form.get('start_date', '')
            end_date = request.form.get('end_date', '')

            if not start_date or not end_date:
                return "Error: Start Date and End Date are required!"

            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")

            if start_date > end_date:
                return "Error: Start Date cannot be later than End Date!"

            days = (end_date - start_date).days
            duration_text = format_duration(days)
            time = days / 365  # Convert days to years

        # Calculate interest based on type
        if interest_type == "simple":
            interest_amount = calculate_simple_interest(principal, rate, time)
        else:
            interest_amount = calculate_compound_interest(principal, rate, time)

        total_amount = principal + interest_amount

        return render_template('result.html', 
                               principal=format_currency(principal), 
                               rate=f"{rate}% per year", 
                               time=duration_text, 
                               interest_type=interest_type.capitalize(),
                               interest_amount=format_currency(interest_amount), 
                               total_amount=format_currency(total_amount))
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
