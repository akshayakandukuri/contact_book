import json
import csv
import os
from datetime import datetime

DB_FILE = "contacts.json"
CSV_EXPORT = "contacts_export.csv"

# ---------- Utilities ----------

def load_data():
    if not os.path.exists(DB_FILE):
        return {"last_id": 0, "contacts": []}
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("Corrupted JSON. Starting fresh.")
        return {"last_id": 0, "contacts": []}

def save_data(db):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2)

def next_id(db):
    db["last_id"] += 1
    return db["last_id"]

def input_nonempty(prompt):
    while True:
        val = input(prompt).strip()
        if val:
            return val
        print("This field cannot be empty.")

def banner(title):
    print("\n" + "=" * 50)
    print(title)
    print("=" * 50)

# ---------- Core Features ----------

def add_contact(db):
    banner("Add Contact")
    name = input_nonempty("Name: ")
    phone = input_nonempty("Phone: ")
    email = input("Email: ").strip()
    address = input("Address: ").strip()

    contact = {
        "id": next_id(db),
        "name": name,
        "phone": phone,
        "email": email,
        "address": address,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    db["contacts"].append(contact)
    save_data(db)
    print(f"Contact '{name}' added.")

def list_contacts(db):
    banner("All Contacts")
    if not db["contacts"]:
        print("No contacts yet.")
        return

    sort_choice = input("Sort by: (n)ame / (d)ate added [n]: ").strip().lower() or "n"
    if sort_choice == "n":
        sorted_contacts = sorted(db["contacts"], key=lambda c: c["name"].lower())
    else:
        sorted_contacts = sorted(db["contacts"], key=lambda c: c["created_at"])

    print("\nID | Name               | Phone        | Email              | Address")
    print("-" * 70)
    for c in sorted_contacts:
        print(f"{c['id']:>2} | {c['name']:<18} | {c['phone']:<12} | {c['email']:<18} | {c['address']}")

def search_contacts(db):
    banner("Search Contacts")
    if not db["contacts"]:
        print("No contacts to search.")
        return
    term = input_nonempty("Enter name, phone, or email: ").lower()
    results = [
        c for c in db["contacts"]
        if term in c["name"].lower() or term in c["phone"] or term in c["email"].lower()
    ]
    if not results:
        print("No matches found.")
        return
    print("\nID | Name               | Phone        | Email              | Address")
    print("-" * 70)
    for c in results:
        print(f"{c['id']:>2} | {c['name']:<18} | {c['phone']:<12} | {c['email']:<18} | {c['address']}")

def edit_contact(db):
    banner("Edit Contact")
    if not db["contacts"]:
        print("No contacts to edit.")
        return
    try:
        cid = int(input("Enter contact ID: ").strip())
    except ValueError:
        print("Invalid ID.")
        return
    contact = next((c for c in db["contacts"] if c["id"] == cid), None)
    if not contact:
        print("Contact not found.")
        return

    print(f"Editing '{contact['name']}' (ID {cid})")
    new_name = input(f"Name [{contact['name']}]: ").strip() or contact["name"]
    new_phone = input(f"Phone [{contact['phone']}]: ").strip() or contact["phone"]
    new_email = input(f"Email [{contact['email']}]: ").strip() or contact["email"]
    new_address = input(f"Address [{contact['address']}]: ").strip() or contact["address"]

    contact.update({
        "name": new_name,
        "phone": new_phone,
        "email": new_email,
        "address": new_address
    })
    save_data(db)
    print("Contact updated.")

def delete_contact(db):
    banner("Delete Contact")
    if not db["contacts"]:
        print("No contacts to delete.")
        return
    try:
        cid = int(input("Enter contact ID: ").strip())
    except ValueError:
        print("Invalid ID.")
        return
    before = len(db["contacts"])
    db["contacts"] = [c for c in db["contacts"] if c["id"] != cid]
    if len(db["contacts"]) < before:
        save_data(db)
        print("Contact deleted.")
    else:
        print("Contact not found.")

def export_csv(db):
    banner("Export to CSV")
    if not db["contacts"]:
        print("No contacts to export.")
        return
    with open(CSV_EXPORT, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "name", "phone", "email", "address", "created_at"])
        writer.writeheader()
        for c in db["contacts"]:
            writer.writerow(c)
    print(f"Exported to {CSV_EXPORT}")

# ---------- Menu Loop ----------

def main_menu():
    db = load_data()
    actions = {
        "1": ("Add contact", add_contact),
        "2": ("List contacts", list_contacts),
        "3": ("Search contacts", 




search_contacts),
        "4": ("Edit contact", edit_contact),
        "5": ("Delete contact", delete_contact),
        "6": ("Export to CSV", export_csv),
        "7": ("Exit", None),
    }

    while True:
        banner("CONTACT BOOK")
        for k, (name, _) in actions.items():
            print(f"{k}. {name}")
        choice = input("\nChoose an option: ").strip()

        if choice not in actions:
            print("Invalid choice.")
            continue
        if choice == "7":
            print("Goodbye! Data saved to contacts.json")
            save_data(db)
            break
        func = actions[choice][1]
        func(db)
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main_menu()

