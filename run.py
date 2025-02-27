from pykrx import stock
import pandas as pd
from datetime import datetime

# 삼성전자 종목코드
samsung_code = "005930"

# 데이터 조회 기간 설정
start_date = "20240101"
end_date = "20241212"

# OHLCV(시가/고가/저가/종가/거래량/거래대금) 데이터 추출
df = stock.get_market_ohlcv(start_date, end_date, samsung_code)

# 데이터프레임 열 이름 변경
df = df.rename(columns={'시가': 'open', '고가': 'high', '저가': 'low', '종가': 'close', '거래량': 'volume'})

# 날짜 인덱스 초기화
df = df.reset_index() 

df['날짜'] = df['날짜'].apply(lambda x: datetime.strftime(x, '%Y-%m-%d'))

# 거래대금 추가
df['Value'] = df['close'] * df['volume']

# 열 순서 재정렬
df = df[['날짜', 'open', 'high', 'low', 'close', 'volume', 'Value']]

# CSV 파일로 저장
df.to_csv('test.csv', encoding='utf-8-sig')

print("데이터가 test.csv 파일로 저장되었습니다.")