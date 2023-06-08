import sqlalchemy
import pandas as pd


def connect(credentials):
    db_user = credentials.get("db_user")
    db_password = credentials.get("db_password")
    db_host = credentials.get("db_host")
    db_port = credentials.get("db_port")
    db_name = credentials.get("db_name")

    try:
        connection = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
        engine = sqlalchemy.create_engine(connection)
        print("Успешное подключение к базе данных PostgreSQL")
        return engine
        
    except Exception as error:
        print("Ошибка при подключении к базе данных PostgreSQL:", error)


def disconnect(engine):
    try:
        engine.dispose()
        print("Подключение к базе данных PostgreSQL закрыто")
    except Exception as error:
        print("Ошибка при закрытии подключения к базе данных PostgreSQL:", error)


def table_appending(table, engine, data):
    clearing_table(table, engine)
    
    try:
        data.to_sql(table, engine, if_exists='append', index=False)
        print("Данные успешно записаны в таблицу")
    except Exception as error:
        print("Ошибка при записи данных в таблицу:", error)

    disconnect(engine)


def table_reader(table, engine):
    try:
        query = f"SELECT * FROM {table}"
        data = pd.read_sql(query, engine)
        print("Данные успешно прочитаны")
    except Exception as error:
        print("Ошибка при чтении данных в таблице:", error)

    disconnect(engine)

    return data


def clearing_table(table, engine):
    metadata = sqlalchemy.MetaData(bind=engine)

    table = sqlalchemy.Table(table, metadata, autoload=True)

    delete_stmt = table.delete()

    with engine.begin() as conn:
        conn.execute(delete_stmt)
