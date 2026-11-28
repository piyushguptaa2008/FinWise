
import streamlit as st
import sqlite3
from html import escape
from storage import initialize_database, get_db_path
import streamlit.components.v1 as components
from pathlib import Path
import re



def savings_connection():
    if "savings_connection" not in st.session_state:
        st.session_state.savings_connection = sqlite3.connect(
            get_db_path(), check_same_thread=False
        )
    return st.session_state.savings_connection


def show_savings():

    initialize_database()

    dark = st.session_state.get("dark_mode", False)

    ink = "#e1ebcd" if dark else "#171717"
    surface = "#242e28" if dark else "#fffdf8"
    green = "#344b36" if dark else "#e1ebcd"
    purple = "#41394e" if dark else "#e8e0f2"
    yellow = "#494535" if dark else "#f6ebcb"
    track = "#354438" if dark else "#e5eadc"

    # CREATE SAVINGS DATABASE TABLE

    with savings_connection() as conn:

        conn.execute("""
            CREATE TABLE IF NOT EXISTS savings_goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                target INTEGER NOT NULL,
                saved INTEGER NOT NULL DEFAULT 0
            )
        """)



   

    st.html(f"""
<div style="
    background:linear-gradient(135deg,{green},{purple},{yellow});
    padding:35px;
    border-radius:26px;
    color:{ink};
">
    <div style="letter-spacing:3px;font-size:12px">
        SAVINGS STUDIO
    </div>

    <div style="font-size:clamp(32px,4vw,52px);font-weight:800;letter-spacing:-2px">
        Dream bigger.<br>Save smarter.
    </div>

    <div style="font-size:17px;margin-top:12px">
        Turn your dreams into achievable goals.
    </div>
</div>

<style>

[data-testid="stMain"] .stButton button {{
    background:{green} !important;
    color:{ink} !important;
    border-radius:14px !important;
    border:1px solid #91b475 !important;
    min-height:45px;
}}

[data-testid="stMain"] .stButton button p {{
    color:{ink} !important;
}}

[data-testid="stMain"] input::placeholder {{
    color:{ink} !important;
    opacity:0.6;
}}

[data-testid="stMain"] label p {{
    color:{ink} !important;
}}

@keyframes savingsGrow {{
    from {{transform:scaleX(0);}}
    to {{transform:scaleX(1);}}
}}

.savings-progress {{
    transform-origin:left;
    animation:savingsGrow 0.8s ease-out;
}}

@media (prefers-reduced-motion:reduce) {{
    .savings-progress {{
        animation:none;
    }}
}}

</style>
""")

    summary = st.container()

    left, right = st.columns(2)

    # CREATE NEW GOAL

    with left:

        st.subheader("✦ Create a savings goal")

        with st.form("create_savings_goal"):

            name = st.text_input(
                "Goal name",
                placeholder="New laptop, vacation..."
            )

            target = st.number_input(
                "Target amount (₹)",
                min_value=1.0,
                max_value=100000000.0,
                step=500.0
            )

            create = st.form_submit_button(
                "＋ Create Goal",
                use_container_width=True
            )

            if create:

                if name.strip():

                    with savings_connection() as conn:

                        conn.execute("""
                            INSERT INTO savings_goals
                            (name, target, saved)
                            VALUES (?, ?, 0)
                        """, (
                            name.strip(),
                            round(target * 100)
                        ))

                    st.success("Savings goal created!")

                else:
                    st.warning("Enter a goal name.")

    # LOAD SAVINGS GOALS

    with savings_connection() as conn:

        goals = conn.execute("""
            SELECT id, name, target, saved
            FROM savings_goals
            ORDER BY id DESC
        """).fetchall()

    # ADD SAVINGS

    with right:

        st.subheader("₹ Add to your savings")

        active_goals = {
            g[0]: g for g in goals
            if g[3] < g[2]
        }

        if active_goals:

            with st.form("add_savings_form"):

                selected = st.selectbox(
                    "Select your goal",
                    list(active_goals),
                    format_func=lambda i: active_goals[i][1]
                )

                amount = st.number_input(
                    "Savings amount (₹)",
                    min_value=1.0,
                    max_value=100000000.0,
                    step=100.0
                )

                add = st.form_submit_button(
                    "＋ Add Savings",
                    use_container_width=True
                )

                if add:

                    with savings_connection() as conn:

                        goal = conn.execute("""
                            SELECT target, saved
                            FROM savings_goals
                            WHERE id = ?
                        """, (selected,)).fetchone()

                        if goal:

                            target, previous = goal

                            new_saved = (
                                previous + round(amount * 100)
                            )

                            conn.execute("""
                                UPDATE savings_goals
                                SET saved = ?
                                WHERE id = ?
                            """, (new_saved, selected))

                            conn.commit()

                            st.session_state["gullak_deposit"] = True

                            st.session_state["gullak_goal_achieved"] = (
                                previous < target <= new_saved
                            )

                            st.rerun()
                            st.balloons()

                            st.success(
                                    "Congratulations! "
                                    "You achieved your savings goal!"
                                )

                        else:

                         st.success(
                                    "Savings added successfully!"
                                )

        else:

            st.info("Create a new goal to start saving.")


    # SMART GULLAK

    import re
    from pathlib import Path
    import streamlit.components.v1 as components

    with savings_connection() as conn:
        saved, target = conn.execute("""
            SELECT COALESCE(SUM(saved), 0),
                   COALESCE(SUM(target), 0)
            FROM savings_goals
        """).fetchone()

    ratio = min(saved / target, 1) if target else 0

    deposited = st.session_state.pop("gullak_deposit", False)
    achieved = st.session_state.pop("gullak_goal_achieved", False)

    html = (Path(__file__).parent / "finwise-gullak.html").read_text(encoding="utf-8")

    html = re.sub(r"<script\b[^>]*>.*?</script>", "", html, flags=re.S | re.I)

    html = re.sub(
        r'<div id="status" class="status">.*?</div>',
        f'<div class="status">₹{saved / 100:,.2f} saved</div>',
        html,
        flags=re.S
    )

    css = f"""
    <style>
    body {{ background: transparent; }}
    .fwstage {{ height: 340px; width: 100%; }}
    .fwstage svg {{ height: 260px; margin-top: 10px; }}
    .brand, .eyebrow {{ display: none; }}
    .level {{
        animation: none !important;
        transform: scaleY({ratio});
    }}
    .bar {{
        animation: none !important;
        width: {ratio * 100}%;
    }}
    .m2, .m3, .m4 {{ display: none; }}
    .money, .jar, .lid, .ring, .star, .success {{
        animation-iteration-count: {1 if deposited else 0} !important;
    }}
    .ring, .star, .success {{
        display: {"inline" if achieved and deposited else "none"};
    }}
    </style>
    """

    html = html.replace("</head>", css + "</head>")

    # GULLAK COIN SOUND

    
           # GULLAK COIN SOUND
    if deposited:
        import base64
        from pathlib import Path

        audio_path = Path(__file__).parent / "coins.mp3"

        audio_data = base64.b64encode(
            audio_path.read_bytes()
        ).decode()

        sound_script = f"""
        <audio id="coinSound"
            src="data:audio/mpeg;base64,{audio_data}">
        </audio>

        <script>
            const sound = document.getElementById("coinSound");
            sound.volume = 0.9;

            setTimeout(() => {{
                sound.play().catch(() => {{}});
            }}, 1500);
        </script>
        """

        html = html.replace("</body>", sound_script + "</body>")

    components.html(html, height=370, scrolling=False)


    if achieved:

        confetti = ""

        colors = [
            "#B6CA91",
            "#DDBD64",
            "#B6A2D2",
            "#DCA1AA"
        ]

        for i in range(45):
            confetti += f"""
            <span style="
                position:absolute;
                top:-20px;
                left:{(i * 37) % 100}%;
                width:9px;
                height:14px;
                background:{colors[i % 4]};
                border-radius:2px;
                animation:fwCelebrationFall
                2.5s ease-in {(i % 10) * 0.1}s both;
            "></span>
            """

        st.html(f"""
        <style>
            @keyframes fwCelebrationFall {{
                from {{
                    transform:translateY(0) rotate(0deg);
                    opacity:1;
                }}
                to {{
                    transform:translateY(300px) rotate(540deg);
                    opacity:0;
                }}
            }}

            @keyframes fwCelebrationGlow {{
                0%, 100% {{
                    box-shadow:0 0 10px #BCD49A;
                }}
                50% {{
                    box-shadow:0 0 35px #A8C48B;
                }}
            }}

            @media (prefers-reduced-motion: reduce) {{
                .fw-celebration,
                .fw-celebration span {{
                    animation:none !important;
                }}
            }}
        </style>

        <div class="fw-celebration" style="
            position:relative;
            overflow:hidden;
            background:#E4ECD5;
            padding:35px;
            border-radius:25px;
            text-align:center;
            color:#394536;
            animation:fwCelebrationGlow 2s ease 2;
        ">
            {confetti}

            <div style="font-size:50px;">🏆</div>

            <p style="letter-spacing:4px;color:#627A4E;">
                ACHIEVEMENT UNLOCKED
            </p>

            <h1 style="color:#394536;">
                Goal achieved!
            </h1>

            <p style="color:#627A4E;">
                Your small steps made a big difference.
            </p>

            <h1 style="color:#48623D;">100%</h1>

            <div style="
                background:#A8C48B;
                height:10px;
                border-radius:20px;
            "></div>
        </div>
        """)

    elif deposited:
        st.success("Money added to your Gullak!")


    with savings_connection() as conn:

        goals = conn.execute("""
            SELECT id, name, target, saved
            FROM savings_goals
            ORDER BY id DESC
        """).fetchall()

    total_saved = sum(g[3] for g in goals) / 100
    completed = sum(g[3] >= g[2] for g in goals)

    # SUMMARY CARDS

    with summary:

        st.write("")

        cards = [
            ("Total Saved", f"₹{total_saved:,.2f}", green),
            ("Savings Goals", len(goals), purple),
            ("Goals Achieved", completed, yellow)
        ]

        for col, card in zip(st.columns(3), cards):

            label, value, color = card

            col.html(f"""
<div style="background:{color};color:{ink};
padding:25px;border-radius:22px">
    <div style="font-size:14px">{label}</div>
    <div style="font-size:30px;font-weight:800">
        {value}
    </div>
</div>
""")

    st.divider()

    # DISPLAY SAVINGS GOALS

    st.subheader("Your Savings Goals")

    if not goals:

        st.info("Your savings journey starts here.")

    for goal_id, name, target, saved in goals:

        percent = min(saved / target * 100, 100)

        remaining = max(target - saved, 0) / 100

        status = (
            "✓ Goal Achieved"
            if saved >= target
            else "In Progress"
        )

        st.html(f"""
<div style="
    background:{surface};
    color:{ink};
    padding:25px;
    border-radius:24px;
    border:1px solid #91b47540;
    margin-bottom:15px;
">

    <div style="display:flex;justify-content:space-between;gap:12px">

        <div>
            <div style="font-size:24px;font-weight:800">
                {escape(name)}
            </div>

            <small>{status}</small>
        </div>

        <div style="font-size:28px;font-weight:800">
            {percent:.0f}%
        </div>

    </div>

    <div style="margin-top:18px">
        ₹{saved/100:,.2f} saved
        / ₹{target/100:,.2f}
    </div>

    <div style="background:{track};height:13px;
    border-radius:20px;overflow:hidden;margin:15px 0">

        <div class="savings-progress"
        style="background:linear-gradient(90deg,#b8d29d,#78965b);
        width:{percent}%;height:100%;border-radius:20px">
        </div>

    </div>

    <div style="font-size:14px">
        ₹{remaining:,.2f} remaining
    </div>

</div>
""")
