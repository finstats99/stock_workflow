import yfinance as yf
import pandas as pd
from datetime import datetime

# 1. 한국 주식 종목 리스트 (티커 뒤에 .KS 또는 .KQ 필수)
tickers = {
    "삼성전자": "005930.KS",
    "SK하이닉스": "000660.KS",
    "NAVER": "035420.KS",
    "카카오": "035720.KS",
    "에코프로": "086520.KQ",
    "현대차": "005380.KS"
}

def check_golden_cross(ticker_symbol):
    # 최신 버전 yfinance의 데이터 구조 문제를 방지하기 위해 multi_level_index=False 추가
    data = yf.download(ticker_symbol, period="60d", interval="1d", multi_level_index=False)
    
    if data.empty or len(data) < 25:
        return None
    
    # 이동평균선 계산
    data['MA5'] = data['Close'].rolling(window=5).mean()
    data['MA20'] = data['Close'].rolling(window=20).mean()
    
    # 마지막 행과 전날 행 데이터 추출 (안전하게 .iloc 활용)
    last_row = data.iloc[-1]
    prev_row = data.iloc[-2]
    
    # NaN 값이 있는지 확인 (상장 직후 종목 등)
    if pd.isna(last_row['MA5']) or pd.isna(last_row['MA20']):
        return None

    # 골든크로스 판별 로직
    is_golden_cross = (prev_row['MA5'] < prev_row['MA20']) and (last_row['MA5'] > last_row['MA20'])
    
    return {
        "price": int(last_row['Close']), # 한국 주식은 소수점이 없으므로 int 형변환
        "ma5": int(last_row['MA5']),
        "ma20": int(last_row['MA20']),
        "signal": "🔥 매수 신호" if is_golden_cross else "대기"
    }

# 2. 결과 리포트 생성 (한국 시간 표시를 위해 +9시간 처리는 Actions 설정에서 하는 것이 좋음)
report_content = f"## 📈 국장 골든크로스 리포트 ({datetime.now().strftime('%Y-%m-%d %H:%M')})\n\n"
report_content += "| 종목명 | 현재가 | 5일 이평선 | 20일 이평선 | 신호 |\n| :--- | :--- | :--- | :--- | :--- |\n"

for name, symbol in tickers.items():
    try:
        result = check_golden_cross(symbol)
        if result:
            report_content += f"| {name} | {result['price']:,}원 | {result['ma5']:,}원 | {result['ma20']:,}원 | {result['signal']} |\n"
        else:
            report_content += f"| {name} | - | - | - | 데이터 부족 |\n"
    except Exception as e:
        print(f"{name}({symbol}) 분석 중 오류 발생: {e}")

# 3. README.md 업데이트
with open("README.md", "w", encoding="utf-8") as f:
    f.write(report_content)

print("리포트 업데이트 완료!")