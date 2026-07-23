# MAI Nexus AI Database Schema

## Core Tables

1. users
- id
- full_name
- email
- phone
- password_hash
- role_id
- branch_id
- status
- created_at

2. roles
- id
- role_name
- description

3. branches
- id
- branch_name
- address
- phone

4. customers
- id
- customer_name
- phone
- address
- notes

5. services
- id
- service_name
- category
- price
- estimated_hours

6. orders
- id
- invoice_number
- customer_id
- service_id
- total_price
- payment_status
- order_status
- created_at

7. payments
- id
- order_id
- payment_method
- amount
- payment_date

8. inventory
- id
- item_name
- stock
- unit
- minimum_stock

9. ai_insights
- id
- order_id
- prediction
- recommendation

10. audit_logs
- id
- user_id
- activity
- created_at
