from werkzeug.security import generate_password_hash

password = "teacher123"

hashed_password = generate_password_hash(
    password
)

print(hashed_password)