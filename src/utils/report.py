"""Generate terminal-style tabbed HTML report from hedge fund results."""

import io
import os
from datetime import datetime
from contextlib import redirect_stdout

from colorama import Fore, Style
from tabulate import tabulate
from ansi2html import Ansi2HTMLConverter

from .analysts import ANALYST_ORDER


# ── helpers ───────────────────────────────────────────────────────────────

def _init_colorama():
    import colorama
    colorama.deinit()
    colorama.init(strip=False, convert=False)

def _restore_colorama():
    import colorama
    colorama.deinit()
    colorama.init()

def _to_html(ansi_text: str) -> str:
    conv = Ansi2HTMLConverter(dark_bg=True, inline=True, scheme="ansi2html")
    return conv.convert(ansi_text, full=False)

def _capture(fn, *args, **kwargs) -> str:
    buf = io.StringIO()
    with redirect_stdout(buf):
        fn(*args, **kwargs)
    return buf.getvalue()

def _sort_signals(rows):
    order = {d: i for i, (d, _) in enumerate(ANALYST_ORDER)}
    order["Risk Management"] = len(ANALYST_ORDER)
    return sorted(rows, key=lambda x: order.get(x[0], 999))


# ── section printers (return ANSI strings) ────────────────────────────────

def _print_agent_analysis(ticker: str, analyst_signals: dict):
    import json

    table_data = []
    for agent, signals in analyst_signals.items():
        if ticker not in signals or agent == "risk_management_agent":
            continue
        signal = signals[ticker]
        agent_name = agent.replace("_agent", "").replace("_", " ").title()
        signal_type = signal.get("signal", "").upper()
        confidence = signal.get("confidence", 0)

        color = {"BULLISH": Fore.GREEN, "BEARISH": Fore.RED, "NEUTRAL": Fore.YELLOW}.get(signal_type, Fore.WHITE)

        reasoning = signal.get("reasoning", "")
        if isinstance(reasoning, dict):
            reasoning = json.dumps(reasoning, indent=2)
        reasoning = str(reasoning)
        # wrap
        wrapped, line = "", ""
        for w in reasoning.split():
            if len(line) + len(w) + 1 > 60:
                wrapped += line + "\n"; line = w
            else:
                line = (line + " " + w).strip()
        if line:
            wrapped += line

        table_data.append([
            f"{Fore.CYAN}{agent_name}{Style.RESET_ALL}",
            f"{color}{signal_type}{Style.RESET_ALL}",
            f"{Fore.WHITE}{confidence}%{Style.RESET_ALL}",
            f"{Fore.WHITE}{wrapped}{Style.RESET_ALL}",
        ])

    table_data = _sort_signals(table_data)
    print(f"\n{Fore.WHITE}{Style.BRIGHT}AGENT ANALYSIS:{Style.RESET_ALL} [{Fore.CYAN}{ticker}{Style.RESET_ALL}]")
    print(tabulate(
        table_data,
        headers=[f"{Fore.WHITE}Agent", "Signal", "Confidence", "Reasoning"],
        tablefmt="grid",
        colalign=("left", "center", "right", "left"),
    ))


def _print_trading_decision(ticker: str, decision: dict):
    import json
    action = decision.get("action", "").upper()
    color = {"BUY": Fore.GREEN, "COVER": Fore.GREEN, "SELL": Fore.RED, "SHORT": Fore.RED, "HOLD": Fore.YELLOW}.get(action, Fore.WHITE)

    reasoning = decision.get("reasoning", "")
    if isinstance(reasoning, dict):
        reasoning = json.dumps(reasoning, indent=2)
    reasoning = str(reasoning)
    wrapped, line = "", ""
    for w in reasoning.split():
        if len(line) + len(w) + 1 > 60:
            wrapped += line + "\n"; line = w
        else:
            line = (line + " " + w).strip()
    if line:
        wrapped += line

    rows = [
        ["Action",     f"{color}{action}{Style.RESET_ALL}"],
        ["Quantity",   f"{color}{decision.get('quantity')}{Style.RESET_ALL}"],
        ["Confidence", f"{Fore.WHITE}{decision.get('confidence', 0):.1f}%{Style.RESET_ALL}"],
        ["Reasoning",  f"{Fore.WHITE}{wrapped}{Style.RESET_ALL}"],
    ]
    print(f"\n{Fore.WHITE}{Style.BRIGHT}TRADING DECISION:{Style.RESET_ALL} [{Fore.CYAN}{ticker}{Style.RESET_ALL}]")
    print(tabulate(rows, tablefmt="grid", colalign=("left", "left")))


def _print_portfolio_summary(decisions: dict, analyst_signals: dict):
    rows = []
    for ticker, decision in decisions.items():
        action = decision.get("action", "").upper()
        color = {"BUY": Fore.GREEN, "COVER": Fore.GREEN, "SELL": Fore.RED, "SHORT": Fore.RED, "HOLD": Fore.YELLOW}.get(action, Fore.WHITE)
        b = r = n = 0
        for agent, sigs in analyst_signals.items():
            if ticker in sigs:
                s = sigs[ticker].get("signal", "").upper()
                if s == "BULLISH": b += 1
                elif s == "BEARISH": r += 1
                elif s == "NEUTRAL": n += 1
        rows.append([
            f"{Fore.CYAN}{ticker}{Style.RESET_ALL}",
            f"{color}{action}{Style.RESET_ALL}",
            f"{color}{decision.get('quantity')}{Style.RESET_ALL}",
            f"{Fore.WHITE}{decision.get('confidence', 0):.1f}%{Style.RESET_ALL}",
            f"{Fore.GREEN}{b}{Style.RESET_ALL}",
            f"{Fore.RED}{r}{Style.RESET_ALL}",
            f"{Fore.YELLOW}{n}{Style.RESET_ALL}",
        ])

    print(f"\n{Fore.WHITE}{Style.BRIGHT}PORTFOLIO SUMMARY:{Style.RESET_ALL}")
    print(tabulate(
        rows,
        headers=[f"{Fore.WHITE}Ticker", "Action", "Quantity", "Confidence", "Bullish", "Bearish", "Neutral"],
        tablefmt="grid",
        colalign=("left", "center", "right", "right", "center", "center", "center"),
    ))

    # portfolio strategy
    for ticker, decision in decisions.items():
        if decision.get("reasoning"):
            import json
            r = decision["reasoning"]
            if isinstance(r, dict):
                r = json.dumps(r, indent=2)
            print(f"\n{Fore.WHITE}{Style.BRIGHT}Portfolio Strategy:{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{r}{Style.RESET_ALL}")
            break


# ── main export ───────────────────────────────────────────────────────────

def write_trading_output_html(result: dict, output_path: str) -> None:
    decisions = result.get("decisions") or {}
    analyst_signals = result.get("analyst_signals") or {}
    run_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    tickers = list(decisions.keys())

    _init_colorama()

    # Summary section
    summary_html = _to_html(_capture(_print_portfolio_summary, decisions, analyst_signals))

    # Per-ticker sections
    ticker_sections: dict[str, str] = {}
    for ticker in tickers:
        ansi = _capture(_print_agent_analysis, ticker, analyst_signals)
        ansi += _capture(_print_trading_decision, ticker, decisions[ticker])
        ticker_sections[ticker] = _to_html(ansi)

    _restore_colorama()

    # Build tabs HTML
    tab_buttons = ['<button class="tab-btn active" onclick="showTab(event,\'tab-summary\')">📊 Summary</button>']
    tab_panels  = [f'<div id="tab-summary" class="tab-panel active"><pre>{summary_html}</pre></div>']

    for ticker in tickers:
        tid = f"tab-{ticker}"
        tab_buttons.append(f'<button class="tab-btn" onclick="showTab(event,\'{tid}\')">{ticker}</button>')
        tab_panels.append(f'<div id="{tid}" class="tab-panel"><pre>{ticker_sections[ticker]}</pre></div>')

    html = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AI Hedge Fund — {run_date}</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: #0d0d0d;
      color: #f0f0f0;
      font-family: 'Cascadia Code','Fira Code','Consolas','Menlo',monospace;
      font-size: 14px;
    }}
    header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 16px 24px;
      border-bottom: 1px solid #333;
    }}
    header h1 {{ color: #00ffff; font-size: 16px; }}
    header time {{ color: #666; font-size: 12px; }}
    .tabs {{
      display: flex;
      gap: 2px;
      padding: 12px 24px 0;
      border-bottom: 1px solid #333;
      background: #111;
    }}
    .tab-btn {{
      background: #1e1e1e;
      color: #999;
      border: 1px solid #333;
      border-bottom: none;
      padding: 6px 18px;
      cursor: pointer;
      font-family: inherit;
      font-size: 13px;
      border-radius: 4px 4px 0 0;
      transition: color .15s;
    }}
    .tab-btn:hover {{ color: #00ffff; }}
    .tab-btn.active {{ background: #0d0d0d; color: #00ffff; border-color: #444; }}
    .tab-panel {{ display: none; padding: 24px; }}
    .tab-panel.active {{ display: block; }}
    pre {{ white-space: pre; overflow-x: auto; line-height: 1.55; }}
  </style>
</head>
<body>
  <header>
    <h1>📈 AI Hedge Fund Report</h1>
    <time>{run_date}</time>
  </header>
  <div class="tabs">
    {''.join(tab_buttons)}
  </div>
  {''.join(tab_panels)}
  <script>
    function showTab(e, id) {{
      document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      document.getElementById(id).classList.add('active');
      e.currentTarget.classList.add('active');
    }}
  </script>
</body>
</html>
"""

    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\nReport saved → {output_path}")
