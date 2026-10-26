-- Ekte Mat Online - SQLite schema (skeleton, plan 01).
-- Money columns are whole NOK. Dates/times are ISO 8601 text.

DROP TABLE IF EXISTS question;
DROP TABLE IF EXISTS order_line;
DROP TABLE IF EXISTS guest_group;
DROP TABLE IF EXISTS customer_order;
DROP TABLE IF EXISTS customer;
DROP TABLE IF EXISTS food_item;

CREATE TABLE food_item (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name_no TEXT NOT NULL,
  name_en TEXT NOT NULL,
  description TEXT NOT NULL DEFAULT '',
  price_per_person_nok INTEGER NOT NULL CHECK (price_per_person_nok >= 0),
  event_type TEXT NOT NULL CHECK (event_type IN ('lunch_meeting', 'party', 'wedding_dinner', 'other')),
  allergens TEXT NOT NULL DEFAULT '',
  image_filename TEXT,
  active INTEGER NOT NULL DEFAULT 1 CHECK (active IN (0, 1))
);

CREATE TABLE customer (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE,
  phone TEXT,
  customer_type TEXT NOT NULL CHECK (customer_type IN ('private', 'corporate')),
  organisation_number TEXT UNIQUE,
  password_hash TEXT NOT NULL DEFAULT '',
  is_admin INTEGER NOT NULL DEFAULT 0 CHECK (is_admin IN (0, 1)),
  created_at TEXT NOT NULL
);

-- "order" is a reserved word in SQL, hence customer_order.
CREATE TABLE customer_order (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  order_number TEXT NOT NULL UNIQUE,
  customer_id INTEGER NOT NULL REFERENCES customer (id),
  event_type TEXT NOT NULL CHECK (event_type IN ('lunch_meeting', 'party', 'wedding_dinner', 'other')),
  event_date TEXT NOT NULL,
  delivery_method TEXT NOT NULL CHECK (delivery_method IN ('delivery', 'pick_up')),
  delivery_address TEXT,
  status TEXT NOT NULL DEFAULT 'submitted'
    CHECK (status IN ('submitted', 'approved', 'in_preparation', 'delivered', 'rejected', 'cancelled')),
  payment_status TEXT NOT NULL DEFAULT 'not_paid'
    CHECK (payment_status IN ('not_paid', 'deposit_paid', 'invoiced', 'paid')),
  created_at TEXT NOT NULL
);

CREATE TABLE guest_group (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  order_id INTEGER NOT NULL REFERENCES customer_order (id) ON DELETE CASCADE,
  label TEXT,
  guest_count INTEGER NOT NULL CHECK (guest_count > 0),
  diet_notes TEXT
);

CREATE TABLE order_line (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  order_id INTEGER NOT NULL REFERENCES customer_order (id) ON DELETE CASCADE,
  food_item_id INTEGER NOT NULL REFERENCES food_item (id),
  quantity INTEGER NOT NULL CHECK (quantity > 0),
  unit_price_nok INTEGER NOT NULL CHECK (unit_price_nok >= 0)
);

CREATE TABLE question (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  customer_id INTEGER REFERENCES customer (id) ON DELETE SET NULL,
  name TEXT NOT NULL,
  email TEXT NOT NULL,
  subject TEXT NOT NULL,
  body TEXT NOT NULL,
  answer TEXT,
  created_at TEXT NOT NULL,
  answered_at TEXT
);
