
**FastAPI User Management Project**

This project implements a user management system using FastAPI, a modern web framework for building APIs with Python. The system allows users to register, log in, update their information, and delete their accounts. MongoDB is used as the database to store user information securely.

**Features:**

1. **User Registration:** Users can register by providing a unique username and password. The system checks for duplicate usernames and ensures secure password storage.

2. **User Login:** Registered users can log in with their username and password to access the system's features securely.

3. **User Profile Management:** Users can update their passwords for added security. The system verifies the current password before allowing changes to be made.

4. **User Deletion:** Users have the option to delete their accounts from the system. Deletion requires confirmation through password authentication.

5. **MongoDB Integration:** User data is stored in a MongoDB database hosted on MongoDB Atlas. The project utilizes the PyMongo library to interact with the database.

6. **HTML Templates:** The project includes HTML templates for the user interface, allowing for a seamless user experience.

**Project Structure:**

- `main.py`: The main script containing the FastAPI application definition and route handlers.
- `html_templates/`: Directory containing HTML templates for the user interface.


**Usage:**

1. Clone the repository to your local machine.
2. Install dependencies listed in `requirements.txt` using `pip`.
3. Run the FastAPI application using `uvicorn`.
4. Access the application through the provided endpoints to register, log in, update profile, and delete account.

**Contributing:**

Contributions to this project are welcome! If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request on GitHub.

