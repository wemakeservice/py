from pykrx import stock
import pandas as pd
from datetime import datetime

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
                '종목코드': ticker,
                '종목명': name,
                '시장구분': 'KOSPI'
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
                '종목코드': ticker,
                '종목명': name,
                '시장구분': 'KOSDAQ'
            })
    
    # DataFrame으로 변환
    total_df = pd.DataFrame(kospi_info + kosdaq_info)
    
    # CSV 파일로 저장
    total_df.to_csv('stock_list.csv', index=False, encoding='utf-8-sig')
    print("종목 정보가 stock_list.csv 파일로 저장되었습니다.")
    print(f"스팩을 제외한 전체 종목 수: {len(total_df)}")
    
    return total_df

if __name__ == "__main__":
    stock_df = get_stock_info()