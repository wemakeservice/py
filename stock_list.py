from pykrx import stock
import pandas as pd
from datetime import datetime
import pymysql

def get_stock_info():
    # 오늘 날짜 설정
    today = datetime.today().strftime("%Y%m%d")
    
    # 코스피 종목 정보 가져오기
    kospi_df = stock.get_market_ticker_list(today, market="KOSPI")
    kospi_info = []
    
    print("코스피 종목 정보 수집 중...")
    for ticker in kospi_df:
        name = stock.get_market_ticker_name(ticker)
        # 스팩 제외
        if "스팩" not in name:
            kospi_info.append({
                'ticker': ticker,
                'name': name,
                'market_type': 'KOSPI'
            })
    
    # 코스닥 종목 정보 가져오기
    kosdaq_df = stock.get_market_ticker_list(today, market="KOSDAQ")
    kosdaq_info = []
    
    print("코스닥 종목 정보 수집 중...")
    for ticker in kosdaq_df:
        name = stock.get_market_ticker_name(ticker)
        # 스팩 제외
        if "스팩" not in name:
            kosdaq_info.append({
                'ticker': ticker,
                'name': name,
                'market_type': 'KOSDAQ'
            })
    
    # DataFrame으로 변환
    total_df = pd.DataFrame(kospi_info + kosdaq_info)
    
    # CSV 파일로 저장
    total_df.to_csv('stock_list.csv', index=False, encoding='utf-8-sig')
    print("종목 정보가 stock_list.csv 파일로 저장되었습니다.")
    print(f"스팩을 제외한 전체 종목 수: {len(total_df)}")
    
    return total_df

def insert_into_db(df):
    # MariaDB 연결 설정
    connection = pymysql.connect(
        host='localhost',
        user='your_username',
        password='your_password',
        db='your_database',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    
    try:
        with connection.cursor() as cursor:
            # 테이블 생성 (필요한 경우)
            create_table_query = """
            CREATE TABLE IF NOT EXISTS stock_info (
                ticker VARCHAR(20) PRIMARY KEY,
                name VARCHAR(200),
                market_type VARCHAR(20)
            )
            """
            cursor.execute(create_table_query)
            
            # 데이터 삽입
            insert_query = """
            INSERT INTO stock_info (ticker, name, market_type)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE
                name = VALUES(name),
                market_type = VALUES(market_type)
            """
            for _, row in df.iterrows():
                cursor.execute(insert_query, (row['ticker'], row['name'], row['market_type']))
        
        # 변경사항 커밋
        connection.commit()
        print("데이터가 MariaDB에 성공적으로 등록되었습니다.")
    
    finally:
        connection.close()

if __name__ == "__main__":
    stock_df = get_stock_info()
    insert_into_db(stock_df)