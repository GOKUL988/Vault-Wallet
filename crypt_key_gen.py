from cryptography.fernet import Fernet

gen_key = Fernet.generate_key() 
print("****************")
print("Generated key :","[",gen_key,"]")  
print("COPY THIS KEY AND PASTE TO KEY IN .env")

print("****************")
# Runs this file to generate a Key to decrypt and encrypt 