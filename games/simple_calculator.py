"""
Simple Calculator mini-app for Toko Pintar
Modern, user-friendly UI for basic arithmetic operations.
"""
import streamlit as st
from urllib.parse import parse_qs


def get_game_info():
    """Get information about the simple calculator game."""
    return {
        "id": "simple_calculator",
        "name": {
            "en": "Simple Calculator",
            "id": "Kalkulator Sederhana"
        },
        "title": "Simple Calculator",
        "description": {
            "en": "A basic calculator for quick arithmetic.",
            "id": "Kalkulator dasar untuk aritmatika cepat."
        },
        "primary_skill": None,
        "levels": 1
    }


def simple_calculator_game():
    # --- Calculator Session State ---
    if "calc_display" not in st.session_state:
        st.session_state["calc_display"] = ""
    if "calc_last" not in st.session_state:
        st.session_state["calc_last"] = ""
    if "calc_operator" not in st.session_state:
        st.session_state["calc_operator"] = ""
    if "calc_reset" not in st.session_state:
        st.session_state["calc_reset"] = False
    if "calc_formula" not in st.session_state:
        st.session_state["calc_formula"] = ""
    if "calc_show_result" not in st.session_state:
        st.session_state["calc_show_result"] = False

    # --- Helper to safely get query param value ---
    def get_first_param(query_params, key):
        val = query_params.get(key)
        return val[0] if val and len(val) > 0 else None

    # --- Restore calculator state from query params if present ---
    query_params = st.query_params
    calc_display = get_first_param(query_params, "calc_display")
    calc_formula = get_first_param(query_params, "calc_formula")
    calc_last = get_first_param(query_params, "calc_last")
    calc_operator = get_first_param(query_params, "calc_operator")
    calc_reset = get_first_param(query_params, "calc_reset")
    calc_show_result = get_first_param(query_params, "calc_show_result")

    if calc_display is not None:
        st.session_state["calc_display"] = calc_display
    if calc_formula is not None:
        st.session_state["calc_formula"] = calc_formula
    if calc_last is not None:
        st.session_state["calc_last"] = calc_last
    if calc_operator is not None:
        st.session_state["calc_operator"] = calc_operator
    if calc_reset is not None:
        st.session_state["calc_reset"] = calc_reset == "True"
    if calc_show_result is not None:
        st.session_state["calc_show_result"] = calc_show_result == "True"

    # --- Handle Button Clicks via Query Params ---
    btn_clicked = get_first_param(query_params, "calc_btn")
    if btn_clicked:
        handle_calculator_input(btn_clicked)
        # Remove the query param after handling to prevent repeated actions
        # But keep state in query params for reload persistence
        st.query_params.clear()
        st.query_params.update({
            "calc_display": st.session_state["calc_display"],
            "calc_formula": st.session_state["calc_formula"],
            "calc_last": st.session_state["calc_last"],
            "calc_operator": st.session_state["calc_operator"],
            "calc_reset": str(st.session_state["calc_reset"]),
            "calc_show_result": str(st.session_state["calc_show_result"]),
        })
        st.rerun()

    st.markdown("""
        <div style='text-align:center;margin-bottom:10px;'>
            <span style='font-size:2.2rem;font-weight:bold;color:#1565C0;'>🧮 Simple Calculator</span>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("<hr style='margin:0 0 20px 0;'>", unsafe_allow_html=True)

    # --- Display ---
    formula = st.session_state["calc_formula"]
    display_val = st.session_state["calc_display"] or "0"
    show_result = st.session_state["calc_show_result"]
    st.markdown("""
        <div class='calc-mobile-display'>
    """, unsafe_allow_html=True)
    if formula and not show_result:
        st.markdown(f"<div style='font-size:1.02rem;color:#888;min-height:18px;height:18px;text-align:right;'>{formula}</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size:2.1rem;color:#222;text-align:right;'>{display_val}</div>", unsafe_allow_html=True)
    st.markdown("""
        </div>
    """, unsafe_allow_html=True)

    # --- Calculator Buttons Layout as HTML/CSS Grid ---
    button_grid = [
        ["7", "8", "9", "÷"],
        ["4", "5", "6", "×"],
        ["1", "2", "3", "-"],
        ["0", ".", "C", "+"],
        ["+/-", "=", None, None],
    ]
    html = """
    <form id='calc-form' autocomplete='off'>
        <div class='calc-grid'>
    """
    for row in button_grid:
        for label in row:
            if label is None:
                html += "<div class='calc-btn calc-btn-empty'></div>"
            else:
                html += f"<button type='submit' name='calc_btn' value='{label}' class='calc-btn'>{label}</button>"
    html += """
        </div>
    </form>
    <script>
    // Submit form and update query param on button click
    document.querySelectorAll('.calc-btn').forEach(function(btn){
        btn.addEventListener('click', function(e){
            e.preventDefault();
            const val = btn.value;
            const url = new URL(window.location.href);
            url.searchParams.set('calc_btn', val);
            // Also add calculator state to query params
            url.searchParams.set('calc_display', document.querySelector('.calc-mobile-display div:last-child').innerText);
            const formulaDiv = document.querySelector('.calc-mobile-display div:first-child');
            url.searchParams.set('calc_formula', formulaDiv ? formulaDiv.innerText : '');
            // The rest of the state is managed in Python and will be synced after processing
            window.location.href = url.toString();
        });
    });
    </script>
    """
    st.markdown(html, unsafe_allow_html=True)

    # --- Responsive Calculator CSS ---
    st.markdown("""
        <style>
        .calc-mobile-display {
            background: #fff;
            border-radius: 8px;
            padding: 8px 8px 4px 8px;
            margin-bottom: 10px;
            text-align: right;
            font-size: 2.1rem;
            letter-spacing: 1px;
            min-height: 40px;
            border: 1.5px solid #e0e0e0;
            box-shadow: 0 1px 2px rgba(60,60,60,0.03);
            color: #222;
            word-break: break-all;
        }
        .calc-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 8px;
            width: 100%;
            max-width: 400px;
            margin: 0 auto 12px auto;
        }
        .calc-btn {
            background: #f2f2f2;
            border: 1.5px solid #e0e0e0;
            color: #222;
            font-size: 1.23rem;
            font-weight: 500;
            border-radius: 7px;
            padding: 12px 0;
            margin: 0;
            transition: background 0.2s, box-shadow 0.2s, color 0.2s;
            box-shadow: 0 1px 2px rgba(60,60,60,0.03);
            width: 100%;
            height: 48px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
        }
        .calc-btn:hover {
            background: #FF7043;
            color: #fff;
            border: 1.5px solid #FF7043;
        }
        .calc-btn-empty {
            background: transparent;
            border: none;
            box-shadow: none;
            cursor: default;
        }
        @media (max-width: 600px) {
            .calc-mobile-display {
                font-size: 1.4rem;
                padding: 7px 4px 2px 4px;
                min-height: 32px;
            }
            .calc-grid {
                max-width: 100vw;
                gap: 5px;
            }
            .calc-btn {
                font-size: 1.05rem;
                padding: 8px 0;
                height: 38px;
            }
        }
        </style>
    """, unsafe_allow_html=True)


def handle_calculator_input(label):
    display = st.session_state["calc_display"]
    last = st.session_state["calc_last"]
    operator = st.session_state["calc_operator"]
    reset = st.session_state["calc_reset"]
    formula = st.session_state["calc_formula"]
    show_result = st.session_state["calc_show_result"]

    if label in "0123456789":
        if reset or display == "0" or show_result:
            display = label
            st.session_state["calc_reset"] = False
            if show_result:
                formula = ""
                st.session_state["calc_show_result"] = False
        else:
            display += label
        formula += label if not show_result else label
    elif label == ".":
        if reset or not display or show_result:
            display = "0."
            st.session_state["calc_reset"] = False
            if show_result:
                formula = ""
                st.session_state["calc_show_result"] = False
        elif "." not in display:
            display += "."
        formula += "." if not show_result else "."
    elif label in ["+", "-", "×", "÷"]:
        if display:
            st.session_state["calc_last"] = display
            st.session_state["calc_operator"] = label
            st.session_state["calc_reset"] = True
            if not formula.endswith(tuple(["+", "-", "×", "÷"])):
                formula += f" {label} "
            else:
                formula = formula[:-3] + f" {label} "
        st.session_state["calc_show_result"] = False
    elif label == "=":
        if operator and last and display:
            try:
                n1 = float(last)
                n2 = float(display)
                if operator == "+":
                    result = n1 + n2
                elif operator == "-":
                    result = n1 - n2
                elif operator == "×":
                    result = n1 * n2
                elif operator == "÷":
                    if n2 == 0:
                        display = "Error"
                        st.session_state["calc_reset"] = True
                    else:
                        result = n1 / n2
                if display != "Error":
                    display = str(result).rstrip("0").rstrip(".") if "." in str(result) else str(result)
                    st.session_state["calc_reset"] = True
                st.session_state["calc_operator"] = ""
                st.session_state["calc_last"] = ""
                st.session_state["calc_show_result"] = True
                formula = ""
            except Exception:
                display = "Error"
                st.session_state["calc_reset"] = True
                st.session_state["calc_show_result"] = True
                formula = ""
    elif label == "C":
        display = ""
        st.session_state["calc_last"] = ""
        st.session_state["calc_operator"] = ""
        st.session_state["calc_reset"] = False
        formula = ""
        st.session_state["calc_show_result"] = False
    elif label == "+/-":
        if display and display != "0" and display != "Error":
            if display.startswith("-"):
                display = display[1:]
            else:
                display = "-" + display
        # formula is not changed for +/-
    st.session_state["calc_display"] = display
    st.session_state["calc_formula"] = formula
    st.session_state["calc_show_result"] = st.session_state.get("calc_show_result", False)
    # Removed unconditional st.rerun() to prevent infinite rerun loop
