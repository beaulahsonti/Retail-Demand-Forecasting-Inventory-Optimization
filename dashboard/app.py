from pathlib import Path
from html import escape

import pandas as pd
import plotly.express as px
import streamlit as st
import streamlit.components.v1 as components


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR = PROJECT_ROOT / "reports"


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Retail Demand Forecasting & Inventory Optimization",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>
        :root {
            --dash-bg: #070b14;
            --dash-panel: #0d1422;
            --dash-panel-2: #111a2a;
            --dash-border: rgba(148, 163, 184, 0.18);
            --dash-text: #f8fafc;
            --dash-muted: #94a3b8;
            --dash-blue: #3b82f6;

            /* ---- KPI CARD GAP TOKENS ----
               Single source of truth for the spacing BETWEEN every
               KPI card (both row-gap and column-gap), tuned per
               breakpoint below. Keeping these as variables means the
               desktop layout/appearance is left exactly as it was —
               only the values used at narrower widths change. */
            --kpi-gap-desktop: 1rem;
            --kpi-gap-tablet: 0.9rem;
            --kpi-gap-mobile: 14px;
            --kpi-gap-xs: 12px;
            --kpi-gap-tiny: 12px;
        }

        /* ================= GLOBAL ================= */
        * , *::before, *::after {
            box-sizing: border-box;
        }

        html, body {
            max-width: 100%;
            overflow-x: hidden;
        }

        .stApp {
            background:
                radial-gradient(circle at 85% 0%, rgba(37, 99, 235, 0.08), transparent 30%),
                radial-gradient(circle at 10% 35%, rgba(124, 58, 237, 0.06), transparent 28%),
                #070b14;
            color: var(--dash-text);
            overflow-x: hidden;
            width: 100%;
        }

        .main .block-container {
            max-width: 1480px;
            width: 100%;
            padding: 1.25rem clamp(0.75rem, 2.5vw, 2.2rem) 3rem;
        }

        /* Hide Streamlit's default menu/deploy decoration where possible. */
        [data-testid="stDecoration"] { display: none; }

        /* ================= TOP HEADER ================= */
        .topbar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            row-gap: 0.5rem;
            gap: 1rem;
            padding: 0.7rem 0 1rem;
            border-bottom: 1px solid rgba(148, 163, 184, 0.12);
            margin-bottom: 1.5rem;
            width: 100%;
            max-width: 100%;
            box-sizing: border-box;
        }

        .brand-title {
            display: flex;
            align-items: center;
            gap: 0.7rem;
            color: #f8fafc;
            font-size: clamp(0.92rem, 2.4vw, 1.25rem);
            font-weight: 800;
            letter-spacing: -0.02em;
            min-width: 0;
            flex: 1 1 220px;
            overflow-wrap: break-word;
        }

        .brand-mark {
            width: 34px;
            height: 34px;
            flex-shrink: 0;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border-radius: 10px;
            background: linear-gradient(135deg, #2563eb, #7c3aed);
            box-shadow: 0 8px 20px rgba(37, 99, 235, 0.28);
            font-size: 1rem;
        }

        .live-pill {
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            padding: 0.42rem 0.8rem;
            border: 1px solid rgba(16, 185, 129, 0.45);
            border-radius: 999px;
            color: #6ee7b7;
            background: rgba(6, 78, 59, 0.25);
            font-size: 0.78rem;
            font-weight: 750;
            flex-shrink: 0;
            white-space: nowrap;
        }

        .live-dot {
            width: 7px;
            height: 7px;
            flex-shrink: 0;
            border-radius: 50%;
            background: #34d399;
            box-shadow: 0 0 12px rgba(52, 211, 153, 0.8);
        }

        .page-heading {
            color: #f8fafc !important;
            font-size: clamp(1.65rem, 4vw, 2.55rem) !important;
            line-height: 1.1;
            font-weight: 850 !important;
            letter-spacing: -0.04em;
            margin: 0 0 0.35rem;
        }

        .page-heading .accent { color: #4f8cff; }

        .page-subtitle {
            color: #94a3b8 !important;
            font-size: clamp(0.88rem, 1.5vw, 1rem);
            line-height: 1.55;
            margin-bottom: 1.25rem;
        }

        /* ================= SIDEBAR ================= */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0d1729 0%, #0a1220 100%);
            border-right: 1px solid rgba(148, 163, 184, 0.14);
        }

        section[data-testid="stSidebar"] > div {
            padding-top: 1rem;
        }

        .side-brand {
            display: flex;
            gap: 0.7rem;
            align-items: center;
            padding: 0.45rem 0.35rem 1rem;
            border-bottom: 1px solid rgba(148, 163, 184, 0.11);
            margin-bottom: 0.85rem;
        }

        .side-logo {
            width: 42px;
            height: 42px;
            flex: 0 0 42px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 11px;
            background: linear-gradient(135deg, #2563eb, #3b82f6);
            box-shadow: 0 8px 20px rgba(37, 99, 235, 0.25);
            font-size: 1.2rem;
        }

        .side-title {
            color: #f8fafc;
            font-size: 1rem;
            font-weight: 800;
            line-height: 1.15;
        }

        .side-subtitle {
            color: #94a3b8;
            font-size: 0.7rem;
            line-height: 1.35;
            margin-top: 0.25rem;
        }

        section[data-testid="stSidebar"] [data-testid="stRadio"] > label {
            color: #64748b !important;
            font-size: 0.68rem !important;
            font-weight: 800 !important;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 0.35rem;
        }

        section[data-testid="stSidebar"] [data-testid="stRadio"] label {
            border-radius: 10px;
            padding: 0.62rem 0.65rem;
            margin: 0.12rem 0;
            color: #cbd5e1 !important;
            transition: all 0.16s ease;
        }

        section[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
            background: rgba(59, 130, 246, 0.10);
            transform: translateX(2px);
        }

        section[data-testid="stSidebar"] [data-testid="stRadio"] p {
            font-weight: 650 !important;
        }

        .side-footer {
            color: #64748b;
            font-size: 0.68rem;
            line-height: 1.5;
            margin-top: 1.2rem;
            padding-top: 0.9rem;
            border-top: 1px solid rgba(148, 163, 184, 0.1);
        }

        .side-info {
            margin-top: 1rem;
            padding: 0.85rem;
            border: 1px solid rgba(96, 165, 250, 0.22);
            border-radius: 12px;
            background: rgba(30, 64, 175, 0.08);
            color: #a5b4fc;
            font-size: 0.72rem;
            line-height: 1.5;
        }

        /* =========================================================
           SIDEBAR TOGGLE ICON — always a 3-line "hamburger", never
           an arrow/chevron.
           IMPORTANT: the icon is hidden with opacity (not
           visibility/display), because visibility:hidden or
           display:none removes an element from click hit-testing —
           that was breaking the toggle. opacity:0 hides it visually
           while keeping the real click target intact underneath the
           ☰ overlay (which itself has pointer-events:none so clicks
           pass straight through to that real target).

           Two separate controls exist: the COLLAPSED rail control
           (shown when the sidebar is hidden) is pinned to the fixed
           top-left corner of the viewport. The EXPANDED sidebar's
           own close button stays docked in its normal spot inside
           the sidebar header — pinning it to the same fixed corner
           would make it overlap the sidebar logo.
           ========================================================= */
        [data-testid*="SidebarCollapsedControl"],
        [data-testid*="CollapsedControl"],
        [data-testid="collapsedControl"],
        [aria-label="Open sidebar"] {
            position: fixed !important;
            top: 14px !important;
            left: 14px !important;
            z-index: 999999 !important;
            border-radius: 10px !important;
            background: rgba(15, 23, 42, 0.92) !important;
            border: 1px solid rgba(148, 163, 184, 0.18) !important;
            overflow: hidden !important;
            min-width: 36px !important;
            min-height: 36px !important;
        }

        [data-testid*="SidebarCollapsedControl"] *,
        [data-testid*="CollapsedControl"] *,
        [data-testid="collapsedControl"] *,
        [aria-label="Open sidebar"] * {
            opacity: 0 !important;
        }

        [data-testid*="SidebarCollapsedControl"]::after,
        [data-testid*="CollapsedControl"]::after,
        [data-testid="collapsedControl"]::after,
        [aria-label="Open sidebar"]::after {
            opacity: 1 !important;
            content: "☰";
            position: absolute;
            inset: 0;
            z-index: 5;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #e2e8f0;
            font-size: 1.15rem;
            line-height: 1;
            pointer-events: none;
        }

        /* Once the sidebar is open, its own close/hamburger control is
           removed entirely — no second toggle icon lingering on top of
           the page. Close the sidebar again by tapping a nav item or
           the rail toggle re-appears once it's collapsed. */
        [data-testid*="SidebarCollapseButton"],
        [aria-label="Close sidebar"] {
            display: none !important;
        }

        /* ================= KPI CARDS ================= */
        .kpi-grid-note { margin-bottom: 0.1rem; }

        /* KPI rows use a real CSS grid rather than depending purely
           on Streamlit's st.columns flex layout — this is what makes
           them reflow correctly at ANY width (desktop, laptop,
           tablet, phone) without needing a matching breakpoint for
           every possible column count. :has() scopes this to rows
           that actually contain KPI cards, so chart/table column
           pairs elsewhere are unaffected and keep their own layout.

           `gap` (plus explicit `row-gap`/`column-gap` as a belt-and-
           braces fallback for older/quirky renderers) is what creates
           real space BETWEEN every card, in both directions at once —
           it is not padding on the row's edges, so cards never touch
           each other regardless of how many end up per line. */
        [data-testid="stHorizontalBlock"]:has(.kpi-card) {
            display: grid !important;
            /*
               Desktop KPI sizing:
               - Five-card rows (Overview) stay on ONE row.
               - Four-card rows (Forecast / Inventory) stay on ONE row.
               - Every card gets equal width.
               - The gap is BETWEEN cards, never only at the outside edge.
            */
            grid-template-columns: repeat(4, minmax(0, 1fr)) !important;
            gap: var(--kpi-gap-desktop) !important;
            row-gap: var(--kpi-gap-desktop) !important;
            column-gap: var(--kpi-gap-desktop) !important;
            width: 100% !important;
            align-items: stretch !important;
        }

        /* Overview has five KPI cards. Keep all five cards on the
           same desktop row instead of wrapping the fifth card. */
        [data-testid="stHorizontalBlock"]:has(.kpi-card):has(> [data-testid="stColumn"]:nth-child(5)) {
            grid-template-columns: repeat(5, minmax(0, 1fr)) !important;
        }

        [data-testid="stHorizontalBlock"]:has(.kpi-card) > [data-testid="stColumn"] {
            width: 100% !important;
            min-width: 0 !important;
            flex: unset !important;
            /* Remove any of Streamlit's own column padding/margin so
               the grid `gap` above is the ONLY source of spacing
               between cards — prevents uneven or collapsed gaps. */
            padding: 0 !important;
            margin: 0 !important;
        }

        [data-testid="stHorizontalBlock"]:has(.kpi-card) > [data-testid="stColumn"] > div {
            margin: 0 !important;
            min-width: 0 !important;
            width: 100% !important;
        }

        /* Streamlit may place an inner wrapper around the HTML card.
           Remove its intrinsic width so the CSS grid controls the card
           size consistently on desktop, tablet and mobile. */
        [data-testid="stHorizontalBlock"]:has(.kpi-card) .stMarkdown,
        [data-testid="stHorizontalBlock"]:has(.kpi-card) .stMarkdownContainer {
            max-width: 100% !important;
            min-width: 0 !important;
            width: 100% !important;
        }

        .kpi-card {
            position: relative;
            min-height: 142px;
            width: 100%;
            min-width: 0;
            padding: 1rem 1rem 0.95rem;
            border-radius: 16px;
            overflow: hidden;
            color: #fff !important;
            border: 1px solid rgba(255,255,255,0.14);
            box-shadow: 0 14px 34px rgba(0,0,0,0.22);
            transition: transform 0.18s ease, box-shadow 0.18s ease;
        }

        /* Hover lift only where a mouse/pointer is actually available —
           avoids a "stuck" hover state on touch devices. */
        @media (hover: hover) and (pointer: fine) {
            .kpi-card:hover {
                transform: translateY(-3px);
                box-shadow: 0 18px 40px rgba(0,0,0,0.28);
            }
        }

        .kpi-card::before {
            content: "";
            position: absolute;
            width: 120px;
            height: 120px;
            right: -45px;
            top: -50px;
            border-radius: 50%;
            background: rgba(255,255,255,0.10);
        }

        .kpi-blue { background: linear-gradient(145deg, #1464d2 0%, #0c2e6e 100%); }
        .kpi-green { background: linear-gradient(145deg, #069669 0%, #064e3b 100%); }
        .kpi-purple { background: linear-gradient(145deg, #7c3aed 0%, #3b176d 100%); }
        .kpi-orange { background: linear-gradient(145deg, #ea6a18 0%, #7c2d12 100%); }
        .kpi-cyan { background: linear-gradient(145deg, #0891b2 0%, #164e63 100%); }

        .kpi-icon {
            position: relative;
            width: 36px;
            height: 36px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border-radius: 11px;
            background: rgba(255,255,255,0.15);
            border: 1px solid rgba(255,255,255,0.14);
            font-size: 1rem;
            margin-bottom: 0.58rem;
            flex-shrink: 0;
        }

        .kpi-label {
            position: relative;
            color: rgba(255,255,255,0.85) !important;
            font-size: clamp(0.72rem, 1.9vw, 0.85rem);
            font-weight: 750;
            text-transform: uppercase;
            letter-spacing: 0.045em;
            line-height: 1.3;
        }

        .kpi-value {
            position: relative;
            color: #fff !important;
            font-size: clamp(1.4rem, 4.6vw, 2.15rem);
            font-weight: 850;
            letter-spacing: -0.025em;
            line-height: 1.15;
            margin-top: 0.2rem;
            word-break: break-word;
        }

        .kpi-helper {
            position: relative;
            color: rgba(255,255,255,0.68) !important;
            font-size: clamp(0.66rem, 1.7vw, 0.78rem);
            margin-top: 0.32rem;
        }

        /* ================= CONTENT PANELS ================= */
        .section-kicker {
            color: #60a5fa;
            font-size: 0.68rem;
            font-weight: 800;
            letter-spacing: 0.09em;
            text-transform: uppercase;
            margin-bottom: 0.2rem;
        }

        .section-title {
            color: #f8fafc;
            font-size: 1.12rem;
            font-weight: 800;
            margin-bottom: 0.2rem;
        }

        .section-subtitle {
            color: #94a3b8;
            font-size: 0.78rem;
            margin-bottom: 0.8rem;
        }

        .insight-card {
            border: 1px solid rgba(96,165,250,0.20);
            background: linear-gradient(145deg, rgba(15, 33, 60, 0.82), rgba(9, 20, 35, 0.88));
            border-radius: 14px;
            padding: 0.9rem 1rem;
            color: #cbd5e1;
            font-size: 0.78rem;
            line-height: 1.55;
        }

        /* ================= TABLES ================= */
        /* Tables scroll horizontally INSIDE their own container at
           every screen size, never the page itself — the page-level
           overflow-x:hidden set in GLOBAL is the outer guarantee,
           this is what actually lets wide tables stay usable. */
        [data-testid="stDataFrame"] {
            width: 100%;
            max-width: 100%;
            border-radius: 12px;
            overflow-x: auto;
        }

        /* ================= CHARTS ================= */
        [data-testid="stPlotlyChart"] {
            width: 100%;
            border: 1px solid rgba(148,163,184,0.13);
            border-radius: 14px;
            background: linear-gradient(145deg, rgba(13,20,34,0.96), rgba(8,14,24,0.96));
            padding: 0.2rem;
            box-shadow: 0 10px 28px rgba(0,0,0,0.13);
        }

        /* ================= GLOBAL FOOTER ================= */
        .dashboard-footer {
            width: 100%;
            max-width: 100%;
            margin-top: 2.4rem;
            padding-top: 1.35rem;
            padding-bottom: 1.2rem;
            border-top: 2px solid rgba(148, 163, 184, 0.38);
            text-align: center;
        }

        .dashboard-footer-insight {
            width: 100%;
            max-width: 100%;
            margin: 0 0 1rem;
            padding: 1rem 1.15rem;
            border: 1px solid rgba(96, 165, 250, 0.22);
            border-radius: 14px;
            background: linear-gradient(145deg, rgba(15, 33, 60, 0.82), rgba(9, 20, 35, 0.88));
            color: #cbd5e1;
            font-size: 0.9rem;
            line-height: 1.55;
            text-align: left;
            box-sizing: border-box;
        }

        .dashboard-footer-title {
            color: #f8fafc;
            font-size: 0.95rem;
            font-weight: 800;
        }

        .dashboard-footer-subtitle {
            color: #a5b4c7;
            font-size: 0.82rem;
            font-weight: 550;
        }

        .dashboard-footer-meta {
            color: #94a3b8;
            font-size: 0.78rem;
            font-weight: 600;
            line-height: 1.5;
            letter-spacing: 0.01em;
        }

        @media (max-width: 767px) {
            .dashboard-footer {
                margin-top: 2rem;
                padding-top: 1.1rem;
                padding-bottom: 1rem;
            }

            .dashboard-footer-insight {
                padding: 0.9rem 0.95rem;
                border-radius: 13px;
                font-size: 0.82rem;
            }

            .dashboard-footer-title {
                font-size: 0.86rem;
            }

            .dashboard-footer-subtitle {
                font-size: 0.74rem;
            }

            .dashboard-footer-meta {
                font-size: 0.68rem;
            }
        }

        /* ================= TABLE / CHART SECTIONS ================= */
        .selection-note {
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            color: #bfdbfe;
            background: rgba(37,99,235,0.10);
            border: 1px solid rgba(96,165,250,0.25);
            border-radius: 999px;
            padding: 0.4rem 0.7rem;
            font-size: 0.72rem;
            font-weight: 650;
            margin: 0.2rem 0 0.55rem;
        }

        /* ================= STREAMLIT WIDGETS ================= */
        div[data-baseweb="select"] > div,
        div[data-baseweb="input"] > div {
            background: #0d1422 !important;
            border-color: rgba(148,163,184,0.22) !important;
        }

        label, [data-testid="stWidgetLabel"] p {
            color: #cbd5e1 !important;
        }

        /* =========================================================
           RESPONSIVE BREAKPOINTS
           desktop  : > 1199px  (no override needed — base styles)
           tablet   : 900px–1199px
           mobile   : 481px–900px
           very small mobile : 361px–480px
           tiny mobile        : <= 360px
           ========================================================= */
        @media (max-width: 1199px) {
            /* Tablet: two balanced KPI cards per row. */
            [data-testid="stHorizontalBlock"]:has(.kpi-card),
            [data-testid="stHorizontalBlock"]:has(.kpi-card):has(> [data-testid="stColumn"]:nth-child(5)) {
                grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
                gap: var(--kpi-gap-tablet) !important;
                row-gap: var(--kpi-gap-tablet) !important;
                column-gap: var(--kpi-gap-tablet) !important;
            }
        }

        @media (max-width: 900px) {
            .main .block-container {
                padding-left: 0.9rem;
                padding-right: 0.9rem;
            }

            .topbar {
                margin-bottom: 1.1rem;
            }
        }

        @media (max-width: 767px) {
            .main .block-container {
                padding: 0.7rem 0.65rem 2.2rem;
            }

            .brand-mark { width: 28px; height: 28px; }
            .live-pill { padding: 0.35rem 0.6rem; }

            .page-heading {
                font-size: 1.55rem !important;
            }

            .page-subtitle {
                font-size: 0.82rem;
            }

            .kpi-card {
                min-height: 126px;
                min-width: 0;
                padding: 0.78rem 0.82rem;
                border-radius: 14px;
            }

            .kpi-icon {
                width: 28px;
                height: 28px;
                font-size: 0.85rem;
                margin-bottom: 0.4rem;
            }

            /* Mobile: a proper 2-column KPI grid (never a squeezed
               4-or-5-across row) — driven by the same CSS grid rule
               above, just with a narrower minimum column so two
               cards comfortably share a row on most phones, all the
               way down to very small screens (see the 480/360px
               breakpoints below for further tuning). Never forced to
               a fixed 1fr — auto-fit is what keeps this from ever
               overflowing at any width. Gap is a fixed 14px here
               (within the requested 12–16px range) so every card —
               left/right AND row-to-row — has a clear, even gap. */
            [data-testid="stHorizontalBlock"]:has(.kpi-card),
            [data-testid="stHorizontalBlock"]:has(.kpi-card):has(> [data-testid="stColumn"]:nth-child(5)) {
                grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
                gap: var(--kpi-gap-mobile) !important;
                row-gap: var(--kpi-gap-mobile) !important;
                column-gap: var(--kpi-gap-mobile) !important;
            }

            /* Non-KPI column rows (chart pairs, etc.) stack full-width
               on mobile for readability — KPI rows are excluded via
               :not() so they keep using the grid rule above instead. */
            [data-testid="stHorizontalBlock"]:not(:has(.kpi-card)) {
                flex-wrap: wrap !important;
                gap: 0.65rem !important;
            }

            [data-testid="stHorizontalBlock"]:not(:has(.kpi-card)) > [data-testid="stColumn"] {
                min-width: 100% !important;
                width: 100% !important;
                flex: 1 1 100% !important;
            }

            [data-testid="stPlotlyChart"] {
                padding: 0;
            }
        }

        @media (max-width: 480px) {
            .main .block-container {
                padding-left: 0.5rem;
                padding-right: 0.5rem;
            }

            .page-heading { font-size: 1.3rem !important; }
            .page-subtitle { font-size: 0.76rem; }

            .kpi-card {
                min-height: 116px;
                min-width: 0;
                padding: 0.68rem 0.72rem;
            }

            .kpi-icon {
                width: 26px;
                height: 26px;
                font-size: 0.8rem;
                margin-bottom: 0.32rem;
            }

            /* Still a 2-up grid — the smaller minmax basis is what
               keeps two cards fitting comfortably down to ~360px
               without ever forcing a fixed column count. Gap is set
               explicitly to 12px here (within the requested 10–14px
               range for very small mobile) so cards stay clearly
               separated in every direction while remaining inside
               the viewport. */
            [data-testid="stHorizontalBlock"]:has(.kpi-card),
            [data-testid="stHorizontalBlock"]:has(.kpi-card):has(> [data-testid="stColumn"]:nth-child(5)) {
                grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
                gap: var(--kpi-gap-xs) !important;
                row-gap: var(--kpi-gap-xs) !important;
                column-gap: var(--kpi-gap-xs) !important;
            }
        }

        /* =========================================================
           FINAL MOBILE KPI RESPONSIVE FIX
           - Always keep 2 KPI cards per row on mobile.
           - Keep a real horizontal gap between the two columns.
           - Keep a guaranteed vertical gap between every KPI row.
           - Do not use height:100% on the cards; that can make
             Streamlit grid rows visually touch on narrow screens.
           ========================================================= */
        [data-testid="stHorizontalBlock"]:has(.kpi-card) {
            width: 100% !important;
            max-width: 100% !important;
            min-width: 0 !important;
            box-sizing: border-box !important;
            overflow: visible !important;
            align-items: stretch !important;
        }

        [data-testid="stHorizontalBlock"]:has(.kpi-card) > [data-testid="stColumn"] {
            min-width: 0 !important;
            max-width: 100% !important;
            width: 100% !important;
            box-sizing: border-box !important;
            padding-left: 0 !important;
            padding-right: 0 !important;
            margin-left: 0 !important;
            margin-right: 0 !important;
            align-self: stretch !important;
            display: flex !important;
            flex-direction: column !important;
        }

        [data-testid="stHorizontalBlock"] .kpi-card {
            width: 100% !important;
            max-width: 100% !important;
            min-width: 0 !important;
            height: auto !important;
            box-sizing: border-box !important;
        }

        /* Keep the Streamlit wrappers from introducing hidden widths. */
        [data-testid="stHorizontalBlock"]:has(.kpi-card) > [data-testid="stColumn"] > div,
        [data-testid="stHorizontalBlock"]:has(.kpi-card) .stMarkdown,
        [data-testid="stHorizontalBlock"]:has(.kpi-card) .stMarkdownContainer {
            width: 100% !important;
            max-width: 100% !important;
            min-width: 0 !important;
            box-sizing: border-box !important;
        }

        /* ================= MOBILE: 2 CARDS PER ROW ================= */
        @media (max-width: 767px) {
            .main .block-container {
                width: 100% !important;
                max-width: 100% !important;
                min-width: 0 !important;
                overflow-x: hidden !important;
                padding-left: 0.75rem !important;
                padding-right: 0.75rem !important;
            }

            [data-testid="stHorizontalBlock"]:has(.kpi-card) {
                display: grid !important;
                grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
                width: 100% !important;
                max-width: 100% !important;
                min-width: 0 !important;
                column-gap: 16px !important;
                row-gap: 0 !important;
                align-items: stretch !important;
            }

            /* Padding below each Streamlit column creates a guaranteed
               visible row gap even when Streamlit's grid sizing changes. */
            [data-testid="stHorizontalBlock"]:has(.kpi-card) > [data-testid="stColumn"] {
                width: auto !important;
                max-width: 100% !important;
                min-width: 0 !important;
                padding-bottom: 16px !important;
            }

            [data-testid="stHorizontalBlock"]:has(.kpi-card) .kpi-card {
                width: 100% !important;
                min-width: 0 !important;
                min-height: 124px !important;
                height: auto !important;
            }
        }

        /* ================= SMALL PHONES ================= */
        @media (max-width: 480px) {
            .main .block-container {
                padding-left: 0.6rem !important;
                padding-right: 0.6rem !important;
            }

            [data-testid="stHorizontalBlock"]:has(.kpi-card) {
                grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
                column-gap: 14px !important;
                row-gap: 0 !important;
            }

            [data-testid="stHorizontalBlock"]:has(.kpi-card) > [data-testid="stColumn"] {
                padding-bottom: 14px !important;
            }

            [data-testid="stHorizontalBlock"]:has(.kpi-card) .kpi-card {
                min-height: 116px !important;
                padding: 0.68rem 0.72rem !important;
            }
        }

        /* ================= VERY SMALL PHONES ================= */
        /* Still keep 2 cards per row as requested. The card content
           scales down instead of changing the grid to one column. */
        @media (max-width: 360px) {
            .main .block-container {
                padding-left: 0.5rem !important;
                padding-right: 0.5rem !important;
            }

            [data-testid="stHorizontalBlock"]:has(.kpi-card) {
                grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
                column-gap: 12px !important;
                row-gap: 0 !important;
            }

            [data-testid="stHorizontalBlock"]:has(.kpi-card) > [data-testid="stColumn"] {
                padding-bottom: 12px !important;
            }

            [data-testid="stHorizontalBlock"]:has(.kpi-card) .kpi-card {
                min-height: 108px !important;
                padding: 0.58rem 0.62rem !important;
                border-radius: 12px !important;
            }

            [data-testid="stHorizontalBlock"]:has(.kpi-card) .kpi-label {
                font-size: 0.60rem !important;
            }

            [data-testid="stHorizontalBlock"]:has(.kpi-card) .kpi-value {
                font-size: 1.12rem !important;
            }

            [data-testid="stHorizontalBlock"]:has(.kpi-card) .kpi-helper {
                font-size: 0.55rem !important;
            }
        }

        /* =========================================================
           FINAL KPI CARD LAYOUT — ALL PAGES
           Only KPI cards are affected.

           Fixes:
           1. Complete rounded border on every card.
           2. No bottom/side clipping on desktop or mobile.
           3. Text/helper text remains visible inside the card.
           4. Equal width + equal height within each KPI row.
           5. 5 cards on one wide-desktop row.
           6. 4 cards on one wide-desktop row.
           7. Exactly 2 cards per row on tablet/mobile.
           8. Clear horizontal and vertical gaps.
           ========================================================= */

        /* KPI grid itself must NEVER clip a card's rounded corners. */
        [data-testid="stHorizontalBlock"]:has(.kpi-card) {
            display: grid !important;
            grid-template-columns: repeat(4, minmax(0, 1fr)) !important;
            grid-auto-flow: row !important;
            grid-auto-rows: auto !important;
            gap: 16px !important;
            row-gap: 16px !important;
            column-gap: 16px !important;
            width: 100% !important;
            max-width: 100% !important;
            min-width: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
            box-sizing: border-box !important;
            align-items: stretch !important;
            overflow: visible !important;
        }

        /* Overview: five cards on one desktop row. */
        [data-testid="stHorizontalBlock"]:has(.kpi-card):has(> [data-testid="stColumn"]:nth-child(5)) {
            grid-template-columns: repeat(5, minmax(0, 1fr)) !important;
        }

        /* Clean Streamlit column wrappers. Nothing clips the card. */
        [data-testid="stHorizontalBlock"]:has(.kpi-card) > [data-testid="stColumn"] {
            display: flex !important;
            flex-direction: column !important;
            align-items: stretch !important;
            justify-content: stretch !important;
            align-self: stretch !important;
            width: 100% !important;
            max-width: 100% !important;
            min-width: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
            flex: none !important;
            box-sizing: border-box !important;
            overflow: visible !important;
        }

        /* All Streamlit inner wrappers must also stay transparent to the
           card's full rounded shape and its contents. */
        [data-testid="stHorizontalBlock"] :has(.kpi-card) > div,
        [data-testid="stHorizontalBlock"]:has(.kpi-card) .stMarkdown,
        [data-testid="stHorizontalBlock"]:has(.kpi-card) .stMarkdownContainer {
            width: 100% !important;
            max-width: 100% !important;
            min-width: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
            box-sizing: border-box !important;
            overflow: visible !important;
        }

        /* =========================================================
           THE ACTUAL KPI CARD
           The previous height:100% + wrapper overflow combination was
           causing the lower part of some cards to be cut off. Let CSS
           Grid stretch each grid cell naturally instead.
           ========================================================= */
        [data-testid="stHorizontalBlock"] .kpi-card {
            display: flex !important;
            flex-direction: column !important;
            align-items: flex-start !important;
            justify-content: flex-start !important;
            width: 100% !important;
            max-width: 100% !important;
            min-width: 0 !important;
            height: auto !important;
            min-height: 142px !important;
            margin: 0 !important;
            box-sizing: border-box !important;

            /* Complete rounded card — all four corners. */
            border-radius: 16px !important;
            border: 1px solid rgba(255,255,255,0.18) !important;
            overflow: hidden !important;
            isolation: isolate !important;
            clip-path: inset(0 round 16px) !important;
        }

        /* Keep the decorative circle inside the rounded card. */
        [data-testid="stHorizontalBlock"] .kpi-card::before {
            z-index: -1 !important;
        }

        /* Desktop spacing. */
        @media (min-width: 1200px) {
            [data-testid="stHorizontalBlock"]:has(.kpi-card) {
                gap: 16px !important;
                row-gap: 16px !important;
                column-gap: 16px !important;
            }
        }

        /* =========================================================
           TABLET + MOBILE — TWO CARDS PER ROW
           ========================================================= */
        @media (max-width: 1199px) {
            [data-testid="stHorizontalBlock"]:has(.kpi-card),
            [data-testid="stHorizontalBlock"]:has(.kpi-card):has(> [data-testid="stColumn"]:nth-child(5)) {
                grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
                grid-auto-rows: auto !important;
                gap: 16px !important;
                row-gap: 16px !important;
                column-gap: 16px !important;
            }

            [data-testid="stHorizontalBlock"]:has(.kpi-card) .kpi-card {
                min-height: 124px !important;
                height: auto !important;
                border-radius: 16px !important;
                clip-path: inset(0 round 16px) !important;
            }
        }

        @media (max-width: 767px) {
            [data-testid="stHorizontalBlock"]:has(.kpi-card),
            [data-testid="stHorizontalBlock"]:has(.kpi-card):has(> [data-testid="stColumn"]:nth-child(5)) {
                grid-template-columns: minmax(0, 1fr) minmax(0, 1fr) !important;
                grid-auto-rows: auto !important;
                gap: 16px !important;
                row-gap: 16px !important;
                column-gap: 16px !important;
                width: 100% !important;
                max-width: 100% !important;
                overflow: visible !important;
            }

            [data-testid="stHorizontalBlock"]:has(.kpi-card) .kpi-card {
                min-height: 124px !important;
                height: auto !important;
                padding: 0.78rem 0.82rem !important;
                border-radius: 16px !important;
                clip-path: inset(0 round 16px) !important;
            }
        }

        /* Small phones: still two cards per row. */
        @media (max-width: 480px) {
            [data-testid="stHorizontalBlock"]:has(.kpi-card),
            [data-testid="stHorizontalBlock"]:has(.kpi-card):has(> [data-testid="stColumn"]:nth-child(5)) {
                grid-template-columns: minmax(0, 1fr) minmax(0, 1fr) !important;
                grid-auto-rows: auto !important;
                gap: 14px !important;
                row-gap: 14px !important;
                column-gap: 14px !important;
            }

            [data-testid="stHorizontalBlock"]:has(.kpi-card) .kpi-card {
                min-height: 116px !important;
                height: auto !important;
                padding: 0.68rem 0.72rem !important;
                border-radius: 15px !important;
                clip-path: inset(0 round 15px) !important;
            }

            [data-testid="stHorizontalBlock"]:has(.kpi-card) .kpi-label {
                font-size: 0.68rem !important;
                line-height: 1.25 !important;
            }

            [data-testid="stHorizontalBlock"]:has(.kpi-card) .kpi-value {
                font-size: 1.35rem !important;
                line-height: 1.1 !important;
            }

            [data-testid="stHorizontalBlock"]:has(.kpi-card) .kpi-helper {
                font-size: 0.64rem !important;
            }
        }

        /* =========================================================
           FINAL DESKTOP KPI PRESENTATION
           - Make every desktop KPI card the same larger size.
           - Center the icon, label, value and helper text.
           - Keep mobile/tablet behavior unchanged; mobile overrides
             below this block restore the normal left-aligned layout.
           ========================================================= */
        @media (min-width: 1200px) {
            [data-testid="stHorizontalBlock"]:has(.kpi-card) .kpi-card {
                min-height: 176px !important;
                height: 176px !important;
                padding: 1.05rem 1rem !important;
                align-items: center !important;
                justify-content: center !important;
                text-align: center !important;
                border-radius: 16px !important;
                clip-path: inset(0 round 16px) !important;
            }

            [data-testid="stHorizontalBlock"]:has(.kpi-card) .kpi-icon {
                margin-left: auto !important;
                margin-right: auto !important;
                margin-bottom: 0.55rem !important;
            }

            [data-testid="stHorizontalBlock"]:has(.kpi-card) .kpi-label {
                width: 100% !important;
                text-align: center !important;
                font-size: 0.90rem !important;
                line-height: 1.28 !important;
                letter-spacing: 0.04em !important;
            }

            [data-testid="stHorizontalBlock"]:has(.kpi-card) .kpi-value {
                width: 100% !important;
                text-align: center !important;
                font-size: 2.25rem !important;
                line-height: 1.12 !important;
                margin-top: 0.22rem !important;
            }

            [data-testid="stHorizontalBlock"]:has(.kpi-card) .kpi-helper {
                width: 100% !important;
                text-align: center !important;
                font-size: 0.80rem !important;
                line-height: 1.25 !important;
                margin-top: 0.32rem !important;
            }
        }

        /* Restore the existing left-aligned mobile/tablet presentation.
           These rules intentionally do not change the mobile card sizing,
           two-column grid, gaps, or responsive behavior. */
        @media (max-width: 1199px) {
            [data-testid="stHorizontalBlock"]:has(.kpi-card) .kpi-card {
                align-items: flex-start !important;
                justify-content: flex-start !important;
                text-align: left !important;
            }

            [data-testid="stHorizontalBlock"]:has(.kpi-card) .kpi-icon {
                margin-left: 0 !important;
                margin-right: 0 !important;
            }

            [data-testid="stHorizontalBlock"]:has(.kpi-card) .kpi-label,
            [data-testid="stHorizontalBlock"]:has(.kpi-card) .kpi-value,
            [data-testid="stHorizontalBlock"]:has(.kpi-card) .kpi-helper {
                width: auto !important;
                text-align: left !important;
            }
        }

        /* =========================================================
           TABLET KPI PRESENTATION — 768px TO 1199px
           Only KPI cards are adjusted here. Keep the existing mobile
           rules below/above intact. Tablet cards use the same polished
           centered presentation as desktop while retaining the existing
           two-column responsive grid and gaps.
           ========================================================= */
        @media (min-width: 768px) and (max-width: 1199px) {
            [data-testid="stHorizontalBlock"]:has(.kpi-card) {
                grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
                gap: 18px !important;
                row-gap: 18px !important;
                column-gap: 18px !important;
            }

            [data-testid="stHorizontalBlock"]:has(.kpi-card) .kpi-card {
                min-height: 156px !important;
                height: 156px !important;
                padding: 1rem 0.9rem !important;
                align-items: center !important;
                justify-content: center !important;
                text-align: center !important;
                border-radius: 16px !important;
                clip-path: inset(0 round 16px) !important;
            }

            [data-testid="stHorizontalBlock"]:has(.kpi-card) .kpi-icon {
                width: 40px !important;
                height: 40px !important;
                margin-left: auto !important;
                margin-right: auto !important;
                margin-bottom: 0.55rem !important;
                font-size: 1.08rem !important;
            }

            [data-testid="stHorizontalBlock"]:has(.kpi-card) .kpi-label {
                width: 100% !important;
                text-align: center !important;
                font-size: 0.84rem !important;
                line-height: 1.28 !important;
                letter-spacing: 0.035em !important;
            }

            [data-testid="stHorizontalBlock"]:has(.kpi-card) .kpi-value {
                width: 100% !important;
                text-align: center !important;
                font-size: 1.95rem !important;
                line-height: 1.12 !important;
                margin-top: 0.22rem !important;
            }

            [data-testid="stHorizontalBlock"]:has(.kpi-card) .kpi-helper {
                width: 100% !important;
                text-align: center !important;
                font-size: 0.74rem !important;
                line-height: 1.25 !important;
                margin-top: 0.3rem !important;
            }
        }

        /* At no breakpoint may the KPI grid/column wrappers clip the
           rounded corners or hide the card's lower text. */
        [data-testid="stHorizontalBlock"]:has(.kpi-card),
        [data-testid="stHorizontalBlock"]:has(.kpi-card) > [data-testid="stColumn"],
        [data-testid="stHorizontalBlock"]:has(.kpi-card) > [data-testid="stColumn"] > div,
        [data-testid="stHorizontalBlock"]:has(.kpi-card) .stMarkdown,
        [data-testid="stHorizontalBlock"]:has(.kpi-card) .stMarkdownContainer {
            overflow: visible !important;
        }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

@st.cache_data
def load_csv(filename):
    """Load a report CSV from the reports folder."""
    file_path = REPORTS_DIR / filename

    if not file_path.exists():
        return pd.DataFrame()

    return pd.read_csv(file_path)


def show_missing_file_message(filename):
    """Display a warning when a report is unavailable."""
    st.warning(
        f"Report file not found: reports/{filename}"
    )


def kpi_card(label, value, icon="📊", tone="blue", helper=None):
    """Render a responsive, professional KPI card."""
    safe_label = escape(str(label))
    safe_value = escape(str(value))
    safe_icon = escape(str(icon))
    safe_helper = escape(str(helper)) if helper else ""
    helper_html = (
        f'<div class="kpi-helper">{safe_helper}</div>'
        if helper else ""
    )

    st.markdown(
        f"""
        <div class="kpi-card kpi-{escape(str(tone))}">
            <div class="kpi-icon">{safe_icon}</div>
            <div class="kpi-label">{safe_label}</div>
            <div class="kpi-value">{safe_value}</div>
            {helper_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# LOAD REPORTS
# ============================================================

model_comparison = load_csv("model_comparison.csv")

baseline_metrics = load_csv("baseline_metrics.csv")
prophet_metrics = load_csv("prophet_metrics.csv")
lightgbm_metrics = load_csv("lightgbm_metrics.csv")

feature_importance = load_csv("lightgbm_feature_importance.csv")

inventory = load_csv("inventory_optimization.csv")
safety_stock = load_csv("safety_stock.csv")
reorder_point = load_csv("reorder_point.csv")

eda_summary = load_csv("eda_summary.csv")
product_store_summary = load_csv("product_store_demand_summary.csv")


# ============================================================
# HEADER

st.markdown(
    '<div class="topbar">'
    '<div class="brand-title"><span class="brand-mark">📊</span>Retail Demand Forecasting & Inventory Optimization</div>'
    '<div class="live-pill"><span class="live-dot"></span><span class="live-text">Live Dashboard</span></div>'
    '</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="page-heading">Project <span class="accent">Analytics</span></div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="page-subtitle">End-to-end analytics platform for demand forecasting, model evaluation, and inventory optimization.</div>',
    unsafe_allow_html=True,
)


# RESPONSIVE NAVIGATION
# All pages render inside this single script run via st.session_state /
# st.radio — clicking a nav item never opens a new tab or a separate
# webpage, it just re-renders this same page.

NAVIGATION_ITEMS = [
    "🏠  Overview",
    "📊  Model Performance",
    "📈  Forecast Analysis",
    "📦  Inventory Optimization",
    "✦  Feature Importance",
    "🗄️  Data Summary",
]

with st.sidebar:
    st.markdown(
        '<div class="side-brand">'
        '<div class="side-logo">📊</div>'
        '<div><div class="side-title">Retail Analytics</div>'
        '<div class="side-subtitle">Demand Forecasting &<br>Inventory Optimization</div></div>'
        '</div>',
        unsafe_allow_html=True,
    )

    selected_nav = st.radio(
        "Dashboard Navigation",
        NAVIGATION_ITEMS,
        index=0,
        label_visibility="visible",
    )

    page = selected_nav.split("  ", 1)[-1].strip()

    st.markdown(
        '<div class="side-info"><b>💡 Data Source</b><br>'
        'Project reports generated from the forecasting and inventory optimization pipeline.</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="side-footer">© 2026 Retail Analytics<br>Built with Python · SQL · DuckDB · Streamlit</div>',
        unsafe_allow_html=True,
    )


# ============================================================
# AUTO-COLLAPSE SIDEBAR ON MOBILE/TABLET AFTER NAVIGATION
# ------------------------------------------------------------
# There is only ONE navigation control in this app: Streamlit's own
# native sidebar (opened via the hamburger rail button styled in the
# CSS above). No second hamburger, popover, or top nav box exists.
#
# On desktop the sidebar just stays open as normal. On mobile/tablet
# viewports, once the visitor taps a navigation item, this script
# automatically triggers Streamlit's own native sidebar-close control
# (kept in the DOM but visually hidden via CSS) so the chosen page
# takes the full screen — the same pattern used by professional
# responsive sites, without introducing any extra nav system.
#
# Runs inside a components.html iframe, so `window.parent` is used to
# reach into the actual Streamlit page DOM.
# ============================================================

components.html(
    """
    <script>
    (function () {
        const MOBILE_BREAKPOINT = 1200; // matches the tablet/mobile CSS breakpoints

        function bindAutoCollapse() {
            const doc = window.parent.document;
            const sidebar = doc.querySelector('section[data-testid="stSidebar"]');
            if (!sidebar) return;

            const radios = sidebar.querySelectorAll('input[type="radio"]');
            radios.forEach(function (radio) {
                if (radio.dataset.autoCollapseBound) return;
                radio.dataset.autoCollapseBound = "true";

                radio.addEventListener("change", function () {
                    if (window.parent.innerWidth > MOBILE_BREAKPOINT) return;

                    setTimeout(function () {
                        const closeControl =
                            doc.querySelector('[data-testid*="SidebarCollapseButton"]') ||
                            doc.querySelector('[aria-label="Close sidebar"]');
                        if (!closeControl) return;

                        const button =
                            closeControl.tagName === "BUTTON"
                                ? closeControl
                                : closeControl.querySelector("button") || closeControl;
                        button.click();
                    }, 150);
                });
            });
        }

        bindAutoCollapse();

        const observer = new MutationObserver(bindAutoCollapse);
        observer.observe(window.parent.document.body, {
            childList: true,
            subtree: true,
        });
    })();
    </script>
    """,
    height=0,
)


# CHART HELPERS
# ============================================================

CHART_CONFIG = {
    "responsive": True,
    "displaylogo": False,
    "scrollZoom": False,
    "displayModeBar": "hover",
}


def selected_point_index(event):
    """Safely extract the first selected Plotly point index."""
    try:
        points = event.selection.points
        if points:
            return int(points[0]["point_index"])
    except (AttributeError, KeyError, TypeError, IndexError, ValueError):
        pass
    return None


def render_selectable_bar_chart(
    fig,
    *,
    key,
    values,
    x_labels=None,
    value_format=".2f",
    orientation="v",
    height=340,
):
    """
    Render a responsive, professional bar chart.

    - Bars are narrowed with `bargap` so they never look oversized on
      wide screens or squashed on mobile.
    - When a bar is clicked, its value is shown in a small callout box
      pinned directly above (vertical) or beside the tip of (horizontal)
      that exact bar via a Plotly annotation — not as trace text, which
      is what caused the label to drift to the side of the bar before.
    """
    state_key = f"{key}__selected_index"
    selected_index = st.session_state.get(state_key)

    values = [float(v) for v in values]
    n = len(values)
    x_labels = list(x_labels) if x_labels is not None else [str(i) for i in range(n)]

    if selected_index is not None and not (0 <= int(selected_index) < n):
        selected_index = None
        st.session_state.pop(state_key, None)

    base_color = "#72b8f4"
    selected_color = "#2f80ed"
    marker_colors = [
        selected_color if selected_index is not None and i == int(selected_index) else base_color
        for i in range(n)
    ]

    # Clear any built-in trace text — the callout annotation below is the
    # single source of truth for the selected value, so it can never
    # appear twice or in the wrong place.
    fig.update_traces(
        text=None,
        textposition="none",
        marker_color=marker_colors,
        marker_line_width=0,
        hoverinfo="skip",
        selectedpoints=[int(selected_index)] if selected_index is not None else None,
    )

    fig.update_layout(
        height=height,
        autosize=True,
        hovermode=False,
        bargap=0.38,
        bargroupgap=0.12,
        margin=dict(l=48, r=22, t=58, b=58),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#cbd5e1", family="Inter, Segoe UI, sans-serif"),
        title_font=dict(color="#f8fafc", size=15),
        xaxis=dict(
            automargin=True,
            gridcolor="rgba(148,163,184,0.13)",
            zerolinecolor="rgba(148,163,184,0.18)",
            tickfont=dict(size=11),
        ),
        yaxis=dict(
            automargin=True,
            gridcolor="rgba(148,163,184,0.13)",
            zerolinecolor="rgba(148,163,184,0.18)",
            tickfont=dict(size=11),
        ),
        showlegend=False,
        annotations=[],
    )

    if selected_index is not None:
        idx = int(selected_index)
        value_text = format(values[idx], value_format)
        label_text = escape(str(x_labels[idx]))

        if orientation == "h":
            # Horizontal bars: callout sits just past the tip, level
            # with that bar's row.
            fig.add_annotation(
                x=values[idx],
                y=idx,
                xref="x",
                yref="y",
                text=f"<b>{label_text}</b><br>{value_text}",
                showarrow=True,
                arrowhead=0,
                arrowwidth=1,
                arrowcolor="rgba(148,163,184,0.55)",
                ax=46,
                ay=0,
                align="left",
                bgcolor="#0f172a",
                bordercolor="rgba(96,165,250,0.45)",
                borderwidth=1,
                borderpad=6,
                font=dict(color="#f8fafc", size=12),
            )
        else:
            # Vertical bars: callout sits centered directly above the
            # top of that exact bar.
            fig.add_annotation(
                x=idx,
                y=values[idx],
                xref="x",
                yref="y",
                text=f"<b>{label_text}</b><br>{value_text}",
                showarrow=True,
                arrowhead=0,
                arrowwidth=1,
                arrowcolor="rgba(148,163,184,0.55)",
                ax=0,
                ay=-42,
                align="center",
                bgcolor="#0f172a",
                bordercolor="rgba(96,165,250,0.45)",
                borderwidth=1,
                borderpad=6,
                font=dict(color="#f8fafc", size=12),
            )

    event = st.plotly_chart(
        fig,
        use_container_width=True,
        key=key,
        on_select="rerun",
        selection_mode="points",
        config=CHART_CONFIG,
    )

    new_index = selected_point_index(event)
    current_index = st.session_state.get(state_key)

    if new_index is not None and new_index != current_index:
        st.session_state[state_key] = new_index
        st.rerun()

    if hasattr(event, "selection") and not event.selection.points and current_index is not None:
        st.session_state.pop(state_key, None)
        st.rerun()

    return new_index


def section_header(kicker, title, subtitle=None):
    subtitle_html = f'<div class="section-subtitle">{escape(str(subtitle))}</div>' if subtitle else ""
    st.markdown(
        f'<div class="section-kicker">{escape(str(kicker))}</div>'
        f'<div class="section-title">{escape(str(title))}</div>'
        f'{subtitle_html}',
        unsafe_allow_html=True,
    )


def selection_note(text):
    st.markdown(
        f'<div class="selection-note">● {escape(str(text))}</div>',
        unsafe_allow_html=True,
    )

# ============================================================
# OVERVIEW
# ============================================================

if page == "Overview":

    st.markdown('<div class="page-heading">Project <span class="accent">Overview</span></div>', unsafe_allow_html=True)

    # --------------------------------------------------------
    # Calculate overview metrics
    # --------------------------------------------------------

    if not inventory.empty:

        total_products = inventory["item_id"].nunique()
        total_stores = inventory["store_id"].nunique()
        total_combinations = len(inventory)

        if "forecast_demand" in inventory.columns:
            total_forecast = inventory["forecast_demand"].sum()
        else:
            total_forecast = 0

        if "target_inventory" in inventory.columns:
            total_target_inventory = inventory["target_inventory"].sum()
        else:
            total_target_inventory = 0

    else:

        total_products = 0
        total_stores = 0
        total_combinations = 0
        total_forecast = 0
        total_target_inventory = 0

    # --------------------------------------------------------
    # KPI cards
    # --------------------------------------------------------

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        kpi_card("Products", f"{total_products:,}", "📦", "blue", "Unique products")

    with col2:
        kpi_card("Stores", f"{total_stores:,}", "🏬", "purple", "Active stores")

    with col3:
        kpi_card("Product-Store Pairs", f"{total_combinations:,}", "🔗", "cyan", "Inventory combinations")

    with col4:
        kpi_card("Forecast Demand", f"{total_forecast:,.2f}", "📈", "green", "Projected demand")

    with col5:
        kpi_card("Target Inventory", f"{total_target_inventory:,.2f}", "🎯", "orange", "Recommended target")

    st.markdown("---")

    # --------------------------------------------------------
    # Model summary
    # --------------------------------------------------------

    st.subheader("Forecasting Model Summary")

    if not model_comparison.empty:

        display_columns = [
            column
            for column in [
                "model",
                "validation_rows",
                "MAE",
                "RMSE",
                "WAPE",
                "sMAPE"
            ]
            if column in model_comparison.columns
        ]

        st.dataframe(
            model_comparison[display_columns],
            use_container_width=True,
            hide_index=True
        )

        if "MAE" in model_comparison.columns:

            fig = px.bar(
                model_comparison,
                x="model",
                y="MAE",
                title="Model MAE Comparison",
            )

            fig.update_layout(
                margin=dict(l=50, r=24, t=70, b=55),
                xaxis_title="Model",
                yaxis_title="MAE",
            )

            render_selectable_bar_chart(
                fig,
                key="overview-mae-chart",
                values=model_comparison["MAE"].tolist(),
                x_labels=model_comparison["model"].tolist(),
                value_format=".4f",
                height=340,
            )

    else:
        show_missing_file_message("model_comparison.csv")


# ============================================================
# MODEL PERFORMANCE
# ============================================================

elif page == "Model Performance":

    st.markdown('<div class="page-heading">Model <span class="accent">Performance</span></div>', unsafe_allow_html=True)

    if model_comparison.empty:

        show_missing_file_message("model_comparison.csv")

    else:

        # ----------------------------------------------------
        # Metrics table
        # ----------------------------------------------------

        st.subheader("Model Evaluation Metrics")

        st.dataframe(
            model_comparison,
            use_container_width=True,
            hide_index=True
        )

        st.markdown("---")

        # ----------------------------------------------------
        # MAE / RMSE
        # ----------------------------------------------------

        col1, col2 = st.columns(2)

        with col1:

            if "MAE" in model_comparison.columns:

                fig_mae = px.bar(
                    model_comparison,
                    x="model",
                    y="MAE",
                    title="Mean Absolute Error (MAE)",
                )

                fig_mae.update_layout(
                    margin=dict(l=50, r=24, t=70, b=55),
                    xaxis_title="Model",
                    yaxis_title="MAE",
                )

                render_selectable_bar_chart(
                    fig_mae,
                    key="performance-mae-chart",
                    values=model_comparison["MAE"].tolist(),
                    x_labels=model_comparison["model"].tolist(),
                    value_format=".4f",
                    height=330,
                )

        with col2:

            if "RMSE" in model_comparison.columns:

                fig_rmse = px.bar(
                    model_comparison,
                    x="model",
                    y="RMSE",
                    title="Root Mean Squared Error (RMSE)",
                )

                fig_rmse.update_layout(
                    margin=dict(l=50, r=24, t=70, b=55),
                    xaxis_title="Model",
                    yaxis_title="RMSE",
                )

                render_selectable_bar_chart(
                    fig_rmse,
                    key="performance-rmse-chart",
                    values=model_comparison["RMSE"].tolist(),
                    x_labels=model_comparison["model"].tolist(),
                    value_format=".4f",
                    height=330,
                )

        # ----------------------------------------------------
        # WAPE / sMAPE
        # ----------------------------------------------------

        col3, col4 = st.columns(2)

        with col3:

            if "WAPE" in model_comparison.columns:

                fig_wape = px.bar(
                    model_comparison,
                    x="model",
                    y="WAPE",
                    title="Weighted Absolute Percentage Error (WAPE)",
                )

                fig_wape.update_layout(
                    margin=dict(l=50, r=24, t=70, b=55),
                    xaxis_title="Model",
                    yaxis_title="WAPE",
                )

                render_selectable_bar_chart(
                    fig_wape,
                    key="performance-wape-chart",
                    values=model_comparison["WAPE"].tolist(),
                    x_labels=model_comparison["model"].tolist(),
                    value_format=".2f",
                    height=330,
                )

        with col4:

            if "sMAPE" in model_comparison.columns:

                fig_smape = px.bar(
                    model_comparison,
                    x="model",
                    y="sMAPE",
                    title="Symmetric Mean Absolute Percentage Error",
                )

                fig_smape.update_layout(
                    margin=dict(l=50, r=24, t=70, b=55),
                    xaxis_title="Model",
                    yaxis_title="sMAPE",
                )

                render_selectable_bar_chart(
                    fig_smape,
                    key="performance-smape-chart",
                    values=model_comparison["sMAPE"].tolist(),
                    x_labels=model_comparison["model"].tolist(),
                    value_format=".2f",
                    height=330,
                )

        # ----------------------------------------------------
        # Individual metric files
        # ----------------------------------------------------

        st.markdown("---")

        st.subheader("Individual Model Reports")

        tab1, tab2, tab3 = st.tabs(
            [
                "Baseline",
                "Prophet",
                "LightGBM"
            ]
        )

        with tab1:

            if not baseline_metrics.empty:
                st.dataframe(
                    baseline_metrics,
                    use_container_width=True,
                    hide_index=True
                )
            else:
                show_missing_file_message(
                    "baseline_metrics.csv"
                )

        with tab2:

            if not prophet_metrics.empty:
                st.dataframe(
                    prophet_metrics,
                    use_container_width=True,
                    hide_index=True
                )
            else:
                show_missing_file_message(
                    "prophet_metrics.csv"
                )

        with tab3:

            if not lightgbm_metrics.empty:
                st.dataframe(
                    lightgbm_metrics,
                    use_container_width=True,
                    hide_index=True
                )
            else:
                show_missing_file_message(
                    "lightgbm_metrics.csv"
                )


# ============================================================
# FORECAST ANALYSIS
# ============================================================

elif page == "Forecast Analysis":

    st.markdown('<div class="page-heading">Forecast <span class="accent">Analysis</span></div>', unsafe_allow_html=True)

    if inventory.empty:

        show_missing_file_message(
            "inventory_optimization.csv"
        )

    else:

        # ----------------------------------------------------
        # Product selector
        # ----------------------------------------------------

        products = sorted(
            inventory["item_id"].dropna().unique()
        )

        selected_product = st.selectbox(
            "Select Product",
            products
        )

        product_data = inventory[
            inventory["item_id"] == selected_product
        ].copy()

        # ----------------------------------------------------
        # Product KPIs
        # ----------------------------------------------------

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            forecast_value = product_data[
                "forecast_demand"
            ].sum()

            kpi_card("Forecast Demand", f"{forecast_value:,.2f}", "📈", "blue", "Selected product")

        with col2:

            if "average_daily_demand" in product_data.columns:

                avg_demand = product_data[
                    "average_daily_demand"
                ].mean()

                kpi_card("Average Daily Demand", f"{avg_demand:.2f}", "📅", "cyan", "Per-day average")

        with col3:

            if "safety_stock" in product_data.columns:

                avg_safety = product_data[
                    "safety_stock"
                ].mean()

                kpi_card("Average Safety Stock", f"{avg_safety:.2f}", "🛡️", "purple", "Service-level buffer")

        with col4:

            if "reorder_point" in product_data.columns:

                avg_reorder = product_data[
                    "reorder_point"
                ].mean()

                kpi_card("Average Reorder Point", f"{avg_reorder:.2f}", "🔄", "orange", "Restock threshold")

        st.markdown("---")

        # ----------------------------------------------------
        # Product-store forecast chart
        # ----------------------------------------------------

        if "store_id" in product_data.columns:

            chart_data = product_data.reset_index(drop=True)

            fig = px.bar(
                chart_data,
                x="store_id",
                y="forecast_demand",
                title=f"Forecast Demand by Store — {selected_product}",
            )

            fig.update_layout(
                title=f"Forecast Demand by Store — {selected_product}",
                margin=dict(l=50, r=24, t=70, b=55),
                xaxis_title="Store ID",
                yaxis_title="Forecast Demand",
            )

            chart_key = "forecast-store-chart"
            existing_index = st.session_state.get(f"{chart_key}__selected_index")

            if existing_index is not None and not (0 <= int(existing_index) < len(chart_data)):
                st.session_state.pop(f"{chart_key}__selected_index", None)
                existing_index = None

            if existing_index is not None:
                selected_store = chart_data.iloc[int(existing_index)]["store_id"]
                selected_value = float(chart_data.iloc[int(existing_index)]["forecast_demand"])
                selection_note(f"Selected store: {selected_store}  ·  Forecast demand: {selected_value:.2f}")

            render_selectable_bar_chart(
                fig,
                key=chart_key,
                values=chart_data["forecast_demand"].astype(float).tolist(),
                x_labels=chart_data["store_id"].astype(str).tolist(),
                value_format=".2f",
                height=350,
            )

        # ----------------------------------------------------
        # Product table
        # ----------------------------------------------------

        st.subheader(
            f"Forecast Details — {selected_product}"
        )

        columns = [
            "item_id",
            "store_id",
            "forecast_demand",
            "forecast_daily_average",
            "forecast_horizon_days",
            "safety_stock",
            "reorder_point",
            "target_inventory",
            "recommended_action"
        ]

        available_columns = [
            column
            for column in columns
            if column in product_data.columns
        ]

        st.dataframe(
            product_data[available_columns],
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# INVENTORY OPTIMIZATION
# ============================================================

elif page == "Inventory Optimization":

    st.markdown('<div class="page-heading">Inventory <span class="accent">Optimization</span></div>', unsafe_allow_html=True)

    if inventory.empty:

        show_missing_file_message(
            "inventory_optimization.csv"
        )

    else:

        # ----------------------------------------------------
        # KPI calculations
        # ----------------------------------------------------

        avg_safety_stock = (
            inventory["safety_stock"].mean()
            if "safety_stock" in inventory.columns
            else 0
        )

        avg_reorder_point = (
            inventory["reorder_point"].mean()
            if "reorder_point" in inventory.columns
            else 0
        )

        avg_target_inventory = (
            inventory["target_inventory"].mean()
            if "target_inventory" in inventory.columns
            else 0
        )

        # ----------------------------------------------------
        # KPI cards
        # ----------------------------------------------------

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            kpi_card("Average Safety Stock", f"{avg_safety_stock:.2f}", "🛡️", "blue", "Inventory protection")

        with col2:
            kpi_card("Average Reorder Point", f"{avg_reorder_point:.2f}", "🔄", "purple", "Restock threshold")

        with col3:
            kpi_card("Average Target Inventory", f"{avg_target_inventory:.2f}", "🎯", "green", "Recommended stock")

        with col4:

            if "forecast_demand" in inventory.columns:

                total_forecast = inventory[
                    "forecast_demand"
                ].sum()

                kpi_card("Total Forecast Demand", f"{total_forecast:,.2f}", "📊", "orange", "Forecast horizon")

        st.markdown("---")

        # ----------------------------------------------------
        # Inventory level distribution
        # ----------------------------------------------------

        col1, col2 = st.columns(2)

        with col1:

            if "inventory_level" in inventory.columns:

                level_counts = (
                    inventory["inventory_level"]
                    .value_counts()
                    .reset_index()
                )

                level_counts.columns = [
                    "inventory_level",
                    "count"
                ]

                fig = px.pie(
                    level_counts,
                    names="inventory_level",
                    values="count",
                    title="Inventory Level Distribution",
                    hole=0.4
                )

                fig.update_layout(
                    margin=dict(l=20, r=20, t=70, b=30),
                    height=430,
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#cbd5e1", family="Inter, Segoe UI, sans-serif"),
                    title_font=dict(color="#f8fafc", size=15),
                    legend=dict(font=dict(color="#cbd5e1")),
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                    config=CHART_CONFIG,
                )

        with col2:

            if "recommended_action" in inventory.columns:

                action_counts = (
                    inventory["recommended_action"]
                    .value_counts()
                    .reset_index()
                )

                action_counts.columns = [
                    "recommended_action",
                    "count"
                ]

                fig = px.bar(
                    action_counts,
                    x="recommended_action",
                    y="count",
                    title="Recommended Inventory Actions",
                )

                fig.update_layout(
                    margin=dict(l=50, r=24, t=70, b=60),
                    xaxis=dict(title="Recommended action", automargin=True),
                    yaxis=dict(title="Count", automargin=True),
                )

                render_selectable_bar_chart(
                    fig,
                    key="inventory-actions-chart",
                    values=action_counts["count"].tolist(),
                    x_labels=action_counts["recommended_action"].astype(str).tolist(),
                    value_format=".0f",
                    height=430,
                )

        # ----------------------------------------------------
        # Safety stock
        # ----------------------------------------------------

        st.markdown("---")

        st.subheader("Safety Stock Analysis")

        if not safety_stock.empty:

            st.dataframe(
                safety_stock,
                use_container_width=True,
                hide_index=True
            )

        # ----------------------------------------------------
        # Reorder point
        # ----------------------------------------------------

        st.subheader("Reorder Point Analysis")

        if not reorder_point.empty:

            st.dataframe(
                reorder_point,
                use_container_width=True,
                hide_index=True
            )

        # ----------------------------------------------------
        # Inventory optimization table
        # ----------------------------------------------------

        st.subheader("Inventory Recommendations")

        display_columns = [
            "item_id",
            "store_id",
            "forecast_demand",
            "safety_stock",
            "reorder_point",
            "target_inventory",
            "inventory_level",
            "recommended_action"
        ]

        available_columns = [
            column
            for column in display_columns
            if column in inventory.columns
        ]

        st.dataframe(
            inventory[available_columns],
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# FEATURE IMPORTANCE
# ============================================================

elif page == "Feature Importance":

    st.markdown('<div class="page-heading">Feature <span class="accent">Importance</span></div>', unsafe_allow_html=True)

    if feature_importance.empty:

        show_missing_file_message(
            "lightgbm_feature_importance.csv"
        )

    else:

        st.subheader(
            "Features Used by the LightGBM Forecasting Model"
        )

        # Try to identify feature and importance columns
        feature_column = None
        importance_column = None

        for column in feature_importance.columns:

            column_lower = column.lower()

            if (
                feature_column is None
                and "feature" in column_lower
            ):
                feature_column = column

            if (
                importance_column is None
                and "importance" in column_lower
            ):
                importance_column = column

        if (
            feature_column is not None
            and importance_column is not None
        ):

            feature_plot_data = (
                feature_importance
                .sort_values(
                    importance_column,
                    ascending=False
                )
                .head(20)
            )

            fig = px.bar(
                feature_plot_data,
                x=importance_column,
                y=feature_column,
                orientation="h",
                title="Top 20 Feature Importance",
            )

            fig.update_layout(
                margin=dict(l=90, r=24, t=70, b=55),
                xaxis=dict(title="Importance", automargin=True),
                yaxis=dict(
                    title="Feature",
                    categoryorder="total ascending",
                    automargin=True,
                ),
            )

            render_selectable_bar_chart(
                fig,
                key="feature-importance-chart",
                values=feature_plot_data[importance_column].astype(float).tolist(),
                x_labels=feature_plot_data[feature_column].astype(str).tolist(),
                value_format=".4f",
                orientation="h",
                height=500,
            )

        st.subheader("Feature Importance Table")

        st.dataframe(
            feature_importance,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# DATA SUMMARY
# ============================================================

elif page == "Data Summary":

    st.markdown('<div class="page-heading">Data <span class="accent">Summary</span></div>', unsafe_allow_html=True)

    # --------------------------------------------------------
    # EDA summary
    # --------------------------------------------------------

    if not eda_summary.empty:

        st.subheader("EDA Summary")

        st.dataframe(
            eda_summary,
            use_container_width=True,
            hide_index=True
        )

    else:

        show_missing_file_message(
            "eda_summary.csv"
        )

    st.markdown("---")

    # --------------------------------------------------------
    # Product-store summary
    # --------------------------------------------------------

    if not product_store_summary.empty:

        st.subheader(
            "Product-Store Demand Summary"
        )

        st.dataframe(
            product_store_summary,
            use_container_width=True,
            hide_index=True
        )

    else:

        show_missing_file_message(
            "product_store_demand_summary.csv"
        )


# ============================================================
# FOOTER

st.markdown(
    '<div class="dashboard-footer">'
    '<div class="dashboard-footer-insight">'
    '<div class="dashboard-footer-title">🎯 Optimizing inventory through data-driven demand forecasting</div>'
    '<div class="dashboard-footer-subtitle">Better forecasts. Leaner inventory. Higher operational efficiency.</div>'
    '</div>'
    '<div class="dashboard-footer-meta">'
    'Retail Demand Forecasting & Inventory Optimization · Python · SQL · DuckDB · Prophet · LightGBM · Streamlit'
    '</div>'
    '</div>',
    unsafe_allow_html=True,
)
