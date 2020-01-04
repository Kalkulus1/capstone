from Crypto.PublicKey import RSA
key = RSA.generate(4096)
publicKey = key.publickey()
def encryption(plain):
	ciphertext = publicKey.encrypt(plain, 0)[0]
	encrypted = ciphertext.encode("hex")
	return ciphertext
def decryption(ciphertext):
	decrypted = key.decrypt(str(ciphertext))
	return decrypted
plaintext = str(1234.23)
encrypted = encryption(plaintext)
print(encrypted.encode("hex"))
print(decryption(encrypted))
