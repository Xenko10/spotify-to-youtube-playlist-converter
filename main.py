import os
from dotenv import load_dotenv
load_dotenv()

CLIENT_ID=os.getenv("CLIENT_ID")
CLIENT_SECRET=os.getenv("CLIENT_SECRET")

def main():
    print("Hello world!")
    print(CLIENT_ID)
    print(CLIENT_SECRET)


if __name__ == "__main__":
    main()