import sqlite3


def check_database(offer):
    with sqlite3.connect("realty.db") as connection:
        cursor = connection.cursor()
        for data in offer:
            avito_id = data[0]
            cursor.execute(
                """
                SELECT avito_id FROM offers WHERE avito_id = (?)
            """,
                (avito_id,),
            )
            result = cursor.fetchone()
            if result is None:
                cursor.execute(
                    """
                    INSERT INTO offers
                    VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime())
                """,
                    data,
                )
                connection.commit()
                print(f"Объявление {avito_id} добавлено в базу данных")
            else:
                print(f"Объявление {avito_id} не добавлено в базу данных")


def create_table():
    connection = sqlite3.connect("realty.db")
    cursor = connection.cursor()
    cursor.execute(
        """ CREATE TABLE IF NOT EXISTS offers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    avito_id INTEGER UNIQUE NOT NULL,
                    rooms TEXT NOT NULL,
                    area REAL NOT NULL,
                    price REAL NOT NULL,
                    address TEXT NOT NULL,
                    district TEXT NOT NULL,
                    floor INTEGER NOT NULL,
                    total_floor INTEGER NOT NULL,
                    phone_number TEXT NOT NULL,
                    text TEXT,
                    online_display TEXT NOT NULL,
                    url TEXT NOT NULL,
                    Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    );
    """
    )
    connection.close()


def main():
    create_table()


if __name__ == "__main__":
    main()
