import yfinance as yf
import pandas as pd
from datetime import datetime

# 1. 한국 주식 종목 리스트
tickers = {
    "삼성전자": "005930.KS",
    "SK하이닉스": "000660.KS",
    "NAVER": "035420.KS",
    "카카오": "035720.KS",
    "에코프로": "086520.KQ",
    "현대차": "005380.KS"
}

def check_golden_cross(ticker_symbol):
    data = yf.download(ticker_symbol, period="60d", interval="1d", multi_level_index=False)
    
    if data.empty or len(data) < 25:
        return None
    
    data['MA5'] = data['Close'].rolling(window=5).mean()
    data['MA20'] = data['Close'].rolling(window=20).mean()
    
    last_row = data.iloc[-1]
    prev_row = data.iloc[-2]
    
    if pd.isna(last_row['MA5']) or pd.isna(last_row['MA20']):
        return None

    is_golden_cross = (prev_row['MA5'] < prev_row['MA20']) and (last_row['MA5'] > last_row['MA20'])
    
    return {
        "price": int(last_row['Close']),
        "ma5": int(last_row['MA5']),
        "ma20": int(last_row['MA20']),
        "signal": "🔥 매수 신호" if is_golden_cross else "대기"
    }

# 2. 결과 리포트 생성 (상단)
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
        print(f"{name} 분석 중 오류: {e}")

# 3. 리포트 하단에 신호 설명 추가
report_content += "\n---\n"
report_content += "### 🔍 신호 가이드\n"
report_content += "* **🔥 매수 신호 (골든크로스)**: 단기 이동평균선(5일)이 장기 이동평균선(20일)을 아래에서 위로 뚫고 올라갔을 때 나타납니다. 향후 상승 추세로의 전환 가능성을 의미합니다.\n"
report_content += "* **대기**: 아직 뚜렷한 상승 신호가 포착되지 않은 상태입니다.\n"
report_content += "\n> **주의**: 본 리포트는 기술적 분석 결과일 뿐이며, 투자의 책임은 본인에게 있습니다.\n"

# 4. README.md 업데이트
with open("README.md", "w", encoding="utf-8") as f:
    f.write(report_content)

print("설명이 포함된 리포트 업데이트 완료!")