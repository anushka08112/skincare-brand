import pymysql

conn = pymysql.connect(
    host="localhost",
    user="root",
    password="Anushka@123",
    database="skincare",
    cursorclass=pymysql.cursors.DictCursor
)

cursor = conn.cursor()

# CREATE TABLE: users
# sql_command = """CREATE TABLE IF NOT EXISTS users (
#   user_id INT PRIMARY KEY AUTO_INCREMENT,
#   name VARCHAR(100),
#   email VARCHAR(100) UNIQUE,
#   password VARCHAR(255),
#   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# );"""
# cursor.execute(sql_command)

# # CREATE TABLE: products
# sql_command = """CREATE TABLE IF NOT EXISTS products (
#   product_id INT PRIMARY KEY AUTO_INCREMENT,
#   name VARCHAR(150),
#   description TEXT,
#   price DECIMAL(10,2),
#   stock INT,
#   image_url TEXT
# );"""
# cursor.execute(sql_command)

# # CREATE TABLE: ingredients
# sql_command = """CREATE TABLE IF NOT EXISTS ingredients (
#   ingredient_id INT PRIMARY KEY AUTO_INCREMENT,
#   name VARCHAR(100)
# );"""
# cursor.execute(sql_command)

# # CREATE TABLE: concerns
# sql_command = """CREATE TABLE IF NOT EXISTS concerns (
#   concern_id INT PRIMARY KEY AUTO_INCREMENT,
#   name VARCHAR(100)
# );"""
# cursor.execute(sql_command)

# # CREATE TABLE: product_ingredients
# sql_command = """CREATE TABLE IF NOT EXISTS product_ingredients (
#   id INT PRIMARY KEY AUTO_INCREMENT,
#   product_id INT,
#   ingredient_id INT,
#   FOREIGN KEY (product_id) REFERENCES products(product_id),
#   FOREIGN KEY (ingredient_id) REFERENCES ingredients(ingredient_id)
# );"""
# cursor.execute(sql_command)

# # CREATE TABLE: product_concerns
# sql_command = """CREATE TABLE IF NOT EXISTS product_concerns (
#   id INT PRIMARY KEY AUTO_INCREMENT,
#   product_id INT,
#   concern_id INT,
#   FOREIGN KEY (product_id) REFERENCES products(product_id),
#   FOREIGN KEY (concern_id) REFERENCES concerns(concern_id)
# );"""
# cursor.execute(sql_command)

# # CREATE TABLE: cart
# sql_command = """CREATE TABLE IF NOT EXISTS cart (
#   cart_id INT PRIMARY KEY AUTO_INCREMENT,
#   user_id INT,
#   product_id INT,
#   quantity INT,
#   FOREIGN KEY (user_id) REFERENCES users(user_id),
#   FOREIGN KEY (product_id) REFERENCES products(product_id)
# );"""
# cursor.execute(sql_command)

# # CREATE TABLE: orders
# sql_command = """CREATE TABLE IF NOT EXISTS orders (
#   order_id INT PRIMARY KEY AUTO_INCREMENT,
#   user_id INT,
#   total_amount DECIMAL(10,2),
#   status VARCHAR(50),
#   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#   FOREIGN KEY (user_id) REFERENCES users(user_id)
# );"""
# cursor.execute(sql_command)

# # CREATE TABLE: order_items
# sql_command = """CREATE TABLE IF NOT EXISTS order_items (
#   id INT PRIMARY KEY AUTO_INCREMENT,
#   order_id INT,
#   product_id INT,
#   quantity INT,
#   price DECIMAL(10,2),
#   FOREIGN KEY (order_id) REFERENCES orders(order_id),
#   FOREIGN KEY (product_id) REFERENCES products(product_id)
# );"""
# cursor.execute(sql_command)

# # CREATE TABLE: reviews
# sql_command = """CREATE TABLE IF NOT EXISTS reviews (
#   review_id INT PRIMARY KEY AUTO_INCREMENT,
#   user_id INT,
#   product_id INT,
#   rating INT,
#   comment TEXT,
#   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#   FOREIGN KEY (user_id) REFERENCES users(user_id),
#   FOREIGN KEY (product_id) REFERENCES products(product_id)
# );"""
# cursor.execute(sql_command)

# conn.commit()
# print("tables created successfully")



# inserting data into tables 

# query = "INSERT INTO users (name, email, password, active) VALUES (%s, %s, %s, %s)"
# values = [
#     ("Anushka", "anu@gmail.com", "1234", True)
# ]

# cursor.executemany(query, values)
# conn.commit()



# inserting into product table


# query = """
# INSERT INTO products (name, description, price, stock, image_url) VALUES
# ('Oil Control Face Wash', 'Removes excess oil and prevents acne', 299, 50, 'oil_cleanser.jpg'),
# ('Acne Control Serum', 'Reduces acne and controls sebum', 499, 40, 'acne_serum.jpg'),
# ('Tea Tree Face Wash', 'Anti-bacterial face wash for acne skin', 349, 60, 'teatree.jpg'),
# ('Mattifying Moisturizer', 'Controls oil and hydrates skin', 399, 30, 'matt_moist.jpg'),
# ('Salicylic Acid Toner', 'Unclogs pores and reduces breakouts', 299, 45, 'salicylic_toner.jpg'),

# ('Charcoal Cleanser', 'Deep cleans pores and removes dirt', 279, 50, 'charcoal_cleanser.jpg'),
# ('Oil Free Sunscreen SPF 50', 'Protects from UV without making skin oily', 349, 70, 'oilfree_sunscreen.jpg'),
# ('Pore Minimizing Serum', 'Tightens pores and smoothens skin', 599, 25, 'pore_serum.jpg'),
# ('Anti Acne Gel', 'Targets acne spots and reduces redness', 259, 40, 'acne_gel.jpg'),
# ('Clay Face Mask', 'Absorbs oil and detoxifies skin', 299, 35, 'clay_mask.jpg'),

# ('Hydrating Face Wash', 'Gentle cleanser for all skin types', 299, 60, 'hydrating_fw.jpg'),
# ('Vitamin C Serum', 'Brightens skin and reduces pigmentation', 499, 50, 'vitc.jpg'),
# ('Daily Moisturizer', 'Keeps skin hydrated all day', 399, 45, 'daily_moist.jpg'),
# ('Gentle Cleanser', 'Mild cleanser suitable for daily use', 279, 55, 'gentle_cleanser.jpg'),
# ('SPF 50 Sunscreen', 'Broad spectrum sun protection', 349, 80, 'sunscreen.jpg'),

# ('Glow Serum', 'Enhances skin glow and radiance', 599, 30, 'glow_serum.jpg'),
# ('Night Repair Cream', 'Repairs skin overnight', 699, 20, 'night_cream.jpg'),
# ('Aloe Vera Gel', 'Soothes and hydrates skin', 199, 100, 'aloe.jpg'),
# ('Brightening Toner', 'Evens skin tone and refreshes', 299, 50, 'bright_toner.jpg'),
# ('Hydration Boost Serum', 'Deep hydration for soft skin', 549, 35, 'hydration_serum.jpg')
# """

# cursor.execute(query)
# conn.commit()
# print("products inserted ✅")



# # inserting into concerns table

# query = """
# INSERT INTO concerns (name) VALUES
# ('Acne Marks'),
# ('Pigmentation / Dark Spots'),
# ('Acne / Pimple'),
# ('Acne Scars'),
# ('Open Pores'),
# ('Dry & Dull Skin'),
# ('View All Products')
# """
# cursor.execute(query)
# conn.commit()
# print("concerns inserted")



# inserting into concerns table     
query = """
INSERT INTO product_concerns (product_id, concern_id) VALUES

-- Acne Marks
(2,1),
(8,1),
(9,1),
(16,1),

-- Pigmentation / Dark Spots
(12,2),
(16,2),
(19,2),
(20,2),

-- Acne / Pimple
(1,3),
(2,3),
(3,3),
(5,3),
(6,3),
(9,3),
(10,3),

-- Acne Scars
(2,4),
(8,4),
(16,4),
(17,4),

-- Open Pores
(6,5),
(8,5),
(10,5),
(5,5),

-- Dry & Dull Skin
(11,6),
(13,6),
(17,6),
(18,6),
(20,6),

-- View All Products
(1,7),
(2,7),
(3,7),
(4,7),
(5,7),
(6,7),
(7,7),
(8,7),
(9,7),
(10,7),
(11,7),
(12,7),
(13,7),
(14,7),
(15,7),
(16,7),
(17,7),
(18,7),
(19,7),
(20,7);
"""
cursor.execute(query)
conn.commit()
print("product_concern linked ✅")


# query = """
# INSERT INTO ingredients (name) VALUES
# ('Niacinamide Range'),
# ('Salicylic Range'),
# ('Vitamin C Range'),
# ('AHA-BHA Range'),
# ('Kojic Range'),
# ('Hyaluronic Range'),
# ('View All Products')
# """
# cursor.execute(query)
# conn.commit()
# print("ingredients inserted")






# query = """
# INSERT INTO cart (user_id, product_id, quantity) VALUES
# (1, 1, 2),
# (1, 3, 1),
# (2, 2, 1),
# (2, 5, 3);
# """
# cursor.execute(query)
# conn.commit()
# print("cart data inserted")

# query = """
# INSERT INTO orders (user_id, total_amount, status) VALUES
# (1, 1098, 'Completed'),
# (2, 799, 'Pending');
# """
# cursor.execute(query)
# conn.commit()
# print("orders data inserted")


# query = """
# INSERT INTO order_items (order_id, product_id, quantity, price) VALUES
# (1, 1, 2, 299),
# (1, 3, 1, 349),
# (2, 2, 1, 499),
# (2, 5, 1, 299);
# """
# cursor.execute(query)
# conn.commit()
# print("order_items data inserted")


# query = """
# INSERT INTO reviews (user_id, product_id, rating, comment) VALUES

# -- PRODUCT 1 (Oil Control Face Wash)
# (1,1,5,'Amazing face wash, controls oil perfectly!'),
# (2,1,4,'Good for oily skin, works well'),
# (3,1,5,'Best cleanser I have used'),
# (4,1,4,'Removes oil without drying skin'),

# -- PRODUCT 2 (Acne Control Serum)
# (1,2,5,'Helped reduce my acne in few weeks'),
# (2,2,4,'Very effective serum'),
# (3,2,5,'Lightweight and works great'),
# (4,2,3,'Took time but shows results'),

# -- PRODUCT 3 (Tea Tree Face Wash)
# (1,3,5,'Refreshing and good for acne'),
# (2,3,4,'Nice smell and effective'),
# (3,3,4,'Good daily cleanser'),
# (4,3,5,'Loved it for oily skin'),

# -- PRODUCT 4 (Mattifying Moisturizer)
# (1,4,4,'Keeps skin matte all day'),
# (2,4,5,'Perfect for oily skin'),
# (3,4,4,'Hydrates well without oiliness'),
# (4,4,3,'Average but okay'),

# -- PRODUCT 5 (Salicylic Acid Toner)
# (1,5,5,'Reduced my breakouts quickly'),
# (2,5,4,'Very effective toner'),
# (3,5,5,'Clears pores nicely'),
# (4,5,4,'Good for acne-prone skin'),

# -- PRODUCT 6 (Charcoal Cleanser)
# (1,6,5,'Deep cleans my skin'),
# (2,6,4,'Removes dirt well'),
# (3,6,4,'Good but slightly drying'),
# (4,6,5,'Loved the result'),

# -- PRODUCT 7 (Oil Free Sunscreen)
# (1,7,5,'No white cast, amazing'),
# (2,7,4,'Lightweight sunscreen'),
# (3,7,5,'Perfect for daily use'),
# (4,7,4,'Non greasy and smooth'),

# -- PRODUCT 8 (Pore Minimizing Serum)
# (1,8,5,'Pores look smaller now'),
# (2,8,4,'Good serum'),
# (3,8,4,'Works slowly but good'),
# (4,8,5,'Skin feels smoother'),

# -- PRODUCT 9 (Anti Acne Gel)
# (1,9,5,'Works instantly on pimples'),
# (2,9,4,'Reduces redness'),
# (3,9,5,'Must have for acne'),
# (4,9,4,'Good spot treatment'),

# -- PRODUCT 10 (Clay Face Mask)
# (1,10,5,'Removes oil instantly'),
# (2,10,4,'Good detox mask'),
# (3,10,5,'Skin feels clean'),
# (4,10,4,'Nice weekly mask'),

# -- PRODUCT 11 (Hydrating Face Wash)
# (1,11,5,'Very gentle and hydrating'),
# (2,11,4,'Good for dry skin'),
# (3,11,5,'Does not dry skin'),
# (4,11,4,'Nice cleanser'),

# -- PRODUCT 12 (Vitamin C Serum)
# (1,12,5,'Gives glow to skin'),
# (2,12,4,'Brightens well'),
# (3,12,5,'Good for pigmentation'),
# (4,12,4,'Visible results'),

# -- PRODUCT 13 (Daily Moisturizer)
# (1,13,5,'Perfect daily moisturizer'),
# (2,13,4,'Hydrates well'),
# (3,13,5,'Very lightweight'),
# (4,13,4,'Nice product'),

# -- PRODUCT 14 (Gentle Cleanser)
# (1,14,5,'Very mild and soothing'),
# (2,14,4,'Good for sensitive skin'),
# (3,14,5,'Loved it'),
# (4,14,4,'Works well'),

# -- PRODUCT 15 (SPF 50 Sunscreen)
# (1,15,5,'Great protection'),
# (2,15,4,'No irritation'),
# (3,15,5,'Perfect sunscreen'),
# (4,15,4,'Nice finish'),

# -- PRODUCT 16 (Glow Serum)
# (1,16,5,'Skin looks radiant'),
# (2,16,4,'Nice glow effect'),
# (3,16,5,'Loved the finish'),
# (4,16,4,'Good product'),

# -- PRODUCT 17 (Night Repair Cream)
# (1,17,5,'Skin feels repaired overnight'),
# (2,17,4,'Good night cream'),
# (3,17,5,'Very nourishing'),
# (4,17,4,'Nice texture'),

# -- PRODUCT 18 (Aloe Vera Gel)
# (1,18,5,'Very soothing'),
# (2,18,4,'Good for irritation'),
# (3,18,5,'Multi-use product'),
# (4,18,4,'Nice gel'),

# -- PRODUCT 19 (Brightening Toner)
# (1,19,5,'Evens skin tone'),
# (2,19,4,'Nice toner'),
# (3,19,5,'Gives glow'),
# (3,19,4,'Good product'),
# (4,19,4,'Good product'),

# -- PRODUCT 20 (Hydration Boost Serum)
# (1,20,5,'Deep hydration'),
# (2,20,4,'Skin feels soft'),
# (3,20,5,'Very effective'),
# (4,20,4,'Nice serum')
# """
# cursor.execute(query)
# conn.commit()
# print("reviews data inserted")

# query = """
# INSERT INTO product_ingredients (product_id, ingredient_id) VALUES

# (1,1),(4,1),(7,1),(8,1),
# (2,2),(3,2),(5,2),(6,2),(9,2),(10,2),
# (12,3),(16,3),(19,3),
# (5,4),(10,4),(19,4),
# (12,5),(16,5),(19,5),
# (11,6),(13,6),(14,6),(15,6),(17,6),(18,6),(20,6),
# (2,1),(8,2),(16,6)
# """

# cursor.execute(query)
# conn.commit()

# print("product_ingredients inserted ✅")