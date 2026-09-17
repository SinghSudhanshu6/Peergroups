# Peer Groups

A Django site where students can create and find interest-based meetup
groups. Anyone can start a group (what you're doing, where, and when),
other students can join it, and each group has its own comment thread
and photo-sharing section.

## Features

- **Browse & search** groups by keyword or interest tag (home page)
- **Create a group**: name, interest tag, description, location, meeting time,
  and public/private visibility
- **Edit a group** (leader only) — including date/time and location, any time
- **Public groups**: anyone can join instantly
- **Private groups**: join requests go to the leader, who approves or
  declines each one from the group page ("Join requests" section)
- **Comments** per group, for coordinating before meeting in person
  (members only)
- **Photo sharing** per group, for members only
- **Accounts**: sign up, log in, log out, forgot-password / reset-by-email,
  change password, and edit your own username/email
- Django admin at `/admin/` for moderation

## Project layout

```
peergroups/
  peergroups/       # project settings, root urls
  groups/           # the one app: models, views, forms, urls
    models.py        Group, Membership, Comment, Photo
    views.py         home, group_detail, create_group, join/leave, signup
    forms.py         GroupForm, CommentForm, PhotoForm, SignUpForm
    migrations/      hand-written 0001_initial.py (see note below)
  templates/
    base.html
    groups/          home.html, group_detail.html, group_form.html
    registration/    login.html, signup.html
```

## Setup

```bash
# 1. create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 2. install dependencies
pip install -r requirements.txt

# 3. apply migrations
python manage.py migrate

# 4. create an admin user (optional, for /admin/)
python manage.py createsuperuser

# 5. run the dev server
python manage.py runserver
```

Then visit http://127.0.0.1:8000/

> **Note on migrations:** this environment didn't have network access to
> run `django-admin`/`makemigrations` for me, so `0001_initial.py` and
> `0002_group_privacy_membership_status.py` were written by hand to match
> `models.py`. They're normal migrations and `migrate` will apply them —
> but if you change `models.py` further, run
> `python manage.py makemigrations` as usual afterward.

> **Note on password-reset emails:** in dev, reset emails print to your
> terminal (the console email backend) instead of actually sending — open
> the link that appears there. Swap in a real email backend before
> deploying (see the comment above `EMAIL_BACKEND` in `settings.py`).

**Already have a database from before this update?** These two fields are
new, so run `python manage.py migrate` again to pick up
`0002_group_privacy_membership_status.py`.

## Where to go next

- **Styling**: `templates/base.html` has the color/font tokens (a
  noticeboard/pinned-card look) — tweak the `:root` CSS variables there.
- **Deployment**: swap `DEBUG=True` and the SQLite database in
  `peergroups/settings.py` for production settings (Postgres, a real
  `SECRET_KEY` from an env var, `ALLOWED_HOSTS`, `DEBUG=False`, and a
  proper static/media file setup — e.g. WhiteNoise + S3 or similar).
- **Verifying students**: right now anyone can sign up. If you want to
  restrict this to students, the natural place is `SignUpForm`/`signup`
  view in `groups/forms.py` / `groups/views.py` — e.g. require a
  `.edu`-style email domain, or add an email-verification step.
- **Notifications**: you could add an email or in-app notification when
  someone joins a group or comments, via Django signals on `Membership`
  and `Comment`.
- **Interest tags**: currently a fixed list in `groups/models.py`
  (`INTEREST_CHOICES`). If you want users to add their own tags, turn
  this into a proper `Interest` model instead.
