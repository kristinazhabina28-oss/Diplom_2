class ApiRoutes:
    BASE_URL = "https://stellarburgers.education-services.ru"
    REGISTER = BASE_URL + "/api/auth/register"
    LOGIN = BASE_URL + "/api/auth/login"
    USER = BASE_URL + "/api/auth/user"
    INGREDIENTS = BASE_URL + "/api/ingredients"
    ORDERS = BASE_URL + "/api/orders"


class ApiErrorMessages:
    USER_ALREADY_EXISTS = "User already exists"
    REQUIRED_FIELDS = "Email, password and name are required fields"
    INCORRECT_CREDENTIALS = "email or password are incorrect"
    INGREDIENTS_REQUIRED = "Ingredient ids must be provided"
    NOT_AUTHORISED = "You should be authorised"
