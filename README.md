# Commerce Project

This is a Django-based web application for managing online auctions done as part of CS50 WEB. This is project 2 called Commerce.

[Watch a demo!](https://youtu.be/Pus208TkuMY)


## Setup

1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd commerce
    ```

2. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Apply migrations:
    ```sh
    python manage.py migrate
    ```

4. Create a superuser:
    ```sh
    python manage.py createsuperuser
    ```

5. Run the development server:
    ```sh
    python manage.py runserver
    ```

## Features

- User authentication (login, logout, register)
- Create and manage auction listings
- Place bids on listings
- Add listings to watchlist
- View closed listings
- Categorize listings

## URLs

- `/admin/` - Admin site
- `/` - Home page with active listings
- `/login` - Login page
- `/logout` - Logout page
- `/register` - Registration page
- `/create` - Create a new listing
- `/listing/<str:title>` - View a specific listing
- `/closed_listing/<str:title>` - View a closed listing
- `/closed_listings` - View all closed listings
- `/watchlist` - View user's watchlist
- `/categories/<str:category>` - View listings by category

## Configuration

The project settings can be found in [commerce/settings.py](commerce/settings.py).

## Deployment

For ASGI configuration, see [commerce/asgi.py](commerce/asgi.py).

For WSGI configuration, see [commerce/wsgi.py](commerce/wsgi.py).

## License

This project is licensed under the MIT License.
