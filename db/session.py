from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine



DATABASE_URL = 'postgresql://postgres:1234@localhost:5432/postgres'


engine = create_engine(DATABASE_URL)
conn  = engine.raw_connection() 
cursor = conn.cursor()

#cursor.execute('select * from task_list ;')
#df = pd.read_sql_query('select * from tasks ;', con=engine)
#res = cursor.fetchall()
#print(df)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    try:
        db = SessionLocal()
        yield db
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        db.close()