Movie Booking System (MBS)
The Movie Booking System (MBS) is a user-friendly, web-based platform that lets customers browse and book tickets for movies currently playing. With a simple interface for users and a powerful admin panel, MBS makes movie selection and ticket booking a breeze.

Features

🎬 Browse Movies: Discover movies by genre, language, or availability.

🗓️ View Showtimes: Easily access up-to-date movie schedules.

💳 Secure Online Booking: Book tickets and make payments securely.

🎟️ Ticket Confirmation: Receive email confirmations with your ticket details.

🛠️ Admin Dashboard: Manage movie listings, schedules, and bookings efficiently.

📊 Reporting Tools: Analyze sales and occupancy data.

Running the Backend
Prerequisites
Python 3.x installed

Postman (for testing APIs)

Setup Instructions
Clone the repository:
git clone https://github.com/joMusangu/mbs.git
Navigate to the backend folder:

Open your terminal or VSCode terminal, then run:
cd mbs_backend
Run the server:

Start the server by running:
python3 manage.py runserver
This will start the server, and you can access it locally at http://127.0.0.1:8000/.

Testing the APIs:

You can test the available APIs using Postman or by directly navigating to the corresponding URL in your browser.

Important:
All available API endpoints can be found in the urls.py file.

To view users in the database, use the following endpoint:
http://127.0.0.1:8000/api/users/
