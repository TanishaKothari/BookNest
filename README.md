# BOOKNEST

## Video Demo: https://www.youtube.com/watch?v=cugCxrWKQRk
## Description:
BookNest is a dynamic web application designed to elevate the reading experience for book enthusiasts. With personalized book recommendations, wishlist management, reading history tracking, and robust user authentication, BookNest offers a comprehensive platform for users to discover, organize, and engage with their favorite books. Powered by user data and intuitive design, BookNest provides a seamless experience for users to explore new titles and track their reading progress.

### Project Overview
The project consists of the following files:
- app.py: This Python file serves as the core of the BookNest web application, built using the Flask framework. It deals with user authentication, routing, database interactions, and request handling functionalities. User authentication is handled securely, ensuring the integrity of user credentials. The routing system defines endpoints for various pages and functionalities, facilitating seamless navigation within the application. Through interactions with the SQLite database, app.py manages data related to users, books, wishlists, and reading history. It processes incoming HTTP requests, executes corresponding actions, and renders dynamic content using HTML templates. Error handling mechanisms gracefully manage exceptions and guide users through unexpected scenarios. Overall, app.py manages the uninterrupted functioning of BookNest, empowering users to explore, organize, and engage with their favorite books effortlessly.

- layout.html: This is the base HTML layout template used by all pages in the application. It defines the structure of the website, including the header, navigation bar, and footer, ensuring a consistent user interface across pages.

- apology.html: This HTML template is used to display error messages or apologies to users when something goes wrong in the application. It provides a user-friendly interface for communicating error information to users, helping them understand the issue and take appropriate action. The template includes dynamic content to customize the error message based on the specific error encountered.

- register.html: This HTML template is used for the registration page. It contains a form where users can create a new account by providing a username and password.

- login.html: This HTML template is used for the login page. It contains a form where users can input their username and password to log in.

- index.html: This HTML template represents the search page of the website. It contains a form where users can search for books by title, author, and genre.

- search.html: This HTML template is used to display the search results for books. It also gives options to add books to wishlist or mark as read.

- wishlist.html: This HTML template displays the user's wishlist, where they can view and manage books they want to read in the future. It also provides an option to mark wishlisted books as read.

- reading_history.html: This HTML template displays the user's reading history, showing books they have read and when they read them. It also provides the option for users to provide feedback on books by liking or disliking them.

- recommendations.html: This HTML template displays personalized book recommendations based on the user's reading history and preferences including liked books and genres of interest, as well as the top 10 most popular books.

- utilities.py: This file contains utility functions and decorators used throughout the BookNest web application. These functions aid in error handling, user authentication, and request processing.

- booknest.db: This is the SQLite database file that stores information about users, books, wishlists, and reading history. SQLite provides a lightweight and efficient solution for data storage and retrieval in web applications.

#### Features
- User Authentication: Users can register, log in, and log out securely.
- Book Search: Users can search for books by title, author, or genre.
- Wishlist: Users can add books to their wishlist for future reference.
- Reading History: Users can keep track of the books they have read and their feedback.
- Personalized Recommendations: BookNest recommends books based on the user's reading history and preferences, such as liked books and genres.
- Popular Books: BookNest also showcases the top 10 most read books by users.

#### Design Choices
- User-Centric Design: The application prioritizes user experience, providing intuitive interfaces and features that cater to the needs of book enthusiasts.
- Data-Driven Recommendations: BookNest leverages user data , by analyzing user behavior and book attributes to generate personalized recommendations ensuring users discover new titles they're likely to enjoy.
- Scalable Architecture: The project is built on the Flask framework, which offers scalability and flexibility for future enhancements and updates. The use of an SQLite database ensures efficient data storage and retrieval, while HTML templates maintain a consistent look and feel across the website.