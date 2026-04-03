# AI 對沖基金

這是一個 AI 驅動對沖基金的概念驗證專案。本專案旨在探索使用 AI 進行交易決策，僅供**教育目的**使用，不適用於實際交易或投資。

本系統由多個 Agent 協同運作：

1. **Aswath Damodaran Agent** - 估值學院院長，專注於故事、數字與嚴謹的估值方法
2. **Ben Graham Agent** - 價值投資教父，只買具有安全邊際的隱藏寶石
3. **Bill Ackman Agent** - 積極股東投資人，採取大膽立場並推動企業變革
4. **Cathie Wood Agent** - 成長投資女王，相信創新與顛覆的力量
5. **Charlie Munger Agent** - 巴菲特的合夥人，以合理價格只買優秀企業
6. **Michael Burry Agent** - 《大空頭》逆向投資者，專獵深度價值標的
7. **Mohnish Pabrai Agent** - Dhandho 投資人，以低風險尋找翻倍機會
8. **Peter Lynch Agent** - 務實投資人，在日常生活中尋找「十倍股」
9. **Phil Fisher Agent** - 嚴謹的成長投資人，善用深度「閒聊」調查法
10. **Rakesh Jhunjhunwala Agent** - 印度股市大牛
11. **Stanley Druckenmiller Agent** - 宏觀投資傳奇，專獵具成長潛力的不對稱機會
12. **Warren Buffett Agent** - 奧馬哈先知，以合理價格尋找優秀企業
13. **估值 Agent** - 計算股票內在價值並產生交易訊號
14. **情緒 Agent** - 分析市場情緒並產生交易訊號
15. **基本面 Agent** - 分析基本面數據並產生交易訊號
16. **技術面 Agent** - 分析技術指標並產生交易訊號
17. **風險管理員** - 計算風險指標並設定持倉限制
18. **投資組合經理** - 做出最終交易決策並產生訂單

<img width="1042" alt="Screenshot 2025-03-22 at 6 19 07 PM" src="https://github.com/user-attachments/assets/cbae3dcf-b571-490d-b0ad-3f0f035ac0d4" />

注意：本系統不會實際執行任何交易。

[![Twitter Follow](https://img.shields.io/twitter/follow/virattt?style=social)](https://twitter.com/virattt)

## 免責聲明

本專案**僅供教育與研究目的**。

- 不適用於實際交易或投資
- 不提供投資建議或任何保證
- 創作者對任何財務損失不承擔責任
- 投資決策請諮詢專業財務顧問
- 過去的績效不代表未來的結果

使用本軟體即表示您同意僅將其用於學習目的。

## 目錄
- [安裝方式](#安裝方式)
- [執行方式](#執行方式)
  - [⌨️ 命令列介面](#️-命令列介面)
  - [🖥️ 網頁應用程式](#️-網頁應用程式)
- [如何貢獻](#如何貢獻)
- [功能請求](#功能請求)
- [授權條款](#授權條款)

## 安裝方式

在執行 AI 對沖基金之前，您需要先安裝並設定 API 金鑰。以下步驟適用於網頁應用程式與命令列介面。

### 1. 複製儲存庫

```bash
git clone https://github.com/virattt/ai-hedge-fund.git
cd ai-hedge-fund
```

### 2. 設定 API 金鑰

建立 `.env` 檔案以儲存您的 API 金鑰：
```bash
# 在根目錄建立 .env 檔案
cp .env.example .env
```

開啟並編輯 `.env` 檔案，填入您的 API 金鑰：
```bash
# 使用 OpenAI 託管的 LLM（gpt-4o、gpt-4o-mini 等）
OPENAI_API_KEY=your-openai-api-key

# 取得財務數據以驅動對沖基金
FINANCIAL_DATASETS_API_KEY=your-financial-datasets-api-key
```

**重要**：您至少需要設定一個 LLM API 金鑰（例如 `OPENAI_API_KEY`、`GROQ_API_KEY`、`ANTHROPIC_API_KEY` 或 `DEEPSEEK_API_KEY`）才能讓對沖基金正常運作。

**財務數據**：AAPL、GOOGL、MSFT、NVDA 和 TSLA 的數據免費提供，無需 API 金鑰。若需查詢其他股票代碼，請在 `.env` 檔案中設定 `FINANCIAL_DATASETS_API_KEY`。

## 執行方式

### ⌨️ 命令列介面

您可以直接透過終端機執行 AI 對沖基金。此方式提供更細緻的控制，適合自動化、腳本編寫及整合用途。

<img width="992" alt="Screenshot 2025-01-06 at 5 50 17 PM" src="https://github.com/user-attachments/assets/e8ca04bf-9989-4a7d-a8b4-34e04666663b" />

#### 快速開始

1. 安裝 Poetry（若尚未安裝）：

**macOS / Linux：**
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

**Windows（PowerShell）：**
```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

> **注意**：Windows 環境中 `curl` 是 `Invoke-WebRequest` 的別名，不支援 `-sSL` 旗標，請使用上方的 PowerShell 指令。或者，也可透過 pip 安裝：
> ```powershell
> pip install poetry
> ```

2. 安裝相依套件：
```bash
poetry install
```

#### 執行 AI 對沖基金

**最快上手（推薦）：**

使用 `--core` 旗標，自動載入 9 位精選分析師 + 預設模型（llama-3.3-70b-versatile），無需互動選單：

```bash
poetry run python src/main.py --tickers AAPL --core
```

**免費股票代碼**：`AAPL`、`GOOGL`、`MSFT`、`NVDA`、`TSLA` 無需 API 金鑰。

---

**完整指令說明：**

| 旗標 | 說明 | 範例 |
|------|------|------|
| `--tickers` | 股票代碼（逗號分隔） | `--tickers AAPL,MSFT,NVDA` |
| `--core` | 精選 9 位核心分析師，使用預設模型，無互動選單 | `--core` |
| `--analysts-all` | 使用全部分析師 | `--analysts-all` |
| `--analysts` | 指定特定分析師 | `--analysts warren_buffett,valuation_analyst` |
| `--model` | 指定 LLM 模型 | `--model llama-3.3-70b-versatile` |
| `--start-date` | 分析起始日期 | `--start-date 2024-01-01` |
| `--end-date` | 分析結束日期 | `--end-date 2024-03-31` |
| `--show-reasoning` | 顯示每位分析師的推理過程 | `--show-reasoning` |
| `--ollama` | 使用本地 Ollama 模型 | `--ollama` |

**`--core` 精選分析師清單：**

| 分析師 | 投資風格 |
|--------|----------|
| Aswath Damodaran | 學術 DCF 估值 |
| Nassim Taleb | 尾部風險 / 反脆弱 |
| Stanley Druckenmiller | 動量 + 宏觀 |
| Michael Burry | 深度逆向價值 |
| Mohnish Pabrai | 下行保護 |
| Peter Lynch | GARP 成長 |
| Warren Buffett | 護城河價值 |
| Valuation Analyst | 四方法集成估值 |
| Technical Analyst | 純技術分析 |

**常用指令範例：**

```bash
# 精選分析師，分析 AAPL（最推薦）
poetry run python src/main.py --tickers AAPL,GOOGL,MSFT,NVDA,TSLA  --core

# 指定日期區間
poetry run python src/main.py --tickers AAPL --core --start-date 2024-01-01 --end-date 2024-03-31

# 同時分析多支股票
poetry run python src/main.py --tickers AAPL,MSFT,NVDA --core

# 指定特定分析師
poetry run python src/main.py --tickers AAPL --analysts warren_buffett,valuation_analyst --model llama-3.3-70b-versatile

# 顯示推理過程
poetry run python src/main.py --tickers AAPL --core --show-reasoning
```

您也可以加上 `--ollama` 旗標，使用本地 LLM 執行：

```bash
poetry run python src/main.py --tickers AAPL,MSFT,NVDA --ollama
```

#### 執行回測器
```bash
poetry run python src/backtester.py --ticker AAPL,MSFT,NVDA
```

**範例輸出：**
<img width="941" alt="Screenshot 2025-01-06 at 5 47 52 PM" src="https://github.com/user-attachments/assets/00e794ea-8628-44e6-9a84-8f8a31ad3b47" />

注意：`--ollama`、`--start-date` 和 `--end-date` 旗標同樣適用於回測器！

### 🖥️ 網頁應用程式

提供圖形化介面，適合不熟悉命令列的使用者。

<img width="1721" alt="Screenshot 2025-06-28 at 6 41 03 PM" src="https://github.com/user-attachments/assets/b95ab696-c9f4-416c-9ad1-51feb1f5374b" />

#### 快速啟動

**Windows（PowerShell）：**
```powershell
cd app
.\run.bat
```

**macOS / Linux：**
```bash
cd app
./run.sh
```

啟動後自動開啟瀏覽器，或手動開啟：
- 網頁介面：http://localhost:5173
- 後端 API：http://localhost:8000
- API 文件：http://localhost:8000/docs

> **前置需求**：[Node.js](https://nodejs.org/)、Python 3、Poetry

---

#### 手動啟動（開發者）

開兩個終端機分別執行：

**終端機 1 — 後端：**
```bash
cd app/backend
poetry run uvicorn main:app --reload
```

**終端機 2 — 前端：**
```bash
cd app/frontend
npm install
npm run dev
```

---

#### 常見問題

| 問題 | 解決方式 |
|------|----------|
| `Command not found: uvicorn` | `cd app/backend && poetry install` |
| Python 版本問題 | 建議使用 Python 3.11，3.13+ 可能有相容性問題 |
| Port 已被佔用 | `pkill -f "uvicorn\|vite"` 或修改 port 設定 |
| 找不到 `.env` | `cp .env.example .env` 並填入 API 金鑰 |

## 如何貢獻

1. Fork 此儲存庫
2. 建立功能分支
3. 提交您的變更
4. 推送至分支
5. 建立 Pull Request

**重要**：請保持 Pull Request 小而專注，這樣更容易審查與合併。

## 功能請求

如果您有功能請求，請開啟一個 [issue](https://github.com/virattt/ai-hedge-fund/issues) 並標記 `enhancement` 標籤。

## 授權條款

本專案採用 MIT 授權條款 - 詳情請參閱 LICENSE 檔案。
