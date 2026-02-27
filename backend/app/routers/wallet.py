from fastapi import APIRouter
from pydantic import BaseModel

from app.store import wallet as store_wallet

router = APIRouter()


class AccountAdd(BaseModel):
    type: str
    name: str
    bankName: str = ""
    cardNo: str = ""


class WithdrawRequest(BaseModel):
    amount: float
    accountId: int


@router.get("")
def get_wallet():
    return store_wallet


@router.get("/balance")
def get_balance():
    return {"balance": store_wallet["balance"]}


@router.get("/accounts")
def list_accounts():
    return store_wallet["accounts"]


@router.post("/accounts")
def add_account(acc: AccountAdd):
    new_id = max((a["id"] for a in store_wallet["accounts"]), default=0) + 1
    card_display = f"**** **** **** {acc.cardNo[-4:]}" if len(acc.cardNo) >= 4 else acc.cardNo
    new_acc = {
        "id": new_id,
        "type": acc.type,
        "icon": "🏢" if acc.type == "corporate" else "💳",
        "label": "对公银行卡" if acc.type == "corporate" else "个人银行卡",
        "name": acc.name,
        "bankName": acc.bankName,
        "cardNo": card_display,
        "tag": "对公" if acc.type == "corporate" else "个人",
    }
    store_wallet["accounts"].append(new_acc)
    return {"success": True, "account": new_acc}


@router.get("/transactions")
def list_transactions(type_filter: str = "all"):
    txs = store_wallet["transactions"]
    if type_filter == "all":
        return txs
    return [t for t in txs if t["type"] == type_filter]


@router.post("/withdraw")
def withdraw(req: WithdrawRequest):
    if req.amount <= 0:
        return {"success": False, "message": "请输入提现金额"}
    if req.amount > store_wallet["balance"]:
        return {"success": False, "message": "余额不足"}
    acc = next((a for a in store_wallet["accounts"] if a["id"] == req.accountId), None)
    if not acc:
        return {"success": False, "message": "请选择收款账户"}
    from datetime import datetime
    store_wallet["balance"] = round(store_wallet["balance"] - req.amount, 2)
    new_tx = {
        "id": max((t["id"] for t in store_wallet["transactions"]), default=0) + 1,
        "type": "withdraw",
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "label": "提现",
        "ref": acc.get("bankName", "") + " " + (acc.get("cardNo", "")[-4:] if acc.get("cardNo") else ""),
        "amt": -req.amount,
        "status": "processing",
    }
    store_wallet["transactions"].insert(0, new_tx)
    return {"success": True, "transaction": new_tx}
