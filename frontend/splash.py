
import streamlit as st


def show_splash():

    if st.session_state.get("splash_shown", False):
        return

    st.markdown("""
<style>

#finwise-splash {
    position: fixed;
    inset: 0;
    z-index: 999999;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    overflow: hidden;
    background:
        radial-gradient(circle at 15% 20%, #f9dce4, transparent 45%),
        radial-gradient(circle at 85% 80%, #dce9ca, transparent 50%),
        #fff9ef;
    font-family: Arial, sans-serif;
    animation: splashExit 6s forwards;
}

.fw-logo {
    font-size: 65px;
    font-weight: 900;
    letter-spacing: -4px;
    color: #526b42;
    animation: logoEnter 1s ease-out both;
}

.fw-logo span {
    color: #dfa3b3;
}

.fw-tagline {
    color: #76866b;
    font-size: 12px;
    letter-spacing: 4px;
}

.fw-stage {
    position: relative;
    width: 300px;
    height: 280px;
    perspective: 900px;
}

/* Animated wallet */

.fw-wallet {
    position: absolute;
    top: 145px;
    left: 60px;
    width: 180px;
    height: 110px;
    background: #78965b;
    border-radius: 20px;
    box-shadow: 0 20px 35px #526b4240;
    animation: walletEnter 6s both;
}

.fw-pocket {
    position: absolute;
    inset: 25px 0 0;
    background: linear-gradient(135deg, #dcebc5, #9ebd7d);
    border: 2px solid #8da970;
    border-radius: 18px;
    z-index: 5;
}

.fw-pocket::after {
    content: "FINWISE";
    position: absolute;
    inset: 8px;
    border: 2px dashed #f5ffe4;
    border-radius: 12px;
    padding: 25px 12px;
    color: #526b42;
    font-size: 13px;
    font-weight: bold;
    letter-spacing: 3px;
}

.fw-lid {
    position: absolute;
    top: 0;
    width: 100%;
    height: 60px;
    border-radius: 18px;
    background: linear-gradient(135deg, #d4e7b8, #9dbd7d);
    transform-origin: top;
    z-index: 6;
    animation: openWallet 6s both;
}

.fw-button {
    position: absolute;
    right: -5px;
    top: 45px;
    width: 45px;
    height: 30px;
    border-radius: 8px;
    background: #e8afbd;
    color: #fff9ef;
    text-align: center;
    line-height: 30px;
    z-index: 7;
    animation: walletButton 6s both;
}

/* Flying banknotes */

.fw-money {
    position: absolute;
    left: 115px;
    top: 20px;
    width: 75px;
    height: 40px;
    display: grid;
    place-items: center;
    background: linear-gradient(135deg, #fce7ed, #e7a5b7);
    border: 2px solid #d49aaa;
    border-radius: 7px;
    font-weight: bold;
    color: #9c566a;
    opacity: 0;
    animation: flyMoney 4.5s var(--delay) both;
}

/* Golden coins */

.fw-coin {
    position: absolute;
    left: 135px;
    top: 20px;
    width: 36px;
    height: 36px;
    display: grid;
    place-items: center;
    border-radius: 50%;
    background: linear-gradient(135deg, #fff4bd, #e8c16a);
    border: 3px solid #dfb75e;
    color: #98702e;
    font-size: 23px;
    font-weight: bold;
    opacity: 0;
    animation: flyMoney 4.5s var(--delay) both;
}

/* Success checkmark */

.fw-success {
    position: absolute;
    left: 120px;
    top: 35px;
    width: 60px;
    height: 60px;
    background: #91b475;
    color: white;
    border-radius: 50%;
    display: grid;
    place-items: center;
    font-size: 35px;
    box-shadow: 0 0 0 12px #a8c68644;
    animation: successPop 6s both;
}

/* Celebration particles */

.fw-particle {
    position: absolute;
    left: 145px;
    top: 170px;
    font-size: 28px;
    color: var(--color);
    animation: celebration 6s both;
}

/* Loading progress bar */

.fw-track {
    width: 220px;
    height: 7px;
    border-radius: 20px;
    background: #e5e5d9;
    overflow: hidden;
    margin: 15px;
}

.fw-progress {
    height: 100%;
    background: linear-gradient(90deg, #91b475, #e8afbd);
    border-radius: 20px;
    animation: loading 5.4s linear forwards;
}

.fw-loading-text {
    color: #526b42;
    font-size: 15px;
    font-weight: bold;
}

.fw-caption {
    color: #a17a85;
    font-size: 12px;
}

/* Animation keyframes */

@keyframes logoEnter {
    from {
        opacity: 0;
        transform: translateY(-30px) scale(0.7);
    }
    to {
        opacity: 1;
        transform: scale(1);
    }
}

@keyframes walletEnter {
    0%, 5% {
        opacity: 0;
        transform: translateY(100px) rotateY(-180deg) scale(0.3);
    }
    20% {
        opacity: 1;
        transform: rotateY(15deg) scale(1.1);
    }
    30%, 65% {
        opacity: 1;
        transform: scale(1);
    }
    75% {
        transform: scale(1.1, 0.95);
    }
    85% {
        transform: translateY(-15px) scale(1.1);
    }
    100% {
        opacity: 1;
        transform: scale(1);
    }
}

@keyframes openWallet {
    0%, 25%, 80%, 100% {
        transform: rotateX(0deg);
    }
    35%, 65% {
        transform: rotateX(175deg);
    }
}

@keyframes walletButton {
    0%, 20%, 80%, 100% {
        transform: none;
    }
    30%, 70% {
        transform: translateX(30px) rotate(-35deg);
    }
}

@keyframes flyMoney {
    0%, 30% {
        opacity: 0;
        transform: scale(0.2);
    }
    45% {
        opacity: 1;
        transform: translate(var(--x), -10px) rotate(-30deg);
    }
    65% {
        opacity: 1;
        transform: translate(calc(var(--x) * -0.7), 50px)
                   rotateY(180deg);
    }
    85% {
        opacity: 1;
        transform: translateY(110px) rotateY(360deg);
    }
    100% {
        opacity: 0;
        transform: translateY(165px) scale(0.2);
    }
}

@keyframes successPop {
    0%, 78% {
        opacity: 0;
        transform: scale(0);
    }
    86% {
        opacity: 1;
        transform: scale(1.3);
    }
    95%, 100% {
        opacity: 1;
        transform: scale(1);
    }
}

@keyframes celebration {
    0%, 78% {
        opacity: 0;
        transform: scale(0);
    }
    87% {
        opacity: 1;
        transform: translate(var(--x), var(--y)) rotate(90deg);
    }
    100% {
        opacity: 0;
        transform: translate(var(--x), var(--y)) scale(0.3);
    }
}

@keyframes loading {
    from { width: 0%; }
    to { width: 100%; }
}

@keyframes splashExit {
    0%, 92% {
        opacity: 1;
        visibility: visible;
    }
    100% {
        opacity: 0;
        visibility: hidden;
        transform: scale(1.1);
    }
}

@media (prefers-reduced-motion: reduce) {
    #finwise-splash {
        display: none;
    }
}

</style>

<div id="finwise-splash">

<div class="fw-logo">FinWise<span>.</span></div>

<div class="fw-tagline">SMARTER MONEY. SWEETER LIFE.</div>

<div class="fw-stage">

<div class="fw-wallet">
<div class="fw-pocket"></div>
<div class="fw-lid"></div>
<div class="fw-button">●</div>
</div>

<div class="fw-money" style="--x:-110px; --delay:0s;">₹500</div>
<div class="fw-money" style="--x:100px; --delay:0.2s;">₹200</div>
<div class="fw-money" style="--x:-70px; --delay:0.4s;">₹100</div>

<div class="fw-coin" style="--x:115px; --delay:0.1s;">₹</div>
<div class="fw-coin" style="--x:-120px; --delay:0.3s;">₹</div>
<div class="fw-coin" style="--x:65px; --delay:0.5s;">₹</div>

<div class="fw-success">✓</div>

<div class="fw-particle" style="--x:-120px; --y:-80px; --color:#e8afbd;">✦</div>
<div class="fw-particle" style="--x:120px; --y:-90px; --color:#91b475;">✧</div>
<div class="fw-particle" style="--x:-100px; --y:30px; --color:#e5bd69;">✦</div>
<div class="fw-particle" style="--x:100px; --y:40px; --color:#e8afbd;">♥</div>
<div class="fw-particle" style="--x:40px; --y:-130px; --color:#e5bd69;">✦</div>
<div class="fw-particle" style="--x:-50px; --y:-120px; --color:#91b475;">✧</div>

</div>

<div class="fw-loading-text">Making every rupee count...</div>

<div class="fw-track">
<div class="fw-progress"></div>
</div>

<div class="fw-caption">Little savings, brighter future.</div>

</div>

""", unsafe_allow_html=True)

    st.session_state["splash_shown"] = True
