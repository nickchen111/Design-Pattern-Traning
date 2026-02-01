# Matchmaking Service (Models Only)

這是一個以 FastAPI 為基礎的簡易專案骨架，目的僅為根據 OOA 圖建立類別（只定義屬性與驗證），不包含類別間的操作實作。

快速上手：

1. 建議建立虛擬環境並安裝依賴：

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. 執行示範程式：

```bash
python matchmaking_service/demo_run.py
```

3. 如果想啟動 FastAPI（目前僅提供根路由）：

```bash
uvicorn matchmaking_service.main:app --reload
```

檔案位置：
- `app/models/`：三個主要類別的定義檔案。
- `demo_run.py`：快速示範實例建立。
