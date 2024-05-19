from datetime import datetime
def successful_login_notification(username: str):
    print(f"successful login at {datetime.now()} - {username}")

def increase_count_file():
    with open("count.txt", mode="a+") as count_file:
        count_file.seek(0)
        content = count_file.readline()
        number = int(0 if not content else content) + 1
        count_file.truncate(0)
        count_file.seek(0)
        count_file.write(f"{number}\n")


