import csv
import random
from datetime import datetime, timedelta

# Set seed for reproducibility
random.seed(42)

print("Generating Swiggy Analytics Dataset...")

# 1. Generate dim_location.csv
locations = [
    (101, "Indiranagar", "Bengaluru", "Karnataka", "South"),
    (102, "Koramangala", "Bengaluru", "Karnataka", "South"),
    (103, "Connaught Place", "New Delhi", "Delhi", "North"),
    (104, "Bandra West", "Mumbai", "Maharashtra", "West"),
    (105, "Jubilee Hills", "Hyderabad", "Telangana", "South"),
    (106, "Park Street", "Kolkata", "West Bengal", "East"),
    (107, "Sector 17", "Chandigarh", "Punjab", "North"),
]

with open("dim_location.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["location_id", "area", "city", "state", "region"])
    writer.writerows(locations)

print("[OK] Created dim_location.csv")

# 2. Generate dim_restaurant.csv
restaurants = [
    (201, "Spice Garden", "Indian", 4.5, 101),
    (202, "Dragon Noodle Bar", "Chinese", 4.2, 102),
    (203, "Pizza Italia", "Italian", 4.6, 103),
    (204, "Burger House", "Fast Food", 4.1, 104),
    (205, "Biryani Zone", "Hyderabadi", 4.8, 105),
    (206, "Sweet Tooth Bakery", "Desserts", 4.4, 106),
    (207, "Tandoori Nights", "North Indian", 4.3, 107),
]

with open("dim_restaurant.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["restaurant_id", "restaurant_name", "cuisine_type", "rating", "location_id"])
    writer.writerows(restaurants)

print("[OK] Created dim_restaurant.csv")

# 3. Generate dim_dish.csv
dishes = [
    (301, "Butter Chicken", "Main Course", 350.00, 201),
    (302, "Paneer Tikka", "Starter", 280.00, 201),
    (303, "Hakka Noodles", "Main Course", 220.00, 202),
    (304, "Dim Sum Basket", "Starter", 250.00, 202),
    (305, "Margherita Pizza", "Main Course", 399.00, 203),
    (306, "Chicken Alfredo Pasta", "Main Course", 420.00, 203),
    (307, "Double Cheese Burger", "Main Course", 199.00, 204),
    (308, "French Fries", "Sides", 99.00, 204),
    (309, "Special Chicken Biryani", "Main Course", 320.00, 205),
    (310, "Mirchi Ka Salan", "Sides", 80.00, 205),
]

with open("dim_dish.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["dish_id", "dish_name", "category", "price", "restaurant_id"])
    writer.writerows(dishes)

print("[OK] Created dim_dish.csv")

# 4. Generate dim_date.csv (2024 to 2025)
start_date = datetime(2024, 1, 1)
end_date = datetime(2025, 12, 31)
cur_date = start_date

with open("dim_date.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["date_key", "full_date", "year", "quarter", "month_number", "month_name", "week_number", "day_of_week", "day_name", "is_weekend"])
    
    while cur_date <= end_date:
        d_key = int(cur_date.strftime("%Y%m%d"))
        f_date = cur_date.strftime("%Y-%m-%d")
        yr = cur_date.year
        qtr = f"Q{(cur_date.month - 1)//3 + 1}"
        m_num = cur_date.month
        m_name = cur_date.strftime("%B")
        w_num = cur_date.isocalendar()[1]
        dow = cur_date.weekday() + 1
        d_name = cur_date.strftime("%A")
        is_wknd = 1 if cur_date.weekday() in [5, 6] else 0
        
        writer.writerow([d_key, f_date, yr, qtr, m_num, m_name, w_num, dow, d_name, is_wknd])
        cur_date += timedelta(days=1)

print("[OK] Created dim_date.csv")

# 5. Generate fact_orders.csv (1000 orders)
order_statuses = ["Delivered", "Delivered", "Delivered", "Delivered", "Cancelled", "Refunded"]
payment_methods = ["UPI", "Credit Card", "Debit Card", "Net Banking", "Cash on Delivery"]

with open("fact_orders.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "order_id", "date_key", "restaurant_id", "dish_id", "location_id", 
        "quantity", "unit_price", "discount_amount", "total_amount", 
        "delivery_time_mins", "order_status", "payment_method"
    ])
    
    for oid in range(1001, 2001):
        random_days = random.randint(0, 729)
        o_date = start_date + timedelta(days=random_days)
        d_key = int(o_date.strftime("%Y%m%d"))
        
        dish = random.choice(dishes)
        dish_id = dish[0]
        rest_id = dish[4]
        loc_id = next(r[4] for r in restaurants if r[0] == rest_id)
        
        qty = random.randint(1, 4)
        u_price = dish[3]
        disc = round(random.choice([0, 0, 10, 20, 50]), 2)
        tot = round((u_price * qty) - disc, 2)
        del_time = random.randint(18, 55)
        status = random.choice(order_statuses)
        pay_method = random.choice(payment_methods)
        
        writer.writerow([
            f"ORD-{oid}", d_key, rest_id, dish_id, loc_id,
            qty, u_price, disc, tot, del_time, status, pay_method
        ])

print("[OK] Created fact_orders.csv (1,000 transaction records)")
print("Dataset Generation Complete!")
