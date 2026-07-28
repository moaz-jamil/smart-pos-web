import datetime
import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils import timezone
from authentication.models import User, Business
from branches.models import Branch
from subscriptions.models import SubscriptionPlan, BusinessSubscription
from products.models import Category, Brand, Product
from suppliers.models import Supplier
from customers.models import Customer
from inventory.models import Warehouse, StockMovement
from purchases.models import Purchase, PurchaseItem
from sales.models import Sale, SaleItem, Coupon
from expenses.models import ExpenseCategory, Expense
from employees.models import EmployeeProfile
from attendance.models import Attendance
from payroll.models import Payroll
from settings_app.models import BusinessSetting
from notifications.models import Notification

class Command(BaseCommand):
    help = "Seeds initial realistic production data for SmartPOS enterprise application."

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Starting SmartPOS Data Seeding..."))

        # 1. Super Admin
        super_admin, created = User.objects.get_or_create(
            username="superadmin",
            defaults={
                "email": "superadmin@smartpos.com",
                "first_name": "Super",
                "last_name": "Admin",
                "role": User.ROLE_SUPER_ADMIN,
                "is_staff": True,
                "is_superuser": True,
            }
        )
        if created:
            super_admin.set_password("password123")
            super_admin.save()
            self.stdout.write(self.style.SUCCESS("Created Super Admin: superadmin / password123"))

        # 2. Business
        business, _ = Business.objects.get_or_create(
            name="SmartPOS Retail Corp",
            defaults={
                "email": "info@smartposretail.com",
                "phone": "+1 (555) 019-2831",
                "address": "742 Evergreen Terrace, Suite 100, New York, NY",
                "tax_number": "TAX-99882211-US",
                "status": True,
            }
        )

        # Business Settings
        setting, _ = BusinessSetting.objects.get_or_create(
            business=business,
            defaults={
                "currency_symbol": "$",
                "tax_number": "TAX-99882211-US",
                "tax_rate": 5.00,
                "receipt_header": "Welcome to SmartPOS Retail Corp HQ\nQuality Products & Excellent Service",
                "receipt_footer": "Thank you for your business!\nPlease retain receipt for returns within 14 days.",
                "theme": "dark",
                "low_stock_threshold": 5,
            }
        )

        # 3. Subscriptions
        plan_ent, _ = SubscriptionPlan.objects.get_or_create(
            name="Enterprise Unlimited",
            defaults={
                "price": 199.99,
                "max_branches": 10,
                "max_users": 50,
                "max_products": 10000,
                "description": "Full access to all POS modules, multi-branch, and analytics.",
            }
        )

        BusinessSubscription.objects.get_or_create(
            business=business,
            plan=plan_ent,
            defaults={
                "start_date": timezone.now().date() - datetime.timedelta(days=90),
                "end_date": timezone.now().date() + datetime.timedelta(days=275),
                "status": True,
            }
        )

        # 4. Branches
        branch_main, _ = Branch.objects.get_or_create(
            business=business,
            name="Main Store HQ",
            defaults={
                "code": "BR-001",
                "phone": "+1 (555) 019-1001",
                "email": "hq@smartposretail.com",
                "address": "742 Evergreen Terrace, New York, NY",
            }
        )

        branch_downtown, _ = Branch.objects.get_or_create(
            business=business,
            name="Downtown Express",
            defaults={
                "code": "BR-002",
                "phone": "+1 (555) 019-1002",
                "email": "downtown@smartposretail.com",
                "address": "120 Broadway St, New York, NY",
            }
        )

        # 5. Users: Admin Owner & Cashiers
        owner, created = User.objects.get_or_create(
            username="owner",
            defaults={
                "email": "owner@smartposretail.com",
                "first_name": "Alexander",
                "last_name": "Wright",
                "role": User.ROLE_ADMIN,
                "business": business,
                "branch": branch_main,
                "phone": "+1 (555) 111-2222",
                "is_staff": True,
            }
        )
        if created:
            owner.set_password("password123")
            owner.save()

        branch_main.manager = owner
        branch_main.save()

        cashier1, created = User.objects.get_or_create(
            username="cashier1",
            defaults={
                "email": "cashier1@smartposretail.com",
                "first_name": "David",
                "last_name": "Miller",
                "role": User.ROLE_EMPLOYEE,
                "business": business,
                "branch": branch_main,
                "phone": "+1 (555) 333-4444",
            }
        )
        if created:
            cashier1.set_password("password123")
            cashier1.save()

        cashier2, created = User.objects.get_or_create(
            username="cashier2",
            defaults={
                "email": "cashier2@smartposretail.com",
                "first_name": "Sophia",
                "last_name": "Taylor",
                "role": User.ROLE_EMPLOYEE,
                "business": business,
                "branch": branch_downtown,
                "phone": "+1 (555) 555-6666",
            }
        )
        if created:
            cashier2.set_password("password123")
            cashier2.save()

        # Employee Profiles
        EmployeeProfile.objects.get_or_create(
            user=cashier1,
            defaults={"business": business, "designation": "Senior POS Cashier", "salary": 3200.00}
        )
        EmployeeProfile.objects.get_or_create(
            user=cashier2,
            defaults={"business": business, "designation": "Branch Cashier", "salary": 2900.00}
        )

        # 6. Customers
        customer_usr, created = User.objects.get_or_create(
            username="johndoe",
            defaults={
                "email": "john.doe@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "role": User.ROLE_CUSTOMER,
                "business": business,
            }
        )
        if created:
            customer_usr.set_password("password123")
            customer_usr.save()

        c1, _ = Customer.objects.get_or_create(
            business=business,
            phone="+1 (555) 777-8888",
            defaults={
                "user": customer_usr,
                "name": "John Doe",
                "email": "john.doe@example.com",
                "address": "450 5th Ave, NY",
                "reward_points": 150,
                "wallet_balance": 50.00,
                "outstanding_balance": 0.00,
            }
        )

        c2, _ = Customer.objects.get_or_create(
            business=business,
            phone="+1 (555) 888-9999",
            defaults={
                "name": "Jane Smith",
                "email": "jane.smith@example.com",
                "address": "88 Park Ave, NY",
                "reward_points": 80,
                "wallet_balance": 25.00,
                "outstanding_balance": 12.50,
            }
        )

        # 7. Categories & Brands
        cat_elec, _ = Category.objects.get_or_create(business=business, name="Electronics", defaults={"description": "Gadgets, Accessories & Hardware"})
        cat_groc, _ = Category.objects.get_or_create(business=business, name="Groceries & Snacks", defaults={"description": "Packaged Foods & Beverages"})
        cat_app, _ = Category.objects.get_or_create(business=business, name="Apparel & Fashion", defaults={"description": "Clothing, Shirts & Jackets"})
        cat_home, _ = Category.objects.get_or_create(business=business, name="Home & Living", defaults={"description": "Decor, Essentials & Appliances"})

        brand_tech, _ = Brand.objects.get_or_create(business=business, name="TechPro", defaults={"description": "Premium Electronics Brand"})
        brand_fresh, _ = Brand.objects.get_or_create(business=business, name="FreshChoice", defaults={"description": "Organic Food Essentials"})
        brand_urban, _ = Brand.objects.get_or_create(business=business, name="UrbanStyle", defaults={"description": "Modern Lifestyle Apparel"})

        # 8. Suppliers
        supp_1, _ = Supplier.objects.get_or_create(
            business=business,
            company_name="Global Tech Imports",
            defaults={
                "contact_name": "Marcus Vance",
                "phone": "+1 (555) 400-1010",
                "email": "marcus@globaltech.com",
                "address": "100 Industrial Pkwy, CA",
                "outstanding_balance": 450.00,
            }
        )
        supp_2, _ = Supplier.objects.get_or_create(
            business=business,
            company_name="Prime Organic Distributors",
            defaults={
                "contact_name": "Elena Rostova",
                "phone": "+1 (555) 400-2020",
                "email": "elena@primeorganic.com",
                "address": "50 Farm Road, OR",
                "outstanding_balance": 0.00,
            }
        )

        # 9. Products
        products_data = [
            ("Wireless Bluetooth Headphones", "89010001", "SKU-1001", cat_elec, brand_tech, supp_1, Decimal("45.00"), Decimal("89.99"), Decimal("5.0"), Decimal("0.0"), 45, 10),
            ("USB-C Fast Charging Cable 2m", "89010002", "SKU-1002", cat_elec, brand_tech, supp_1, Decimal("5.00"), Decimal("14.99"), Decimal("5.0"), Decimal("5.0"), 120, 15),
            ("Smart Fitness Watch Series 5", "89010003", "SKU-1003", cat_elec, brand_tech, supp_1, Decimal("80.00"), Decimal("159.99"), Decimal("5.0"), Decimal("10.0"), 18, 5),
            ("Ergonomic Wireless Mouse", "89010004", "SKU-1004", cat_elec, brand_tech, supp_1, Decimal("15.00"), Decimal("34.99"), Decimal("5.0"), Decimal("0.0"), 3, 5),  # Low Stock!
            ("Mechanical RGB Keyboard", "89010005", "SKU-1005", cat_elec, brand_tech, supp_1, Decimal("40.00"), Decimal("79.99"), Decimal("5.0"), Decimal("0.0"), 2, 5),   # Low Stock!
            ("Organic Green Tea 100g Pack", "89010006", "SKU-1006", cat_groc, brand_fresh, supp_2, Decimal("3.50"), Decimal("7.99"), Decimal("0.0"), Decimal("0.0"), 85, 20),
            ("Premium Extra Virgin Olive Oil 1L", "89010007", "SKU-1007", cat_groc, brand_fresh, supp_2, Decimal("9.00"), Decimal("18.50"), Decimal("0.0"), Decimal("0.0"), 60, 10),
            ("Dark Chocolate Bar 85% 100g", "89010008", "SKU-1008", cat_groc, brand_fresh, supp_2, Decimal("1.80"), Decimal("4.49"), Decimal("0.0"), Decimal("0.0"), 150, 25),
            ("Men Cotton Crew Neck T-Shirt", "89010009", "SKU-1009", cat_app, brand_urban, supp_1, Decimal("8.00"), Decimal("24.99"), Decimal("5.0"), Decimal("10.0"), 40, 10),
            ("Denim Slim Fit Jeans", "89010010", "SKU-1010", cat_app, brand_urban, supp_1, Decimal("22.00"), Decimal("59.99"), Decimal("5.0"), Decimal("0.0"), 25, 8),
            ("Stainless Steel Thermal Bottle 750ml", "89010011", "SKU-1011", cat_home, brand_tech, supp_2, Decimal("7.50"), Decimal("19.99"), Decimal("5.0"), Decimal("0.0"), 4, 10), # Low Stock!
            ("Ceramic Coffee Mug 350ml", "89010012", "SKU-1012", cat_home, brand_tech, supp_2, Decimal("2.50"), Decimal("8.99"), Decimal("5.0"), Decimal("0.0"), 95, 15),
        ]

        created_products = []
        for name, barcode, sku, cat, brand, supp, p_cost, p_sell, tax, disc, qty, min_qty in products_data:
            p, _ = Product.objects.get_or_create(
                business=business,
                barcode=barcode,
                sku=sku,
                defaults={
                    "category": cat,
                    "brand": brand,
                    "supplier": supp,
                    "name": name,
                    "purchase_price": p_cost,
                    "selling_price": p_sell,
                    "tax_rate": tax,
                    "discount_rate": disc,
                    "stock_quantity": qty,
                    "min_stock_level": min_qty,
                    "status": True,
                }
            )
            created_products.append(p)

        # 10. Warehouse & Stock Movements
        wh, _ = Warehouse.objects.get_or_create(business=business, name="Central Warehouse", defaults={"location": "Bldg 4, Industrial Zone"})

        for p in created_products:
            StockMovement.objects.get_or_create(
                business=business,
                product=p,
                movement_type=StockMovement.TYPE_IN,
                quantity=p.stock_quantity + 20,
                reference_number="INIT-STOCK-2026",
                defaults={"created_by": owner, "notes": "Initial stock ingestion"}
            )

        # 11. Purchases
        po_1, _ = Purchase.objects.get_or_create(
            business=business,
            invoice_number="PO-2026-001",
            defaults={
                "branch": branch_main,
                "supplier": supp_1,
                "total_amount": Decimal("1250.00"),
                "paid_amount": Decimal("800.00"),
                "payment_status": Purchase.PAYMENT_PARTIAL,
                "received_status": Purchase.RECEIVED_STATUS_RECEIVED,
                "created_by": owner,
            }
        )
        PurchaseItem.objects.get_or_create(
            purchase=po_1,
            product=created_products[0],
            defaults={"quantity": 20, "unit_cost": Decimal("45.00"), "total_cost": Decimal("900.00")}
        )
        PurchaseItem.objects.get_or_create(
            purchase=po_1,
            product=created_products[1],
            defaults={"quantity": 70, "unit_cost": Decimal("5.00"), "total_cost": Decimal("350.00")}
        )

        # 12. Coupons
        coupon, _ = Coupon.objects.get_or_create(
            business=business,
            code="WELCOME10",
            defaults={
                "discount_percentage": Decimal("10.00"),
                "min_purchase": Decimal("30.00"),
                "valid_until": timezone.now().date() + datetime.timedelta(days=180),
            }
        )

        # 13. Sales History (Generate past 15 days of dynamic sales)
        today = timezone.now().date()
        for i in range(15, -1, -1):
            sale_date = today - datetime.timedelta(days=i)
            # Create 2 to 4 sales per day
            for s_idx in range(1, random.randint(3, 5)):
                inv_num = f"INV-2026-{i:02d}{s_idx:02d}"
                if Sale.objects.filter(invoice_number=inv_num).exists():
                    continue
                prod1 = random.choice(created_products)
                prod2 = random.choice(created_products)
                qty1 = random.randint(1, 3)
                qty2 = random.randint(1, 2)

                subtotal = (prod1.selling_price * qty1) + (prod2.selling_price * qty2)
                tax_val = subtotal * Decimal("0.05")
                total = subtotal + tax_val

                sale = Sale.objects.create(
                    business=business,
                    branch=branch_main if s_idx % 2 == 0 else branch_downtown,
                    customer=c1 if s_idx % 2 == 0 else c2,
                    cashier=cashier1 if s_idx % 2 == 0 else cashier2,
                    invoice_number=inv_num,
                    total_amount=total,
                    tax_amount=tax_val,
                    discount_amount=Decimal("0.00"),
                    paid_amount=total,
                    change_amount=Decimal("0.00"),
                    payment_method=Sale.METHOD_CASH if s_idx % 2 == 0 else Sale.METHOD_CARD,
                    payment_status=Sale.STATUS_PAID,
                )
                sale.created_at = timezone.make_aware(datetime.datetime.combine(sale_date, datetime.time(random.randint(9, 19), random.randint(0, 59))))
                sale.save()

                SaleItem.objects.create(
                    sale=sale,
                    product=prod1,
                    quantity=qty1,
                    unit_price=prod1.selling_price,
                    subtotal=prod1.selling_price * qty1,
                )
                SaleItem.objects.create(
                    sale=sale,
                    product=prod2,
                    quantity=qty2,
                    unit_price=prod2.selling_price,
                    subtotal=prod2.selling_price * qty2,
                )

        # 14. Expense Categories & Expenses
        exp_rent, _ = ExpenseCategory.objects.get_or_create(business=business, name="Store Rent")
        exp_util, _ = ExpenseCategory.objects.get_or_create(business=business, name="Utilities & Electricity")
        exp_sal, _ = ExpenseCategory.objects.get_or_create(business=business, name="Employee Payroll")
        exp_net, _ = ExpenseCategory.objects.get_or_create(business=business, name="Internet & Communications")

        Expense.objects.get_or_create(
            business=business,
            title="Monthly Store HQ Rent",
            amount=Decimal("2200.00"),
            expense_date=today - datetime.timedelta(days=10),
            defaults={"category": exp_rent, "branch": branch_main, "payment_method": "Bank Transfer"}
        )
        Expense.objects.get_or_create(
            business=business,
            title="High Speed Fiber Internet",
            amount=Decimal("150.00"),
            expense_date=today - datetime.timedelta(days=5),
            defaults={"category": exp_net, "branch": branch_main, "payment_method": "Credit Card"}
        )
        Expense.objects.get_or_create(
            business=business,
            title="Electricity Bill",
            amount=Decimal("380.00"),
            expense_date=today - datetime.timedelta(days=3),
            defaults={"category": exp_util, "branch": branch_main, "payment_method": "Cash"}
        )

        # 15. Attendance & Payroll
        for emp in [cashier1, cashier2]:
            for d in range(10, -1, -1):
                att_date = today - datetime.timedelta(days=d)
                Attendance.objects.get_or_create(
                    business=business,
                    employee=emp,
                    date=att_date,
                    defaults={
                        "branch": emp.branch,
                        "clock_in": datetime.time(9, 0),
                        "clock_out": datetime.time(17, 30),
                        "working_hours": Decimal("8.50"),
                    }
                )

            Payroll.objects.get_or_create(
                business=business,
                employee=emp,
                month=today.month,
                year=today.year,
                defaults={
                    "base_salary": Decimal("3000.00"),
                    "bonus": Decimal("200.00"),
                    "deductions": Decimal("150.00"),
                    "net_salary": Decimal("3050.00"),
                    "payment_status": Payroll.STATUS_PAID,
                }
            )

        # 16. Notifications
        Notification.objects.get_or_create(
            business=business,
            user=owner,
            title="Low Stock Alert!",
            defaults={
                "message": "Products 'Ergonomic Wireless Mouse' & 'Mechanical RGB Keyboard' are below minimum stock threshold.",
                "notification_type": Notification.TYPE_LOW_STOCK,
                "is_read": False,
            }
        )
        Notification.objects.get_or_create(
            business=business,
            user=owner,
            title="New Supplier Delivery Received",
            defaults={
                "message": "Purchase Order PO-2026-001 has been marked as RECEIVED from Global Tech Imports.",
                "notification_type": Notification.TYPE_PURCHASE,
                "is_read": False,
            }
        )

        self.stdout.write(self.style.SUCCESS("SmartPOS Data Seeding Completed Successfully!"))
