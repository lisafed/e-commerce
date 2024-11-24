
import mysql.connector # type: ignore
from faker import Faker
from mysql.connector import Error # type: ignore
import hashlib


# Initialisation de Faker
faker = Faker()

# Connexion à la base de données e_commerce-sql
try:
    connection = mysql.connector.connect(
        host='localhost',
        database='e_commerce_sql',
        user='root',
        password=''
    )
    cursor = connection.cursor()

    # Génération des utilisateurs
    for _ in range(50):
        username = faker.user_name()
        password_hash = hashlib.sha256('password'.encode()).hexdigest()  # Hachage du mot de passe
        email = faker.email()
        first_name = faker.first_name()
        last_name = faker.last_name()
        phone_number = faker.phone_number()

        cursor.execute("INSERT INTO users (username, password_hash, email, first_name, last_name, phone_number) VALUES (%s, %s, %s, %s, %s, %s)", 
                       (username, password_hash, email, first_name, last_name, phone_number))

    # Génération des adresses
    for user_id in range(1, 51):
        street = faker.street_address()
        city = faker.city()
        postal_code = faker.postcode()
        country = faker.country()

        cursor.execute("INSERT INTO address (users_id, street, city, postal_code, country) VALUES (%s, %s, %s, %s, %s)", 
                       (user_id, street, city, postal_code, country))

    # Génération des produits
    for _ in range(100):
        name = faker.word()
        description = faker.paragraph()
        price = round(faker.pyfloat(left_digits=3, right_digits=2, positive=True, min_value=5, max_value=500), 2)
        stock_quantity = faker.random_int(min=1, max=100)

        cursor.execute("INSERT INTO product (name, description, price, stock_quantity) VALUES (%s, %s, %s, %s)", 
                       (name, description, price, stock_quantity))

    # Génération des photos
    for _ in range(50):
        user_id = faker.random_int(min=1, max=50)
        product_id = faker.random_int(min=1, max=100)
        photo_url = faker.image_url()

        cursor.execute("INSERT INTO photo (users_id, product_id, photo_url) VALUES (%s, %s, %s)", 
                       (user_id, product_id, photo_url))

    # Génération des paniers et des articles de panier
    for user_id in range(1, 51):
        cursor.execute("INSERT INTO cart (users_id) VALUES (%s)", (user_id,))
        cart_id = cursor.lastrowid

        for _ in range(faker.random_int(min=1, max=5)):
            product_id = faker.random_int(min=1, max=100)
            quantity = faker.random_int(min=1, max=3)

            cursor.execute("INSERT INTO cart_item (cart_id, product_id, quantity) VALUES (%s, %s, %s)", 
                           (cart_id, product_id, quantity))

    # Génération des commandes et factures
    for cart_id in range(1, 51):
        total_amount = round(faker.pyfloat(left_digits=3, right_digits=2, positive=True, min_value=20, max_value=500), 2)
        payment_status = faker.random_element(elements=('pending', 'paid', 'cancelled'))

        cursor.execute("INSERT INTO command (cart_id, total_amount, payment_status) VALUES (%s, %s, %s)", 
                       (cart_id, total_amount, payment_status))

        invoice_status = 'paid' if payment_status == 'paid' else 'unpaid'
        cursor.execute("INSERT INTO invoices (command_id, total_amount, payment_status) VALUES (%s, %s, %s)", 
                       (cursor.lastrowid, total_amount, invoice_status))

    # Génération des méthodes de paiement
    for user_id in range(1, 51):
        payment_method = faker.credit_card_provider()
        card_number = faker.credit_card_number()
        iban = faker.iban()
        expiration_date = faker.credit_card_expire()
        cvv = faker.random_number(digits=3)

        cursor.execute("INSERT INTO payment (users_id, payment_method, card_number, iban, expiration_date, cvv) VALUES (%s, %s, %s, %s, %s, %s)", 
                       (user_id, payment_method, card_number, iban, expiration_date, cvv))

    #  sauvegarder les changements 
    connection.commit()


except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()