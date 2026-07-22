# HabitGrid

#### Video Demo: <https://www.youtube.com/watch?v=HuQLqU34nb8>

#### Description:

HabitGrid is a web based habit tracker. The idea behind it is simple: you add a habit, and the app shows you a grid of squares representing the entire year, where each square corresponds to one day. If you complete your habit that day, you click the square and it turns blue. Over time, the grid fills in and you get a clear visual record of your consistency, along with a running streak count so you know how many days in a row you have kept a habit going. It is meant to be a fast, quiet tool you check once a day and then close.

I wanted to build something like this because most habit apps I tried felt too busy for what should be a simple task. They came with too many buttons, too many settings pages, and features I never touched. I wanted an app where I could open it, see my habits laid out as squares, click what I actually did today, and be done in about ten seconds. That single idea a habit tracker that gets out of your way was the goal behind this entire project. Everything I built was in service of keeping it that simple on the surface, even though there is a fair amount of logic running underneath.

## **Screenshots**

**Home page (dark mode)**
![Home Dark](screenshots/home%20dark.png)

**Home page (light mode)**
![Home Light](screenshots/home%20light.png)

## Distinctiveness and Complexity

CS50 psets give you starter files and a schema ready made. HabitGrid had none of that. I designed the database, the routes, and the logic myself.

One example: I first stored completed dates as a single text field. It didn't scale, so I redesigned it into three tables, adding a separate `habit_logs` table.

The heatmap was another challenge. `generate_heatmap` builds 365 days using Python's `datetime.timedelta`, groups them into 52 weeks, adds month borders, and blocks future dates from being logged. Getting the click to save behavior right in `script.js` also took a few tries before it felt responsive.

The app looks simple, but there's a lot of backend doing the work.

There's a full login system using Werkzeug for password hashing and Flask Session for keeping users logged in across pages. The database has three tables (`users`, `habits`, `habit_logs`), and every read or write has to be correct or it shows up immediately as a broken heatmap or a habit that won't save.

`generate_heatmap` was the hardest part. It builds a whole year by hand using python's `datetime.timedelta`, groups them into 52 weeks, and checks each day against the user's log history to mark it done or not. Future dates needed extra work too: CSS dims them and disables the cursor, and the JS click handler checks for a `future` class before it ever sends a request to `/log`. The `/log` route itself checks if a log already exists for that habit and date before deciding whether to insert or toggle it, so there are no duplicate rows.

None of this shows on the surface, but it's what made this take longer than a normal problem set.

## File Structure

`app.py` -> Main Flask application with routes for register, login, logout, home page, adding habits, deleting habits, clearing history, and saving heatmap clicks.

`helpers.py` -> Utility functions: `login_required` (decorator to block logged out users), `get_db` (opens SQLite connection and runs `schema.sql` if needed), `generate_heatmap` (builds the year grid), and `get_streak` (counts consecutive days a habit has been marked done).

`schema.sql` -> Defines the three tables: `users`, `habits`, and `habit_logs`.

`templates/layout.html` -> Base template with navbar, dark mode toggle, and flash messages.

`templates/home.html` -> Main page after login, loops through habits, renders heatmaps and streaks, and includes forms for habit management.

`templates/login.html` / `templates/register.html` -> Authentication forms.

`templates/about.html` -> Static page describing the app.

`static/css/style.css` -> Styling for themes, grid layout, animations, and month borders.

`static/js/script.js` -> Handles dark mode toggle and heatmap click events with immediate UI feedback and background fetch requests.

`requirements.txt` -> Python dependencies.

`habits.db` -> SQLite database file, auto created if missing.

## Installation and usage

Clone or download the project folder, then install dependencies:

```python

pip install -r requirements.txt

python app.py

```

Open your browser to the URL Flask prints in the terminal (usually `http://127.0.0.1:5000`). The database sets itself up automatically on first run, since `get_db` runs `schema.sql` and SQLite only creates tables that do not already exist. From there you can register an account, log in, and start adding habits right away.

## Design Decisions

I used three separate SQLite tables instead of one since one table was getting complicated real fast and had empty rows/columns. With 3 tables every query stays a plain select, insert, update, or delete with no joins. Easier to write and easier to debug.

I built the frontend in plain HTML, CSS, and JavaScript, no frameworks like bootstrap. I wanted to understand every line running in the browser.

Theme preference is stored in the browser's localStorage instead of the database. It's a display setting, not user data, so keeping it client side is simpler and faster. I considered adding a settings table for this, but learned that browser localStorage was a simpler way to store a display preference like theme, so I dropped that sql table.

The heatmap is built with Python's `timedelta` instead of a calendar library, so I have full control over how days are grouped into weeks and how today and future days are marked. And got a fun challenge to code.

## Limitations and future work

Currently, streak counts only update after a page refresh. I'd like to update the streak text live instead.

Other things I'd add later: habit reminders, a better mobile layout, and a way to export your habit history, I would also add a year selector, since the heatmap is currently locked to the current calendar year and won't show 2026 anymore once 2027 begins.

## Acknowledgements

Built with Flask, Flask-Session, Werkzeug, and SQLite on the backend, and plain HTML, CSS, and JavaScript on the frontend, no frontend frameworks like bootstrap or JS libraries.

I referred to the Flask and SQLite documentation for queries and session handling, and to Python's datetime and functools docs for date handling and decorators. I also watched CSS tutorials from Kevin Powell and Coding2GO for some of the frontend styling.

### Academic Honesty and AI Use

I used AI (ChatGPT and Claude) as a helper, asking conceptual questions rather than having it write code for me. Some examples:

- How a dark mode toggle is built
- An easier method to store a user's theme setting in the browser's localStorage
- What colors work well for a minimal UI, including hover colors for buttons
- How to build a calendar or heatmap layout from scratch
- Good color choices to make months look visually distinct on the grid
- How to reduce repetition in CSS using grouping selectors

I did not ask it to write project code for me, since the goal was to actually learn the whole project building process.

All instances of AI use are cited in comments within the source code, per CS50's Academic Honesty policy. The database schema, the heatmap and streak logic, and all routes and features were implemented by me.
