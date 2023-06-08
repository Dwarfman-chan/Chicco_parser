CREATE TABLE categories (
    id INTEGER PRIMARY KEY,
    category TEXT,
    parent_id INTEGER

);

CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    category INTEGER,
    subcategory INTEGER,
    name TEXT,
    link_product TEXT,
    link_photo TEXT,
    price INTEGER,
    FOREIGN KEY (category) REFERENCES categories(id),
    FOREIGN KEY (subcategory) REFERENCES categories(id)
    
);

CREATE TABLE product_photo (
    id INTEGER,
    photo_code BYTEA,
    FOREIGN KEY (id) REFERENCES products(id)
);

CREATE TABLE product_info (
  id INTEGER,
  description TEXT,
  features TEXT,
  characteristic TEXT,
  FOREIGN KEY (id) REFERENCES products(id)

);