-- =========================================
-- Sample Data for Rental App
-- =========================================

BEGIN;

-- 1. USERS
INSERT INTO users (email, full_name, user_type, password_hash) VALUES
  ('agent1@example.com',  'Alice Agent',  'agent',  'password'),
  ('agent2@example.com',  'Eve Agent',    'agent',  'password'),
  ('renter1@example.com', 'Bob Renter',   'renter', 'password'),
  ('renter2@example.com', 'Carol Renter', 'renter', 'password');

-- 2. AGENTS (must reference existing users.email)
INSERT INTO agents (email, job_title, agency_name, contact_info) VALUES
  ('agent1@example.com', 'Senior Agent', 'Top Realty',   'alice@toprealty.com'),
  ('agent2@example.com', 'Junior Agent', 'City Homes',   'eve@cityhomes.com');

-- 3. RENTERS (must reference existing users.email)
INSERT INTO renters (email, desired_move_in, preferred_location, budget) VALUES
  ('renter1@example.com', '2025-07-01', 'Chicago',      2000.00),
  ('renter2@example.com', '2025-08-15', 'New York',     3000.00);

-- 4. ADDRESSES (any user can have multiple addresses)
INSERT INTO addresses (address_id, user_email, street, city,     state, zip_code) VALUES
  (1, 'renter1@example.com', '123 Maple St',    'Chicago',  'IL', '60601'),
  (2, 'renter2@example.com', '456 Oak Ave',     'New York', 'NY', '10001'),
  (3, 'agent1@example.com',  '789 Pine Rd',     'Chicago',  'IL', '60602'),
  (4, 'agent2@example.com',  '321 Cedar Ln',    'New York', 'NY', '10002');

-- 5. CREDIT CARDS (for renters, billing_address must exist & not be deleted while in use)
INSERT INTO credit_cards (card_number, renter_email, exp_date,    cvv, billing_address) VALUES
  ('4111111111111111', 'renter1@example.com', '2026-12-31', '123', 1),
  ('5555555555554444', 'renter2@example.com', '2027-06-30', '456', 2);

-- 6. PROPERTIES (master table—agent must exist)
INSERT INTO properties
  (property_id, agent_email, property_type, description,          street,            city,      state, price,    available_from, available_to, sqr_footage)
VALUES
  (1, 'agent1@example.com','house',     'Cozy 2-bedroom house',      '123 Maple St',   'Chicago', 'IL', 1650.00, '2025-07-01','2025-12-31', 1200),
  (2, 'agent1@example.com','apartment', 'Modern 1-bed apt',          '500 W Madison',  'Chicago', 'IL', 1450.00, '2025-07-01','2025-12-31',  800),
  (3, 'agent2@example.com','commercial','Downtown office space',     '100 Broadway',   'New York','NY', 5200.00, '2025-07-01','2025-12-31', 5000),
  (4, 'agent2@example.com','house',     'Spacious 3-bedroom house',  '456 Oak Ave',    'New York','NY', 2500.00, '2025-08-01','2026-01-31', 1800),
  (5, 'agent1@example.com','commercial','Retail storefront',        '789 Pine Rd',    'Chicago', 'IL', 7500.00, '2025-07-01','2025-12-31', 3000);

-- 7. HOUSES (only for property_type = 'house')
INSERT INTO houses (property_id, num_rooms) VALUES
  (1, 2),
  (4, 3);

-- 8. APARTMENTS (only for property_type = 'apartment')
INSERT INTO apartments (property_id, num_rooms, building_type) VALUES
  (2, 1, 'High-Rise');

-- 9. COMMERCIAL BUILDINGS (only for property_type = 'commercial')
INSERT INTO commercial_buildings (property_id, business_type) VALUES
  (3, 'Office'),
  (5, 'Retail');

-- 10. BOOKINGS (must reference property, renter & card)
INSERT INTO bookings
  (booking_id, property_id, renter_email, card_number, start_date,   end_date,     total_cost)
VALUES
  (1, 1, 'renter1@example.com', '4111111111111111', '2025-07-08','2025-07-15', 11550.00),
  (2, 2, 'renter2@example.com', '5555555555554444', '2025-08-20','2025-08-27', 10150.00);

COMMIT;
