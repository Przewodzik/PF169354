from projekt.src.user import UserRole


class Auth:

    def __init__(self):
        self.logged_users = {}

    def login(self, user, email, password):

        if not isinstance(email, str):
            raise TypeError("Email must be a string")

        if not isinstance(password, str):
            raise TypeError("Password must be a string")

        if email != user.email or password != user.password:
            raise PermissionError("Invalid credentials !")

        if user.id in self.logged_users:
            raise PermissionError("User already logged in")

        self.logged_users[user.id] = user

        return True

    def logout(self, user):

        user = self.logged_users.get(user.id)
        if not user:
            raise PermissionError("User not logged in")

        self.logged_users.pop(user.id)

        return True

    def is_logged_in(self, user):

        return user.id in self.logged_users

    def is_admin(self, user):

        return user.role == UserRole.ADMIN
