from sqlmodel import create_engine , SQLModel

DATABASE_URL  = "postgresql://postgres.yievwgptecphkglqhvwk:S67FgS5m7877kne0@aws-1-ap-south-1.pooler.supabase.com:6543/postgres"

engine =  create_engine(DATABASE_URL)

def create_db_and_table () :
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__" :

    create_db_and_table()

    print("--- Chúc mừng! Bảng đã được tạo tự động trên Supabase ---")