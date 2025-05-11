------------------------------------------------------------------
--  Sample Data
--  psql  -h localhost -U realestate_user -d realestate_db -f sample_data.sql

-- docker compose exec db \
--  psql -U postgres -d realestate_db -f /tmp/sample_data.sql
------------------------------------------------------------------

-- ── 1 · USERS & ROLES ──────────────────────────────────────────
INSERT INTO users (email, full_name, user_type, password_hash) VALUES
  -- password for everyone below =  "test123"  (generated with werkzeug generate_password_hash)
  ('agent1@example.com',  'Alice Agent',   'agent',  '$pbkdf2-sha256$600000$$7thFUIy5m4m64u..IUaFufgKWmQt6UtJV1dHpFOxtlA'),
  ('agent2@example.com',  'Bob Broker',   'agent',   '$pbkdf2-sha256$600000$$7thFUIy5m4m64u..IUaFufgKWmQt6UtJV1dHpFOxtlA'),
  ('renter1@example.com', 'Randy Renter', 'renter',  '$pbkdf2-sha256$600000$$7thFUIy5m4m64u..IUaFufgKWmQt6UtJV1dHpFOxtlA'),
  ('renter2@example.com', 'Rachel Rent',  'renter',  '$pbkdf2-sha256$600000$$7thFUIy5m4m64u..IUaFufgKWmQt6UtJV1dHpFOxtlA');

INSERT INTO agents  (email) VALUES
  ('agent1@example.com'), ('agent2@example.com');

INSERT INTO renters (email) VALUES
  ('renter1@example.com'), ('renter2@example.com');

-- ── 2 · ADDRESSES ─────────────────────────────────────────────
INSERT INTO addresses (address_id, user_email, street, city, state, zip_code) VALUES
  (1,'renter1@example.com','101 Maple St','Chicago','IL','60616'),
  (2,'renter2@example.com','202 Oak Ave','Boston','MA','02110'),
  (3,'agent1@example.com', '300 Pine Rd','Austin','TX','78701');   -- for showcase only

-- ── 3 · CREDIT CARDS (renter only) ────────────────────────────
INSERT INTO credit_cards (card_number, renter_email, exp_date, cvv, billing_address)
VALUES
  ('4111111111111111', 'renter1@example.com','2027-05-01','123', 1),
  ('5555555555554444', 'renter2@example.com','2026-12-01','456', 2);

-- ── 4 · PROPERTIES & SUBTYPES ─────────────────────────────────
-- base table
INSERT INTO properties
  (property_id, agent_email, property_type, description, street, city, state,
   price, available_from, available_to, sqr_footage)
VALUES
  (10,'agent1@example.com','house',
   'Cozy 3-bedroom single-family home.',
   '12 Elm Dr','Chicago','IL', 2400,
   '2025-08-01','2025-12-31', 1800),

  (11,'agent1@example.com','apartment',
   'Modern loft apartment in downtown.',
   '500 W Madison St','Chicago','IL', 1800,
   '2025-06-15','2025-10-31',  900),

  (12,'agent2@example.com','commercial',
   'Retail storefront in busy plaza.',
   '800 Commercial Blvd','Boston','MA', 4200,
   '2025-07-01','2025-09-30', 3000);

-- subtype-specific rows
INSERT INTO houses (property_id,num_rooms)          VALUES (10,3);
INSERT INTO apartments (property_id,num_rooms,building_type) VALUES (11,1,'loft');
INSERT INTO commercial_buildings (property_id,business_type) VALUES (12,'retail');

-- ── 5 · BOOKINGS  (make sure they fit availability + not overlapping) ──────
INSERT INTO bookings
  (booking_id, property_id, renter_email, card_number,
   start_date, end_date, total_cost)
VALUES
  (100, 10, 'renter1@example.com', '4111111111111111',
   '2025-09-01','2025-11-30', 3*2400),      -- 3 months
  (101, 11, 'renter2@example.com', '5555555555554444',
   '2025-07-01','2025-08-31', 2*1800);      -- 2 months
