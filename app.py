import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Настройка страницы
st.set_page_config(page_title="Гармония в общении", page_icon="💬", layout="wide")

# Стили: крупные ползунки + анимация смайликов
st.markdown("""
<style>
    /* Увеличиваем ползунки */
    .stSlider > div > div > div {
        height: 12px !important;
        border-radius: 6px !important;
    }
    .stSlider > div > div > div > div {
        height: 24px !important;
        width: 24px !important;
        border-radius: 50% !important;
        background-color: #a67c9f !important;
        border: 2px solid white !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.2) !important;
    }

    /* Анимация для смайликов */
    .emoji-container {
        text-align: center;
        font-size: 40px;
        margin: 12px auto 20px;
        transition: transform 0.3s ease, opacity 0.3s ease;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    /* Мягкий фон */
    .reportview-container { background: #fdf6f0; }
    .sidebar .sidebar-content { background: #faf3ec; }
    h1, h2, h3 { color: #5a4a66; }
</style>
""", unsafe_allow_html=True)

st.title("💬 Гармония в общении: как вам двоим комфортно вместе?")

# === Вспомогательные функции для смайликов ===
def render_emoji(val, low_emoji, mid_emoji, high_emoji):
    if val <= 3:
        emoji = low_emoji
    elif val <= 6:
        emoji = mid_emoji
    else:
        emoji = high_emoji
    # Анимированный контейнер
    st.markdown(f"""
    <div class="emoji-container" style="opacity: 0.95;">
        {emoji}
    </div>
    """, unsafe_allow_html=True)

# === СБОР ДАННЫХ ===
st.header("Расскажите немного о вас и вашем собеседнике")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Вы")
    
    openness_a = st.slider("Любознательность и открытость новому", 1, 10, 7)
    render_emoji(openness_a, "🤖", "🙂", "✨")
    
    conscientiousness_a = st.slider("Организованность и надёжность", 1, 10, 6)
    render_emoji(conscientiousness_a, "🌀", "🙂", "🎯")
    
    extraversion_a = st.slider("Общительность и энергия в компании", 1, 10, 8)
    render_emoji(extraversion_a, "🕯️", "🙂", "🌟")
    
    agreeableness_a = st.slider("Доброта и умение идти на компромисс", 1, 10, 5)
    render_emoji(agreeableness_a, "😤", "🙂", "💖")
    
    neuroticism_a = st.slider("Эмоциональная устойчивость", 1, 10, 3)
    render_emoji(neuroticism_a, "🧘‍♀️", "😐", "🌧️")

with col2:
    st.subheader("Ваш собеседник / партнёр")
    
    openness_b = st.slider("Любознательность и открытость новому", 1, 10, 5)
    render_emoji(openness_b, "🤖", "🙂", "✨")
    
    conscientiousness_b = st.slider("Организованность и надёжность", 1, 10, 9)
    render_emoji(conscientiousness_b, "🌀", "🙂", "🎯")
    
    extraversion_b = st.slider("Общительность и энергия в компании", 1, 10, 4)
    render_emoji(extraversion_b, "🕯️", "🙂", "🌟")
    
    agreeableness_b = st.slider("Доброта и умение идти на компромисс", 1, 10, 8)
    render_emoji(agreeableness_b, "😤", "🙂", "💖")
    
    neuroticism_b = st.slider("Эмоциональная устойчивость", 1, 10, 6)
    render_emoji(neuroticism_b, "🧘‍♀️", "😐", "🌧️")

st.header("Как вы взаимодействуете?")

col3, col4 = st.columns(2)

with col3:
    relationship_type = st.selectbox("Тип ваших отношений", 
        ["Коллеги", "Друзья", "Семья", "Партнёры"])
    power_distance = st.slider("Насколько вы равны в этих отношениях?", -5, 5, 0, 
                               help="-5: один сильно доминирует → 0: равные партнёры → +5: другой доминирует")
    trust_level = st.slider("Насколько вы доверяете друг другу?", 1, 10, 7)

with col4:
    communication_style = st.selectbox("Как вы обычно общаетесь?", 
        ["Спокойно и уважительно", "По-дружески", "Иногда возникают споры", "Стараемся находить общий язык"])
    time_pressure = st.slider("Часто ли вам нужно принимать решения в спешке?", 1, 10, 3)
    setting_formality = st.slider("Насколько формальны ваши встречи?", 1, 10, 5)

# === ВКЛАДКИ ===
tab1, tab2, tab3, tab4 = st.tabs(["📊 Ваши профили", "🌈 Как вы похожи?", "🔍 Что важно учитывать?", "💌 Советы для вас"])

with tab1:
    st.info("Здесь вы видите, как вы и ваш собеседник воспринимаете мир. Нет «хорошо» или «плохо» — просто разные способы быть собой ❤️")

with tab2:
    st.header("Ваши профили рядом")
    
    categories = ['Любознательность', 'Организованность', 'Общительность', 'Доброта', 'Эмоциональная устойчивость']
    values_a = [openness_a, conscientiousness_a, extraversion_a, agreeableness_a, neuroticism_a]
    values_b = [openness_b, conscientiousness_b, extraversion_b, agreeableness_b, neuroticism_b]
    
    fig, ax = plt.subplots(figsize=(10, 8), subplot_kw=dict(projection='polar'))
    angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False).tolist()
    values_a += values_a[:1]
    values_b += values_b[:1]
    angles += angles[:1]
    
    ax.plot(angles, values_a, 'o-', linewidth=2, label='Вы', color='#a67c9f')
    ax.fill(angles, values_a, alpha=0.25, color='#a67c9f')
    ax.plot(angles, values_b, 'o-', linewidth=2, label='Ваш собеседник', color='#6b9ca9')
    ax.fill(angles, values_b, alpha=0.25, color='#6b9ca9')
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=11)
    ax.set_ylim(0, 10)
    ax.legend(loc='upper right')
    ax.grid(True, color='#d4c1b0')
    st.pyplot(fig)

with tab3:
    st.header("Что помогает вам понимать друг друга?")
    
    similarity = 1 - (np.abs(np.array(values_a[:-1]) - np.array(values_b[:-1])).mean() / 10)
    harmony = (min(extraversion_a, extraversion_b) + min(agreeableness_a, agreeableness_b)) / 20
    emotional_gap = (abs(agreeableness_a - agreeableness_b) + abs(neuroticism_a - neuroticism_b)) / 20
    overall = (similarity + harmony + (1 - emotional_gap)) / 3
    
    data = {
        'Аспект': ['Похожесть взглядов', 'Взаимодополнение', 'Эмоциональная близость', 'Общая гармония'],
        'Оценка': [similarity, harmony, 1 - emotional_gap, overall]
    }
    df = pd.DataFrame(data)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ['#d4a5a5', '#a8c3b1', '#c2b4d4', '#f0c9a9']
    bars = ax.barh(df['Аспект'], df['Оценка'], color=colors)
    ax.set_xlim(0, 1)
    ax.set_xlabel('Уровень')
    ax.set_title('Как вам комфортно вместе?')
    for bar, val in zip(bars, df['Оценка']):
        ax.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2, f'{val:.2f}', va='center')
    st.pyplot(fig)
    
    st.subheader("Что это значит для вас?")
    
    if overall > 0.7:
        st.success("✨ У вас прекрасная основа для доверительного общения! Вы чувствуете друг друга и умеете находить общий язык.")
    elif overall > 0.5:
        st.warning("🌱 Ваши отношения имеют потенциал! Небольшие усилия помогут вам лучше понимать друг друга.")
    else:
        st.error("🌧️ Возможно, вам стоит уделить внимание тому, как вы общаетесь. Это нормально — даже близкие люди иногда «говорят на разных языках».")
    
    st.write("### На что обратить внимание:")
    if abs(extraversion_a - extraversion_b) > 4:
        st.write("💬 **Общительность:** Один из вас заряжается в компании, другой — в тишине. Это не плохо, просто по-разному!")
    if agreeableness_a < 4 or agreeableness_b < 4:
        st.write("🤝 **Доброта:** В моменты напряжения важно помнить: за резкостью может скрываться усталость или страх.")
    if neuroticism_a > 7 or neuroticism_b > 7:
        st.write("🌧️ **Эмоциональная устойчивость:** Кому-то из вас может быть сложнее справляться со стрессом. Поддержка здесь важнее оценки.")

with tab4:
    st.header("Как сделать общение ещё теплее?")
    
    tips = []
    if abs(extraversion_a - extraversion_b) > 3:
        tips.append("✨ **Разные ритмы общения:** Если вы любите поговорить, а партнёр — помолчать, договоритесь: «Я поделюсь — и дам тебе время подумать».")
    if agreeableness_a < 5 and agreeableness_b < 5:
        tips.append("💬 **Мягкость в диалоге:** Попробуйте начинать с «Я чувствую…», а не «Ты всегда…» — это снижает напряжение.")
    if emotional_gap > 0.6:
        tips.append("💞 **Эмоциональная поддержка:** Просто спросите: «Как ты себя чувствуешь?» — иногда этого достаточно.")
    if similarity < 0.4:
        tips.append("🌈 **Цените различия:** То, что вы видите мир по-разному, — это шанс расти вместе, а не повод для споров.")
    if time_pressure > 7:
        tips.append("⏳ **Спешка и понимание:** В стрессе мы хуже слышим друг друга. Договоритесь: «Давай обсудим это, когда сможем уделить время».")
    
    if not tips:
        tips = [
            "🌷 **Продолжайте в том же духе!** Вы уже умеете слушать и слышать.",
            "💬 **Регулярно спрашивайте:** «Как тебе было в нашем разговоре?» — это укрепляет доверие.",
            "❤️ **Маленькие жесты важны:** Иногда достаточно сказать «Спасибо, что выслушал(а)»."
        ]
    
    for i, tip in enumerate(tips, 1):
        st.markdown(f"{i}. {tip}")

    st.download_button(
        label="📥 Сохранить советы",
        data=df.to_csv(index=False).encode('utf-8'),
        file_name='harmony_tips.csv',
        mime='text/csv',
    )

with st.sidebar:
    st.header("О чём это приложение?")
    st.write("""
    Здесь нет «теста» и «оценок».  
    Это инструмент, чтобы **лучше понять себя и другого человека** — без осуждения, с теплотой и уважением.
    """)
    st.info("🌸 Совет: проходите анализ вместе с близким человеком — это может стать началом тёплого разговора.")
