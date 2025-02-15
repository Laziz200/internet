import socket
import pymysql

db_password = 'LAZIZ'
db_name = 'Internet'

connection = pymysql.connect(
    password=db_password,
    database=db_name
)

cursor = connection.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS Internet")
cursor.execute("USE Internet")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Domain (
        id INT AUTO_INCREMENT PRIMARY KEY,
        domain VARCHAR(255) NOT NULL,
        ip VARCHAR(45) NOT NULL
    )
""")

with open('domains.txt', 'r') as file:
    domains = file.readlines()

for domain in domains:
    domain = domain.strip()
    try:
        ip_address = socket.gethostbyname(domain)
        cursor.execute("INSERT INTO Domain (domain, ip) VALUES (%s, %s)", (domain, ip_address))
    except socket.gaierror:
        print(f"Could not get IP for domain: {domain}")

connection.commit()
cursor.close()
connection.close()