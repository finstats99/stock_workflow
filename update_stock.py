import yfinance as yf
import pandas as pd
from datetime import datetime

# 1. 분석할 종목 리스트 (티커 입력: 삼성전자, 애플, 비트코인 등)
tickers = {
    "Samsung Electronics": "005930.KS",
    "Apple": "AAPL",
    "Bitcoin": "BTC-USD",
    "Tesla": "TSLA"
}

def check_golden_cross(ticker_symbol):
    # 최근 50일간의 데이터 가져오기
    data = yf.download(ticker_symbol, period="50d", interval="1d")
    
    # 이동평균선 계산 (5일선, 20일선)
    data['MA5'] = data['Close'].rolling(window=5).mean()
    data['MA20'] = data['Close'].rolling(window=20).mean()
    
    # 마지막 날과 전날 데이터 추출
    last_row = data.iloc[-1]
    prev_row = data.iloc[-2]
    
    # 골든크로스 조건: 전날(MA5 < MA20) -> 오늘(MA5 > MA20)
    is_golden_cross = (prev_row['MA5'] < prev_row['MA20']) and (last_row['MA5'] > last_row['MA20'])
    
    return {
        "price": round(float(last_row['Close']), 2),
        "ma5": round(float(last_row['MA5']), 2),
        "ma20": round(float(last_row['MA20']), 2),
        "signal": "🔥 매수 신호 (골든크로스)" if is_golden_cross else "대기"
    }

# 2. 결과 리포트 생성
report_content = f"## 📈 주식/코인 골든크로스 리포트 ({datetime.now().strftime('%Y-%m-%d %H:%M')})\n\n"
report_content += "| 종목명 | 현재가 | 5일 이평선 | 20일 이평선 | 신호 |\n| :--- | :--- | :--- | :--- | :--- |\n"

for name, symbol in tickers.items():
    try:
        result = check_golden_cross(symbol)
        report_content += f"| {name} | {result['price']} | {result['ma5']} | {result['ma20']} | {result['signal']} |\n"
    except Exception as e:
        print(f"{name} 분석 중 오류 발생: {e}")

# 3. README.md 업데이트
with open("README.md", "w", encoding="utf-8") as f:
    f.write(report_content)

print("리포트 업데이트 완료!")