import click
from project.user import register_user, login_user
from project.transactions import add_transaction, view_all_transactions, update_transaction, delete_transaction, fetch_by_category
from project.budget import set_budget, view_budget
from project.report import monthly_report, yearly_report
from project.data_persistant import backup_database,restore_database 

@click.group()
def cli():
    """Personal Finance Management CLI"""
    pass

# Register command
@cli.command()
@click.option('--username', prompt='Username', help='Your username')
@click.option('--password', prompt='Password', help='Your password') #hide_input=True, confirmation_prompt=True, 
def register(username, password):
    """Register a new user"""
    try:
        register_user(username, password)
        click.echo('User registered successfully!')
    except ValueError as e:
        click.echo(str(e))

# Login command
@cli.command()
def login():
    username = click.prompt("Enter username")
    password = click.prompt("Enter password", hide_input=True)
    """Login a user"""
    try:
        user_id = login_user(username, password)
        click.echo(f"Login successful! User ID: {user_id}")
        logged_in_menu(user_id)
    except ValueError as e:
        click.echo(f"Error: {e}")

# Logged-in menu function
def logged_in_menu(user_id):
    """User's dashboard after login"""
    # db_manager = DatabaseManager() 
    while True:
        click.echo("\n--- Menu ---")
        click.echo("1. Add transaction")
        click.echo("2. View all transactions")
        click.echo("3. Update transaction")
        click.echo("4. Delete transaction")
        click.echo("5. Fetch transactions by category")
        click.echo("6. Monthly report")
        click.echo("7. Yearly report")
        click.echo("8. Set budget")
        click.echo("9. View budget")
        click.echo("10. Backup database")
        click.echo("11. Restore database")
        click.echo("12. Logout")

        choice = click.prompt("Enter your choice", type=int)

        if choice == 1:
        # Prompt for transaction type (income/expense)
            transaction_type = click.prompt(
                "Enter transaction type", 
                type=click.Choice(['income', 'expense'])
            )

            # Dynamically prompt for category based on transaction type
            if transaction_type == 'income':
                category = click.prompt(
                    "Enter category", 
                    type=click.Choice(['salary', 'bonus', 'other']), 
                    show_choices=True
                )
            elif transaction_type == 'expense':
                category = click.prompt(
                    "Enter category", 
                    type=click.Choice(['rent', 'food', 'drink', 'travel', 'other']), 
                    show_choices=True
                )

            # Prompt for amount
            amount = click.prompt("Enter amount", type=float)

            # Add the transaction
            add_transaction(user_id, transaction_type, category, amount)
            click.echo("Transaction added successfully!")

        elif choice == 2:
            view_all_transactions(user_id)
            click.echo("All transactions")
        elif choice == 3:
            transaction_id = click.prompt("Enter transaction ID", type=int)
            category = click.prompt("Enter new category", type=str)
            amount = click.prompt("Enter new amount", type=float)
            update_transaction(transaction_id, category, amount)

        elif choice == 4:
            transaction_id = click.prompt("Enter transaction ID", type=int)
            delete_transaction(transaction_id)
            click.echo("Transactions deleted successfully")

        elif choice == 5:
            transaction_type = click.prompt("transaction_type", type=click.Choice(['income', 'expense']))
            fetch_by_category(user_id, transaction_type)
        
        elif choice == 6:
            month = click.prompt('Enter the month (YYYY-MM)', type=str)
            monthly_report(user_id, month)
            click.echo("Monthly report shown")

        elif choice == 7:
            year = click.prompt('Enter the year (YYYY)', type=str)
            yearly_report(user_id, year)
            click.echo("Yearly report shown")

        elif choice == 8:
            category = click.prompt("Enter category", type=str)
            monthly_budget = click.prompt("Enter monthly budget", type=float)
            month = click.prompt("Enter month (YYYY-MM)", type=str)
            set_budget(user_id, category,  monthly_budget,month)
            click.echo("budegt set successfully")

        elif choice == 9:
            view_budget(user_id)
            click.echo("Your budget category wise")

        elif choice == 10:
            # Backup database
            backup_path = click.prompt("Enter backup file path (default: 'backup_finance.db')", default="backup_finance.db")
            backup_database(backup_path)

        elif choice == 11:
            # Restore database
            backup_path = click.prompt("Enter backup file path (default: 'backup_finance.db')", default="backup_finance.db")
            restore_database(backup_path)

        elif choice == 12:
            click.echo("Logging out...")
            break

        else:
            click.echo("Invalid choice. Please try again.")

@cli.command()
def run():
    """Run the Personal Finance Management Application"""
    cli()

if __name__ == '__main__':
    cli()


# username c- ZXCVB

# pass - Go12@