"""
智农云 · 农业管理平台  —  后端 API (Flask)
钱包模块: 5.3.1.1 ~ 5.3.1.5
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# ─────────────────────────────────────────────────────────────
# 内存数据库 (演示用，可替换为 SQLite / PostgreSQL)
# ─────────────────────────────────────────────────────────────
_id_counter = [20]


def _next_id():
    _id_counter[0] += 1
    return _id_counter[0]


_wallet = {
    "balance": 5800.00,
    "accounts": [
        {
            "id": 1,
            "type": "corporate",
            "icon": "🏢",
            "label": "对公银行卡",
            "name": "华东农业科技有限公司",
            "bank_name": "建设银行",
            "card_no": "**** **** **** 8888",
            "tag": "对公",
        },
        {
            "id": 2,
            "type": "personal",
            "icon": "💳",
            "label": "个人银行卡",
            "name": "王大明",
            "bank_name": "农业银行",
            "card_no": "**** **** **** 6688",
            "tag": "个人",
        },
    ],
    "transactions": [
        {"id": 1,  "type": "income",   "time": "2024-01-15 14:32", "label": "订单收入", "ref": "ORD202401150012", "amount":  4380.00, "status": "success"},
        {"id": 2,  "type": "withdraw", "time": "2024-01-14 09:15", "label": "提现",     "ref": "建设银行 8888",    "amount": -1000.00, "status": "success"},
        {"id": 3,  "type": "income",   "time": "2024-01-12 16:48", "label": "订单收入", "ref": "ORD202401120008", "amount":  2560.00, "status": "success"},
        {"id": 4,  "type": "withdraw", "time": "2024-01-10 10:20", "label": "提现",     "ref": "农业银行 6688",    "amount": -3000.00, "status": "processing"},
        {"id": 5,  "type": "income",   "time": "2024-01-08 11:05", "label": "订单收入", "ref": "ORD202401080003", "amount":  1980.00, "status": "success"},
        {"id": 6,  "type": "income",   "time": "2024-01-05 09:33", "label": "订单收入", "ref": "ORD202401050001", "amount":  3200.00, "status": "success"},
        {"id": 7,  "type": "withdraw", "time": "2023-12-28 14:10", "label": "提现",     "ref": "微信支付",          "amount": -2000.00, "status": "success"},
        {"id": 8,  "type": "income",   "time": "2023-12-22 08:55", "label": "订单收入", "ref": "ORD202312220020", "amount":  5100.00, "status": "success"},
    ],
}

_ICON_MAP  = {"corporate": "🏢", "personal": "💳", "wechat": "💚", "alipay": "🔵"}
_TAG_MAP   = {"corporate": "对公", "personal": "个人", "wechat": "微信", "alipay": "支付宝"}
_LABEL_MAP = {"corporate": "对公银行卡", "personal": "个人银行卡", "wechat": "微信支付", "alipay": "支付宝"}


# ─────────────────────────────────────────────────────────────
# 辅助
# ─────────────────────────────────────────────────────────────
def _ok(data, status=200):
    return jsonify(data), status


def _err(msg, status=400):
    return jsonify({"error": msg}), status


# ─────────────────────────────────────────────────────────────
# 5.3.1.1  钱包首页 — 汇总接口
# ─────────────────────────────────────────────────────────────
@app.route("/api/wallet/summary", methods=["GET"])
def wallet_summary():
    """返回余额、最近3条明细、绑定账户列表"""
    return _ok({
        "balance": _wallet["balance"],
        "accounts": _wallet["accounts"],
        "recent_transactions": _wallet["transactions"][:3],
    })


# ─────────────────────────────────────────────────────────────
# 5.3.1.2 / 5.3.1.3  收款账户管理
# ─────────────────────────────────────────────────────────────
@app.route("/api/wallet/accounts", methods=["GET"])
def list_accounts():
    return _ok(_wallet["accounts"])


@app.route("/api/wallet/accounts", methods=["POST"])
def create_account():
    """新增收款账户（银行卡 / 微信 / 支付宝）"""
    data = request.get_json() or {}
    acct_type = data.get("type", "").strip()
    if acct_type not in _ICON_MAP:
        return _err("无效的账户类型，支持：corporate / personal / wechat / alipay")

    # 微信/支付宝同类型只保留一个
    if acct_type in ("wechat", "alipay"):
        _wallet["accounts"] = [a for a in _wallet["accounts"] if a["type"] != acct_type]

    card_raw = (data.get("card_no") or "").replace(" ", "")
    masked   = ("**** **** **** " + card_raw[-4:]) if len(card_raw) >= 4 else card_raw

    new_acct = {
        "id":        _next_id(),
        "type":      acct_type,
        "icon":      _ICON_MAP[acct_type],
        "label":     _LABEL_MAP[acct_type],
        "name":      data.get("name", ""),
        "bank_name": data.get("bank_name", ""),
        "card_no":   masked or data.get("card_no", ""),
        "tag":       _TAG_MAP[acct_type],
    }
    _wallet["accounts"].append(new_acct)
    return _ok(new_acct, 201)


@app.route("/api/wallet/accounts/<int:account_id>", methods=["PUT"])
def update_account(account_id):
    """更换收款账户信息"""
    acct = next((a for a in _wallet["accounts"] if a["id"] == account_id), None)
    if not acct:
        return _err("账户不存在", 404)

    data = request.get_json() or {}
    card_raw = (data.get("card_no") or "").replace(" ", "")
    if card_raw:
        data["card_no"] = ("**** **** **** " + card_raw[-4:]) if len(card_raw) >= 4 else card_raw

    for key in ("name", "bank_name", "card_no"):
        if key in data:
            acct[key] = data[key]
    return _ok(acct)


@app.route("/api/wallet/accounts/<int:account_id>", methods=["DELETE"])
def delete_account(account_id):
    before = len(_wallet["accounts"])
    _wallet["accounts"] = [a for a in _wallet["accounts"] if a["id"] != account_id]
    if len(_wallet["accounts"]) == before:
        return _err("账户不存在", 404)
    return _ok({"message": "账户已删除"})


# ─────────────────────────────────────────────────────────────
# 5.3.1.4  收支明细列表（分页 + 筛选）
# ─────────────────────────────────────────────────────────────
@app.route("/api/wallet/transactions", methods=["GET"])
def list_transactions():
    tx_type   = request.args.get("type", "all")
    page      = max(1, int(request.args.get("page", 1)))
    page_size = min(50, max(1, int(request.args.get("page_size", 20))))

    txs = _wallet["transactions"]
    if tx_type != "all":
        txs = [t for t in txs if t["type"] == tx_type]

    total = len(txs)
    start = (page - 1) * page_size
    items = txs[start: start + page_size]

    return _ok({
        "list":      items,
        "total":     total,
        "page":      page,
        "page_size": page_size,
        "has_more":  start + page_size < total,
    })


# ─────────────────────────────────────────────────────────────
# 5.3.1.5  提现
# ─────────────────────────────────────────────────────────────
@app.route("/api/wallet/withdraw", methods=["POST"])
def submit_withdraw():
    data = request.get_json() or {}

    try:
        amount = round(float(data.get("amount", 0)), 2)
    except (TypeError, ValueError):
        return _err("金额格式错误")

    account_id = data.get("account_id")

    if amount <= 0:
        return _err("提现金额必须大于 0")
    if amount > _wallet["balance"]:
        return _err("余额不足，提现金额不能超过可提现余额")
    if not account_id:
        return _err("请选择收款账户")

    acct = next((a for a in _wallet["accounts"] if a["id"] == account_id), None)
    if not acct:
        return _err("收款账户不存在")

    ref = acct["name"] if acct["type"] in ("wechat", "alipay") \
        else f"{acct['bank_name']} {acct['card_no'][-4:]}"

    new_tx = {
        "id":     _next_id(),
        "type":   "withdraw",
        "time":   datetime.now().strftime("%Y-%m-%d %H:%M"),
        "label":  "提现",
        "ref":    ref,
        "amount": -amount,
        "status": "processing",
    }
    _wallet["transactions"].insert(0, new_tx)
    _wallet["balance"] = round(_wallet["balance"] - amount, 2)

    return _ok({
        "message":     "提现申请已提交，预计 1–3 个工作日到账",
        "new_balance": _wallet["balance"],
        "transaction": new_tx,
    })


# ─────────────────────────────────────────────────────────────
# 短信验证码（模拟）
# ─────────────────────────────────────────────────────────────
@app.route("/api/auth/send-sms", methods=["POST"])
def send_sms():
    data  = request.get_json() or {}
    phone = (data.get("phone") or "").strip()
    if len(phone) != 11 or not phone.isdigit():
        return _err("请输入正确的 11 位手机号")
    return _ok({"message": f"验证码已发送至 {phone}"})


# ─────────────────────────────────────────────────────────────
# 健康检查
# ─────────────────────────────────────────────────────────────
@app.route("/api/ping", methods=["GET"])
def ping():
    return _ok({"status": "ok", "service": "智农云-钱包API"})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
