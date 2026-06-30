from waitress import serve

from app import app


def main():

    print("=" * 60)
    print("College Attendance Management System")
    print("=" * 60)
    print()
    print("Production Server : Waitress")
    print("Listening on all network interfaces")
    print()
    print("Local URL")
    print("http://127.0.0.1:5000")
    print()
    print("Network URL")
    print("http://192.168.0.7:5000")
    print()
    print("Press CTRL + C to stop")
    print("=" * 60)

    serve(
        app,
        host="0.0.0.0",
        port=5000,
        threads=8
    )


if __name__ == "__main__":
    main()