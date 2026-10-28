# Community Vaccination Tracker

A simple Python program that tracks vaccine doses for people in a community. It shows who has started a vaccine, who has finished it, and when the next dose is due. It was built with Object-Oriented Programming (OOP) for the Health domain of the OOP assignment.

## Features
- Add participants using an age group (child, adult or senior) and a region only
- Record vaccine doses (MMR, COVID19, TETANUS, HEPATITIS_B)
- Rejects doses given too early, unknown vaccines and unknown participants
- Shows each participant's progress (e.g. `1/2 doses`), the next due date, and a summary
- Runs in the terminal with a numbered menu, or as an automatic demo

## Requirements
Python 3.8 or newer. No extra libraries are needed.

## How to run
```
python vaccination_tracker.py --demo    # automatic example
python vaccination_tracker.py           # interactive menu
```

## Project structure
| File | Purpose |
|------|---------|
| `vaccination_tracker.py` | All source code |
| `sample_output.txt` | Output of the `--demo` run |
| `README.md` | This file |
| `LICENSE` | MIT licence |

## How the code is organised
| Class | Responsibility |
|-------|----------------|
| `Participant` | An anonymous community member: ID, age group and region |
| `VaccinationRecord` | One participant's progress for one vaccine |
| `VaccinationTracker` | Stores participants and records in dictionaries and connects the other two classes |

- **Data structure:** dictionaries store the objects (`participants` by ID, `records` by `(participant_id, vaccine)`). Tuples hold the vaccine schedules and allowed age groups.
- **Instance methods:** e.g. `add_dose()`, `display_info()`, `record_dose()`
- **Class methods:** `Participant.total_created()`, `Participant.from_dict()`
- **Static method:** `Participant.is_valid_age_group()`

## Example usage
Part of an interactive session (typed input follows each prompt):
```
--- Community Vaccination Tracker ---
1. Add a participant
2. Show participants
3. Record a dose
4. Show vaccination records
5. Show summary
6. Quit
Choose an option (1-6): 1
Age group (child/adult/senior): child
Region: Western Area
Participant P0001 added.

Choose an option (1-6): 3
Participant ID (e.g. P0001): P0001
Available vaccines: MMR, COVID19, TETANUS, HEPATITIS_B
Enter vaccine name: MMR
Dose date (YYYY-MM-DD), or press Enter for today: 2026-01-10
P0001 / MMR: Dose recorded.

Choose an option (1-6): 4
P0001 | MMR | 1/2 doses | IN PROGRESS | Next dose due: 2026-02-07
```
See `sample_output.txt` for the full demo output.

## Digital Public Goods (DPG) alignment
- **Open-source:** the code is public on GitHub under the MIT licence, uses only the Python standard library, and anyone can use, study and improve it.
- **Inclusive and accessible design:** a plain numbered text menu with short prompts and clear error messages. It needs no internet connection, special hardware or extra software, and the dose date can be left blank to use today's date.
- **Privacy-respecting:** no names, birth dates, phone numbers or addresses are stored. Participants get an automatic anonymous ID (e.g. `P0001`) and only a general age group and region.
- **Modular and reusable:** each class has one job. Vaccine schedules are kept as data in one place (`VACCINE_SCHEDULES`), so new vaccines can be added without changing the program logic.

## Limitations
Records are kept in memory only and are lost when the program closes.

## Author
[Your full name] - [Module name / code], Limkokwing University of Creative Technology, Sierra Leone

## Licence
MIT. See `LICENSE`.
