# 👥 Peer Groups

A Django web app where students can **find and create interest-based meetup groups**. Anyone can start a group (what, where, when), others can join, and every group gets its own comment thread and photo gallery.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Django](https://img.shields.io/badge/Django-5.x-092E20)
![Database](https://img.shields.io/badge/Database-SQLite-lightgrey)

## ✨ Features

- **Browse & search** upcoming groups by keyword or interest tag
- **Create a group** with name, interest, description, location, meeting time and privacy
- **Edit a group** (leader only), including date, time and location
- **Public groups**: anyone can join instantly
- **Private groups**: members send a join request, and the leader approves or declines it
- **Comments** inside each group (members only)
- **Photo sharing** inside each group (members only)
- **Accounts**: sign up, log in/out, change password, reset password by email, edit profile
- **Admin panel** at `/admin/` for moderation

## 🛠 Tech Stack

- Python, Django 5
- SQLite (default database)
- Pillow (image uploads)
- Django templates (HTML/CSS)

## 📁 Project Structure

```
peergroups/
├── peergroups/        # Project settings and root URLs
├── groups/            # Main app
│   ├── models.py      # Group, Membership, Comment, Photo
│   ├── views.py       # Home, group detail, create/edit, join/leave, signup
│   ├── forms.py       # GroupForm, CommentForm, PhotoForm, SignUpForm
│   ├── urls.py
│   └── migrations/
├── templates/
│   ├── base.html
│   ├── groups/        # home, group detail, group form
│   └── registration/  # login, signup, password reset, profile
├── media/             # Uploaded group photos
├── manage.py
└── requirements.txt
```

## 🚀 Getting Started

```bash
# 1. Clone the repository
git clone https://github.com/SinghSudhanshu6/Peergroups.git
cd Peergroups/peergroups

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply migrations
python manage.py migrate

# 5. (Optional) Create an admin user
python manage.py createsuperuser

# 6. Run the server
python manage.py runserver
```

Open **http://127.0.0.1:8000/** in your browser.

> In development, password-reset emails are printed in the terminal (console email backend).

## 🗺 Main Pages

| URL | Description |
|-----|-------------|
| `/` | Browse and search groups |
| `/group/new/` | Create a group |
| `/group/<id>/` | Group page: details, comments, photos |
| `/group/<id>/edit/` | Edit group (leader only) |
| `/accounts/signup/` | Create an account |
| `/accounts/login/` | Log in |
| `/admin/` | Admin panel |

## 🔒 Before Deploying

- Set `SECRET_KEY` from an environment variable
- Set `DEBUG = False` and update `ALLOWED_HOSTS`
- Use a production database such as PostgreSQL
- Configure a real email backend (SMTP)
- Set up static and media file hosting

## 🔮 Future Ideas

- Restrict sign-up to students (college email verification)
- Email or in-app notifications for joins and comments
- User-created interest tags
- Group deletion and member management

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
