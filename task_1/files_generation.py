import os
import random
import numpy as np
import datetime as dt


EN_CHARS = [chr(i) for i in list(range(65, 91)) + list(range(97, 123))]
RU_CHARS = [chr(i) for i in list(range(1040, 1104))]

END_DATE = dt.date.today()
START_DATE = END_DATE - dt.timedelta(days=365 * 5 + 1)  # date 5 years ago


def random_date(start_date: dt.date, end_date: dt.date) -> dt.date:
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = np.random.randint(days_between_dates)
    rand_date = start_date + dt.timedelta(days=random_number_of_days)

    return rand_date


def transform_date(date: dt.date) -> str:
    new_date = str(date).split("-")
    new_date = list(reversed(new_date))
    new_date = ".".join(new_date)

    return new_date


def random_str(symbols_list: list, size: int) -> str:
    rand_str = np.random.choice(symbols_list, size)
    rand_str = "".join(rand_str)

    return rand_str


def rows_generator(num_rows: int):
    for i in range(num_rows):
        rand_date = random_date(START_DATE, END_DATE)
        rand_date_str = transform_date(rand_date)

        rand_en_str = random_str(EN_CHARS, 10)

        rand_ru_str = random_str(RU_CHARS, 10)

        rand_even_int = random.randrange(2, 1e8 + 1, 2)

        rand_float_str = str(round(np.random.uniform(1, 20), 9))
        rand_float_str = rand_float_str.replace(".", ",")[:-1]

        new_row = f"{rand_date_str}||{rand_en_str}||{rand_ru_str}||{rand_even_int}||{rand_float_str}||\n"

        yield new_row


def generate_files(directory: str, num_files: int, num_rows: int):
    if not os.path.isdir(directory):
        os.mkdir(directory)
        print(f"Directory {directory} created.")

    for i in range(num_files):
        file_path = os.path.join(directory, f"file_{i}.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            r_generator = rows_generator(num_rows)
            for new_row in r_generator:
                f.write(new_row)

        print(f"{file_path} successfully created. {num_files - i - 1} files remaining.")


generate_files("generated_files/", 100, 100000)
print("Generation completed successfully!")
