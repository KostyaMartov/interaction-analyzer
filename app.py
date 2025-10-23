import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Настройка страницы
st.set_page_config(page_title="Анализ взаимодействия", page_icon="👥", layout="wide")

st.title("👥 Многофакторный анализ взаимодействия двух людей")

# === СБОР ДАННЫХ НА ВЕРХНЕМ УРОВНЕ (обязательно для Streamlit) ===

st.header("Параметры участников взаимодействия")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Человек А")
    a_openness = st.slider("Открытость опыту (А)", 1, 10, 7)
    a_conscientiousness = st.slider("Добросовестность (А)", 1, 10, 6)
    a_extraversion = st.slider("Экстраверсия (А)", 1, 10, 8)
    a_agreeableness = st.slider("Доброжелательность (А)", 1, 10, 5)
    a_neuroticism = st.slider("Невротизм (А)", 1, 10, 3)

with col2:
    st.subheader("Человек Б")
    b_openness = st.slider("Открытость опыту (Б)", 1, 10, 5)
    b_conscientiousness = st.slider("Добросовестность (Б)", 1, 10, 9)
    b_extraversion = st.slider("Экстраверсия (Б)", 1, 10, 4)
    b_agreeableness = st.slider("Доброжелательность (Б)", 1, 10, 8)
    b_neuroticism = st.slider("Невротизм (Б)", 1, 10, 6)

st.header("Параметры взаимодействия")

col3, col4 = st.columns(2)

with col3:
    relationship_type = st.selectbox("Тип отношений", 
        ["Профессиональные", "Дружеские", "Семейные", "Романтические"])
    power_distance = st.slider("Разница в статусе", -5, 5, 0)
    trust_level = st.slider("Уровень доверия", 1, 10, 7)

with col4:
    communication_style = st.selectbox("Стиль общения", 
        ["Формальный", "Неформальный", "Конфликтный", "Кооперативный"])
    time_pressure = st.slider("Временное давление", 1, 10, 3)
    setting_formality = st.slider("Формальность обстановки", 1, 10, 5)

# === ТЕПЕРЬ МОЖНО СОЗДАВАТЬ ВКЛАДКИ ===

tab1, tab2, tab3, tab4 = st.tabs(["📊 Ввод данных", "📈 Визуализация", "🔍 Анализ", "💡 Рекомендации"])

with tab1:
    st.info("Данные успешно введены! Перейдите на другие вкладки для анализа.")

with tab2:
    st.header("Визуализация профилей личности")
    
    categories = ['Открытость', 'Добросовестность', 'Экстраверсия', 'Доброжелательность', 'Невротизм']
    values_a = [a_openness, a_conscientiousness, a_extraversion, a_agreeableness, a_neuroticism]
    values_b = [b_openness, b_conscientiousness, b_extraversion, b_agreeableness, b_neuroticism]
    
    # Радар-чарт
    fig, ax = plt.subplots(figsize=(10, 8), subplot_kw=dict(projection='polar'))
    angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False).tolist()
    values_a += values_a[:1]
    values_b += values_b[:1]
    angles += angles[:1]
    
    ax.plot(angles, values_a, 'o-', linewidth=2, label='Человек А')
    ax.fill(angles, values_a, alpha=0.25)
    ax.plot(angles, values_b, 'o-', linewidth=2, label='Человек Б')
    ax.fill(angles, values_b, alpha=0.25)
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)
    ax.set_ylim(0, 10)
    ax.legend(loc='upper right')
    ax.grid(True)
    st.pyplot(fig)
    
    # Столбчатая диаграмма
    st.subheader("Сравнение параметров")
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    x = np.arange(len(categories))
    width = 0.35
    ax2.bar(x - width/2, values_a[:-1], width, label='Человек А')
    ax2.bar(x + width/2, values_b[:-1], width, label='Человек Б')
    ax2.set_xlabel('Черты личности')
    ax2.set_ylabel('Баллы')
    ax2.set_title('Сравнение профилей личности')
    ax2.set_xticks(x)
    ax2.set_xticklabels(categories)
    ax2.legend()
    st.pyplot(fig2)

with tab3:
    st.header("Анализ взаимодействия")
    
    # Расчёт метрик
    personality_similarity = 1 - (np.abs(np.array(values_a[:-1]) - np.array(values_b[:-1])).mean() / 10)
    complementarity_score = (min(a_extraversion, b_extraversion) + min(a_agreeableness, b_agreeableness)) / 20
    potential_conflict = (abs(a_agreeableness - b_agreeableness) + abs(a_neuroticism - b_neuroticism)) / 20
    
    data = {
        'Параметр': ['Сходство личностей', 'Комплементарность', 'Потенциал конфликта', 'Общая оценка'],
        'Значение': [
            personality_similarity,
            complementarity_score, 
            1 - potential_conflict,
            (personality_similarity + complementarity_score + (1 - potential_conflict)) / 3
        ]
    }
    df = pd.DataFrame(data)
    
    # График
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    colors = ['skyblue', 'lightgreen', 'lightcoral', 'gold']
    bars = ax3.barh(df['Параметр'], df['Значение'], color=colors)
    ax3.set_xlim(0, 1)
    ax3.set_xlabel('Оценка')
    ax3.set_title('Анализ качества взаимодействия')
    for bar, value in zip(bars, df['Значение']):
        ax3.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2, f'{value:.2f}', va='center')
    st.pyplot(fig3)
    
    # Интерпретация
    st.subheader("Интерпретация результатов")
    overall_score = df[df['Параметр'] == 'Общая оценка']['Значение'].values[0]
    if overall_score > 0.7:
        st.success("✅ Высокий потенциал эффективного взаимодействия. Партнеры хорошо дополняют друг друга.")
    elif overall_score > 0.5:
        st.warning("⚠️ Умеренный потенциал. Взаимодействие возможно, но требует усилий и компромиссов.")
    else:
        st.error("❌ Низкий потенциал. Высокий риск недопонимания и конфликтов.")
    
    st.write("### Детальный анализ:")
    if abs(a_extraversion - b_extraversion) > 4:
        st.write("- **Экстраверсия:** Большая разница в уровне общительности может создавать напряжение")
    if a_agreeableness < 4 or b_agreeableness < 4:
        st.write("- **Доброжелательность:** Низкие показатели могут указывать на склонность к конфронтации")
    if a_neuroticism > 7 or b_neuroticism > 7:
        st.write("- **Эмоциональная стабильность:** Высокий невротизм может осложнять взаимодействие")

with tab4:
    st.header("Рекомендации по оптимизации взаимодействия")
    
    recommendations = []
    if abs(a_extraversion - b_extraversion) > 3:
        recommendations.append("**Баланс общительности:** Экстраверту стоит давать возможность высказаться, интроверту — время на обдумывание")
    if a_agreeableness < 5 and b_agreeableness < 5:
        recommendations.append("**Развитие эмпатии:** Обоим партнерам стоит практиковать активное слушание и поиск компромиссов")
    if potential_conflict > 0.6:
        recommendations.append("**Управление конфликтами:** Установите четкие правила обсуждения разногласий")
    if personality_similarity < 0.4:
        recommendations.append("**Использование различий:** Рассматривайте различия как источник дополнительных перспектив")
    if time_pressure > 7:
        recommendations.append("**Тайм-менеджмент:** При высоком давлении используйте структурированные форматы встреч")
    
    if not recommendations:
        recommendations = [
            "**Поддержание текущего курса:** Параметры взаимодействия сбалансированы",
            "**Регулярная обратная связь:** Продолжайте обсуждать процесс взаимодействия",
            "**Развитие доверия:** Укрепляйте установившиеся позитивные паттерны"
        ]
    
    for i, rec in enumerate(recommendations, 1):
        st.write(f"{i}. {rec}")
    
    st.download_button(
        label="📥 Скачать отчет по анализу",
        data=df.to_csv(index=False).encode('utf-8'),
        file_name='interaction_analysis.csv',
        mime='text/csv',
    )

# Боковая панель
with st.sidebar:
    st.header("О методе анализа")
    st.write("""
    Этот инструмент оценивает взаимодействие на основе:
    - Пятифакторной модели личности
    - Социальных параметров
    - Контекста взаимодействия
    
    **Интерпретация шкал:**
    - 1-3: Низкий показатель
    - 4-7: Средний показатель  
    - 8-10: Высокий показатель
    """)
    st.info("💡 Для точного анализа используйте данные психологического тестирования и наблюдения за реальным взаимодействием.")
