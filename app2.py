import json
import os
from datetime import datetime, timedelta
import calendar

# Core Logic: HabitManager
class HabitManager:
    def __init__(self, data_file="habits.json"):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_file = os.path.join(script_dir, data_file)
        
        self.habits = self.load_habits()

    def load_habits(self):
        """Load habits from a file."""
        try:
            with open(self.data_file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_habits(self):
        """Save habits to a file."""
        with open(self.data_file, "w") as f:
            json.dump(self.habits, f, indent=4)

    def add_habit(self, title, regularity):
        """Add a new habit with regularity."""
        habit = {
            "title": title,
            "regularity": regularity,  # 'daily', 'weekly', or 'monthly'
            "completed_on": []  # List of dates when the habit was completed
        }
        self.habits.append(habit)
        self.save_habits()

    def get_habits(self):
        """Return all habits."""
        return self.habits

    def mark_habit_completed(self, habit_no):
        """Mark a habit as completed for today."""
        if 1 <= habit_no <= len(self.habits):
            habit = self.habits[habit_no - 1]
            today = str(datetime.now().date())
            
            # Ensure we only mark it as completed once for a given day
            if today not in habit["completed_on"]:
                habit["completed_on"].append(today)
                self.save_habits()
                return True
        return False

    def get_completed_habits_for_month(self, year, month):
        """Get all habits completed on specific days of the month."""
        completed_habits_by_date = {}
        for habit in self.habits:
            for completed_date in habit["completed_on"]:
                completed_datetime = datetime.strptime(completed_date, "%Y-%m-%d")
                if completed_datetime.year == year and completed_datetime.month == month:
                    date_str = completed_datetime.strftime("%Y-%m-%d")
                    if date_str not in completed_habits_by_date:
                        completed_habits_by_date[date_str] = []
                    completed_habits_by_date[date_str].append(habit["title"])
        return completed_habits_by_date

# Interface Layer: CLI Implementation
class HabitTrackerCLI:
    def __init__(self):
        self.manager = HabitManager()

    def display_habits(self):
        """Display all habits."""
        habits = self.manager.get_habits()
        if not habits:
            print("No habits to show!\n")
            return

        print("\nYour Habits:")
        for i, habit in enumerate(habits, start=1):
            regularity = habit["regularity"]
            print(f"{i}. {habit['title']} (Regularity: {regularity})")
        print()

    def add_habit(self):
        """Prompt user to add a new habit."""
        title = input("Enter habit title: ")
        regularity = input("Enter habit regularity (daily, weekly, monthly): ").lower()
        if regularity not in ["daily", "weekly", "monthly"]:
            print("Invalid regularity! Habit must be 'daily', 'weekly', or 'monthly'.\n")
            return
        self.manager.add_habit(title, regularity)
        print("Habit added successfully!\n")

    def mark_habit_completed(self):
        """Prompt user to mark a habit as completed for today."""
        self.display_habits()
        try:
            habit_no = int(input("Enter habit number to mark as completed for today: "))
            if self.manager.mark_habit_completed(habit_no):
                print("Habit marked as completed for today!\n")
            else:
                print("Invalid habit number or habit already completed today!\n")
        except ValueError:
            print("Please enter a valid number!\n")

    def display_calendar(self):
        """Display a calendar for the current month and show completed habits."""
        today = datetime.today()
        month_days = calendar.monthcalendar(today.year, today.month)
        
        print("\nCalendar for", today.strftime('%B %Y'))
        print("Mo Tu We Th Fr Sa Su")
        
        # Get completed habits for the current month
        completed_habits_by_date = self.manager.get_completed_habits_for_month(today.year, today.month)
        
        for week in month_days:
            for day in week:
                if day == 0:
                    print("  ", end="   ")
                else:
                    day_str = str(day).rjust(2)
                    task_indicator = ""
                    date_str = f"{today.year}-{today.month:02d}-{day:02d}"
                    
                    # Check if there were completed habits on this day
                    if date_str in completed_habits_by_date:
                        task_indicator = "✓"  # Indicate task completion with a checkmark
                        # Display the day and the checkmark for completed tasks
                        print(f"{day_str}({task_indicator})", end="  ")
                    else:
                        print(f"{day_str}", end="  ")
            print()

    def run(self):
        """Main function for the CLI app."""
        while True:
            print("1. Add Habit")
            print("2. View Habits")
            print("3. Mark Habit as Completed for Today")
            print("4. View Calendar")
            print("5. Exit")

            choice = input("Enter your choice: ")

            if choice == "1":
                self.add_habit()
            elif choice == "2":
                self.display_habits()
            elif choice == "3":
                self.mark_habit_completed()
            elif choice == "4":
                self.display_calendar()
            elif choice == "5":
                print("Goodbye!")
                break
            else:
                print("Invalid choice, please try again!\n")

if __name__ == "__main__":
    app = HabitTrackerCLI()
    app.run()
