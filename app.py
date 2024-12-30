from flask import Flask, render_template, request, redirect, url_for
import pywhatkit as kit
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        #getting data from the form
        phone_number = request.form['phone_number']
        message = request.form['message']
        send_time = request.form['send_time']
        hour = send_time[0]+send_time[1]
        min = send_time[3]+send_time[4]
        
        min_int = int(min)
        hour_int = int(hour)
        
        
        # If the user does not add the country code, this adds South Africa's contry code 
        if len(phone_number) == 9 and phone_number[0] != '0':
            phone_number = f'+27{phone_number}'
        elif len(phone_number) == 9 and phone_number[0] == '0':
            return render_template('index.html', error='The number you entered does not exist')
            
        
        
        # If the user enters 0 infront of the number and not the country code
        if phone_number[0] == '0' and len(phone_number) == 10:
            for i in range(len(phone_number)-1):
                cut_number = phone_number[i+1]
            phone_number = f'+27{cut_number}'

        
        try:
            # Schedule the message
            kit.sendwhatmsg(phone_number, message, hour_int, min_int)
            print(f"Message scheduled for {phone_number} at {send_time.strftime('%H:%M')}")
        except Exception as e:
            print(f"An error occurred: {e}")
            return render_template('index.html', error=e)
        
        return render_template('index.html', message='Message scheduled successfully')

    
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
