
import csv
from collections import defaultdict

FILE_NAME = "sales.csv"
REPORT_FILE = "sales_report.txt"


def load_sales():
    sales = []

    try:
        with open(FILE_NAME, "r", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                sales.append({
                    "product": row["product"],
                    "quantity": int(row["quantity"]),
                    "price": float(row["price"])
                })

    except FileNotFoundError:
        print("Sales file not found.")
    except (ValueError, KeyError):
        print("Invalid sales data.")

    return sales


def analyze_sales(sales):
    revenue_by_product = defaultdict(float)
    units_by_product = defaultdict(int)

    total_revenue = 0
    total_units = 0

    for sale in sales:
        revenue = sale["quantity"] * sale["price"]

        total_revenue += revenue
        total_units += sale["quantity"]

        revenue_by_product[sale["product"]] += revenue
        units_by_product[sale["product"]] += sale["quantity"]

    return (
        total_revenue,
        total_units,
        revenue_by_product,
        units_by_product
    )


def display_report(sales):
    if not sales:
        print("No sales data available.")
        return

    total, units, revenue_data, units_data = analyze_sales(sales)

    best_product = max(units_data, key=units_data.get)

    report = []
    report.append("========== SALES REPORT ==========")
    report.append(f"Total Sales Revenue: Rs. {total:.2f}")
    report.append(f"Total Units Sold: {units}")
    report.append(f"Number of Products: {len(units_data)}")
    report.append(
        f"Best Selling Product: {best_product} "
        f"({units_data[best_product]} units)"
    )

    report.append("\n--- PRODUCT-WISE REVENUE ---")

    for product, revenue in sorted(revenue_data.items()):
        report.append(
            f"{product}: Rs. {revenue:.2f} "
            f"| Units: {units_data[product]}"
        )

    for line in report:
        print(line)

    with open(REPORT_FILE, "w") as file:
        file.write("\n".join(report))

    print(f"\nReport saved to {REPORT_FILE}")


def main():
    sales = load_sales()

    if sales:
        display_report(sales)


if __name__ == "__main__":
    main()
