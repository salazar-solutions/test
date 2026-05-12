#!/usr/bin/env python3
import argparse
import json
import sys
import time
import os
from datetime import datetime, timezone
from pathlib import Path

try:
    import requests
except ImportError:
    print("ERROR: 'requests' package required. Install with: pip install requests")
    sys.exit(1)

BASE_URL = "https://api.binance.com"
EXCLUDE_BASE = ["USDC", "FDUSD", "TUSD", "BUSD", "DAI", "USDP", "USD1", "XUSD", "EUR", "GBP", "AUD", "BRL", "TRY", "PAXG", "XAUT"]

# Tier thresholds based on collateral rate
COLLATERAL_TIER_THRESHOLDS = [(1, 0.95), (2, 0.80), (3, 0.65), (4, 0.50), (5, 0.00)]


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--min-adv", type=float, default=1_000_000)
    p.add_argument("--max-tier", type=int, default=5)
    p.add_argument("--output", type=str, default=None)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--show-rates", action="store_true")
    return p.parse_args()


def api_get(endpoint, params=None, retries=3):
    url = f"{BASE_URL}{endpoint}"
    
    headers = {}
    /sapi/ endpoints require API key (even if MARKET_DATA)
    if "/sapi/" in endpoint:
        api_key = os.getenv("BINANCE_API_KEY")
        if not api_key:
            print("ERROR: Please set BINANCE_API_KEY environment variable")
            print("Example: export BINANCE_API_KEY=your_key_here")
            sys.exit(1)
        headers["X-MBX-APIKEY"] = api_key


    for attempt in range(retries):
        try:
            resp = requests.get(url, headers=headers, params=params, timeout=30)
            
            if resp.status_code == 429:
                print(f"Rate limited, waiting... (attempt {attempt+1})")
                time.sleep(3 ** attempt + 2)
                continue
                
            resp.raise_for_status()
            return resp.json()
            
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error {resp.status_code} for {endpoint}:")
            print(resp.text)
            if attempt == retries - 1:
                raise
            time.sleep(3 ** attempt)
        except Exception as e:
            print(f"Error: {e}")
            if attempt == retries - 1:
                raise
            time.sleep(3 ** attempt)
    return None


def assign_tier(rate):
    for tier, threshold in COLLATERAL_TIER_THRESHOLDS:
        if rate >= threshold:
            return tier
    return 5


def main():
    args = parse_args()
    out_path = Path(args.output) if args.output else Path(__file__).resolve().parent.parent / "tradeable_coins.json"

    print("Fetching data from Binance...")

    # Get exchange info
    ex_info = api_get("/api/v3/exchangeInfo")
    if not ex_info:
        print("Failed to fetch exchangeInfo")
        sys.exit(1)

    valid = {
        s["symbol"] for s in ex_info["symbols"]
        if s["status"] == "TRADING"
        and s["quoteAsset"] == "USDT"
        and s.get("isSpotTradingAllowed", False)
        and s["baseAsset"] not in EXCLUDE_BASE
    }

    # Get 24h tickers and collateral rates
    tickers = api_get("/api/v3/ticker/24hr")
    collateral = api_get("/sapi/v1/portfolio/collateralRate")

    if not tickers or not collateral:
        print("Failed to fetch required data")
        sys.exit(1)

    c_map = {e["asset"]: float(e["collateralRate"]) for e in collateral if isinstance(collateral, list)}

    if args.show_rates:
        data = sorted([
            (t["symbol"].replace("USDT", ""), 
             c_map.get(t["symbol"].replace("USDT", ""), 0), 
             float(t["quoteVolume"]))
            for t in tickers 
            if t["symbol"] in valid and float(t["quoteVolume"]) >= args.min_adv
        ], key=lambda x: -x[1])
        
        print(f"{'Symbol':<10} {'Rate':>8} {'24h Volume':>15}")
        print("-" * 40)
        for s, r, v in data[:50]:  # Show top 50
            print(f"{s:<10} {r:>8.4f} {v:>15,.0f}")
        return

    # Main processing
    assets, no_c = [], []
    for t in tickers:
        sym = t["symbol"]
        if sym not in valid:
            continue
        vol = float(t["quoteVolume"])
        if vol < args.min_adv:
            continue
            
        base = sym.replace("USDT", "")
        rate = c_map.get(base, -1)
        
        if rate < 0:
            no_c.append(base)
            tier = 5
        else:
            tier = assign_tier(rate)
            
        if tier <= args.max_tier:
            assets.append({
                "symbol": base,
                "tier": tier,
                "collateral_rate": round(rate, 4) if rate >= 0 else None,
                "volume_24h": round(vol, 2),
                "price": round(float(t["lastPrice"]), 6)
            })

    assets.sort(key=lambda a: (a["tier"], -a["volume_24h"]))

    by_tier = {}
    for a in assets:
        by_tier.setdefault(f"tier_{a['tier']}", []).append(a["symbol"])

    res = {
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "source": "binance",
        "min_adv": args.min_adv,
        "total": len(assets),
        "by_tier": by_tier,
        "assets": assets
    }

    if args.dry_run:
        print(f"Dry run: {len(assets)} assets found.")
    else:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(res, indent=2))
        print(f"✅ Saved {len(assets)} assets to {out_path}")


if __name__ == "__main__":
    main()