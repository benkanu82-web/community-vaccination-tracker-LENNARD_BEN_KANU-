
import sys
from datetime import date, timedelta


# Vaccine names and the minimum number of days between doses.
# The first number is 0 because there is no previous dose.
VACCINE_SCHEDULES = {
    "MMR": (0, 28),
    "COVID19": (0, 21),
    "TETANUS": (0,),
    "HEPATITIS_B": (0, 30, 150)
}


class Participant:
    """Stores basic information about a community participant."""

    AGE_GROUPS = ("child", "adult", "senior")
    _counter = 0

    def __init__(self, age_group, region):
        age_group = age_group.strip().lower()

        if not Participant.is_valid_age_group(age_group):
            raise ValueError(
                f"Please choose an age group from: "
                f"{', '.join(Participant.AGE_GROUPS)}"
            )

        Participant._counter += 1
        self.participant_id = f"P{Participant._counter:04d}"
        self.age_group = age_group
        self.region = region.strip().title()

    def display_info(self):
        """Display the participant's information."""
        print( 
            f"ID: {self.participant_id} | "
            f"Age group: {self.age_group} | "
            f"Region: {self.region}"
        )

    @classmethod
    def total_created(cls):
        """Return the total number of participants created."""
        return cls._counter

    @classmethod
    def from_dict(cls, data):
        """Create a participant using information from a dictionary."""
        return cls(data["age_group"], data["region"])

    @staticmethod
    def is_valid_age_group(value):
        """Check whether the age group is allowed."""
        return isinstance(value, str) and value in Participant.AGE_GROUPS


class VaccinationRecord:
    """Keeps track of the doses received for one vaccine."""

    def __init__(self, participant_id, vaccine):
        self.participant_id = participant_id
        self.vaccine = vaccine
        self.doses_received = 0
        self.last_dose_date = None

    def doses_required(self):
        """Return the number of doses needed for this vaccine."""
        return len(VACCINE_SCHEDULES[self.vaccine])

    def is_complete(self):
        """Check whether all required doses have been recorded."""
        return self.doses_received >= self.doses_required()

    def next_due_date(self):
        """Calculate when the next dose can be given."""
        if self.is_complete():
            return None

        if self.last_dose_date is None:
            return date.today()

        days_to_wait = VACCINE_SCHEDULES[self.vaccine][
            self.doses_received
        ]

        return self.last_dose_date + timedelta(days=days_to_wait)

    def add_dose(self, dose_date):
        """Record a dose if it follows the schedule."""
        if self.is_complete():
            return False, "All doses for this vaccine are already recorded."

        due_date = self.next_due_date()

        if self.last_dose_date is not None and dose_date < due_date:
            return False, f"Too early. The next dose is due on {due_date}."

        self.doses_received += 1
        self.last_dose_date = dose_date

        return True, "Dose recorded."

    def display_info(self):
        """Show the current vaccination status."""
        if self.is_complete():
            status = "COMPLETE"
        else:
            status = "IN PROGRESS"

        print(
            f"{self.participant_id} | {self.vaccine} | "
            f"{self.doses_received}/{self.doses_required()} doses | "
            f"{status}",
            end=""
        )

        if not self.is_complete() and self.last_dose_date is not None:
            print(f" | Next dose due: {self.next_due_date()}")
        else:
            print()


class VaccinationTracker:
    """Manages participants and their vaccination records."""

    def __init__(self):
        self.participants = {}
        self.records = {}

    def add_participant(self, participant):
        """Add a participant to the tracker."""
        self.participants[participant.participant_id] = participant
        print(f"Participant {participant.participant_id} added.")

    def display_participants(self):
        """Display all registered participants."""
        if not self.participants:
            print("No participants have been added yet.")
            return

        for participant in self.participants.values():
            participant.display_info()

    def record_dose(self, participant_id, vaccine, dose_date=None):
        """Find the participant and record a dose for the chosen vaccine."""
        participant_id = participant_id.upper()
        vaccine = vaccine.strip().upper()

        if dose_date is None:
            dose_date = date.today()

        if participant_id not in self.participants:
            print(f"Participant {participant_id} was not found.")
            return

        if vaccine not in VACCINE_SCHEDULES:
            print(
                f"Unknown vaccine. Available vaccines: "
                f"{', '.join(VACCINE_SCHEDULES)}"
            )
            return

        record_key = (participant_id, vaccine)

        if record_key not in self.records:
            self.records[record_key] = VaccinationRecord(
                participant_id, vaccine
            )

        success, message = self.records[record_key].add_dose(dose_date)
        print(f"{participant_id} / {vaccine}: {message}")

    def display_records(self):
        """Display all vaccination records."""
        if not self.records:
            print("No vaccination records have been added yet.")
            return

        for record in self.records.values():
            record.display_info()

    def summary(self):
        """Show a summary of the vaccination records."""
        total_participants = len(self.participants)
        total_records = len(self.records)

        completed_records = sum(
            1 for record in self.records.values()
            if record.is_complete()
        )

        print(
            f"Participants: {total_participants} | "
            f"Records: {total_records} | "
            f"Fully vaccinated: {completed_records}"
        )


def run_demo():
    """Run an example to show how the tracker works."""
    tracker = VaccinationTracker()

    print("=== Adding Participants ===")

    tracker.add_participant(Participant("child", "Western Area"))

    tracker.add_participant(
        Participant.from_dict({
            "age_group": "adult",
            "region": "northern province"
        })
    )

    tracker.add_participant(Participant("senior", "Eastern Province"))

    print("\n=== Participants ===")
    tracker.display_participants()
    print(f"Total created: {Participant.total_created()}")

    print("\n=== Recording Doses ===")

    start_date = date(2026, 1, 10)

    tracker.record_dose("P0001", "MMR", start_date)
    tracker.record_dose(
        "P0001", "MMR", start_date + timedelta(days=10)
    )
    tracker.record_dose(
        "P0001", "MMR", start_date + timedelta(days=30)
    )

    tracker.record_dose("P0002", "HEPATITIS_B", start_date)
    tracker.record_dose("P0003", "TETANUS", start_date)

    tracker.record_dose("P0009", "MMR", start_date)
    tracker.record_dose("P0002", "FLU", start_date)

    print("\n=== Vaccination Records ===")
    tracker.display_records()

    print("\n=== Summary ===")
    tracker.summary()


def ask_date(prompt):
    """Ask for a date and use today's date if the input is empty."""
    user_input = input(prompt).strip()

    if not user_input:
        return date.today()

    try:
        return date.fromisoformat(user_input)
    except ValueError:
        print("Invalid date. Today's date will be used.")
        return date.today()


def run_menu():
    """Display the main menu and respond to the user's choices."""
    tracker = VaccinationTracker()

    while True:
        print("\n--- Community Vaccination Tracker ---")
        print("1. Add a participant")
        print("2. Show participants")
        print("3. Record a dose")
        print("4. Show vaccination records")
        print("5. Show summary")
        print("6. Quit")

        choice = input("Choose an option (1-6): ").strip()

        if choice == "1":
            age_group = input(
                "Age group (child/adult/senior): "
            ).strip()

            region = input("Region: ").strip()

            try:
                participant = Participant(age_group, region)
                tracker.add_participant(participant)
            except ValueError as error:
                print(error)

        elif choice == "2":
            tracker.display_participants()

        elif choice == "3":
            participant_id = input(
                "Participant ID (e.g. P0001): "
            ).strip()

            print("Available vaccines:", ", ".join(VACCINE_SCHEDULES))
            vaccine = input("Enter vaccine name: ").strip()

            dose_date = ask_date(
                "Dose date (YYYY-MM-DD), or press Enter for today: "
            )

            tracker.record_dose(
                participant_id, vaccine, dose_date
            )

        elif choice == "4":
            tracker.display_records()

        elif choice == "5":
            tracker.summary()

        elif choice == "6":
            print("Goodbye.")
            break

        else:
            print("Invalid choice. Please select a number from 1 to 6.")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        run_demo()
    else:
        run_menu()
