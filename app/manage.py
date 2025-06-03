import os
import sys
print(sys.argv)

if len(sys.argv) < 2:
    print("Usage: python manage.py <command>")
    sys.exit(1)

command = sys.argv[1]

if command == "makemigrations":
    message = input("Enter migration message: ")
    os.system(f'alembic revision --autogenerate -m "{message}"')

elif command == "migrate":
    os.system("alembic upgrade head")

elif command == "runserver":
    os.system("uvicorn main:app --reload --port 5000")


    print("Invalid command. Available commands: makemigrations, migrate, runserver,createapp")
