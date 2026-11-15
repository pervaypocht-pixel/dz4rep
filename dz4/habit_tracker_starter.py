
import json
import os

import pandas as pd
import plotly.express as px
import streamlit as st

DATA_FILE = "habit_data_sample.json"


def load_data() -> list:
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(records: list) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)



st.title("📊 Habit Tracker Dashboard")
st.write("Записуй свою щоденну активність — я збережу дані і покажу статистику.")


with st.form("new_record"):
    date = st.date_input("Дата")

    category = st.selectbox(
        "Категорія",
        [
            "Навчання",
            "Спорт",
            "Читання",
            "Малювання",
            "Програмування",
            "Медитація",
            "Гра на інструментах",
            "Інше"
        ]
    )

    minutes = st.number_input(
        "Скільки хвилин?",
        min_value=1,
        max_value=600,
        value=30
    )

    submitted = st.form_submit_button("➕ Додати запис")


if submitted:
    records = load_data()

    new_record = {
        "date": str(date),
        "category": category,
        "minutes": int(minutes)
    }

    records.append(new_record)
    save_data(records)

    st.success("Запис успішно збережено! ✅")


records = load_data()

if len(records) > 0:

    df = pd.DataFrame(records)

    
    df["date"] = pd.to_datetime(df["date"])

    
    st.subheader("📋 Усі записи")
    st.dataframe(df, use_container_width=True)

    
    total_minutes = df["minutes"].sum()

    st.subheader("📊 Загальна статистика")
    st.metric("Загальний час", f"{total_minutes} хвилин")

    
    by_category = (
        df.groupby("category")["minutes"]
        .sum()
        .reset_index()
    )

    
    by_day = (
        df.groupby("date")["minutes"]
        .sum()
        .reset_index()
        .sort_values("date")
    )

    
    st.subheader("📊 Час за категоріями")

    fig_bar = px.bar(
        by_category,
        x="category",
        y="minutes",
        title="Час за категоріями",
        labels={
            "category": "Категорія",
            "minutes": "Хвилини"
        }
    )

    st.plotly_chart(fig_bar, use_container_width=True)

    # Лінійний графік
    st.subheader("📈 Динаміка активності по днях")

    fig_line = px.line(
        by_day,
        x="date",
        y="minutes",
        title="Динаміка по днях",
        markers=True,
        labels={
            "date": "Дата",
            "minutes": "Хвилини"
        }
    )

    st.plotly_chart(fig_line, use_container_width=True)

    
    st.subheader("🥧 Розподіл часу за категоріями")

    fig_pie = px.pie(
        by_category,
        names="category",
        values="minutes",
        title="Частка кожної категорії в загальному часі",
        hole=0.3
    )

    st.plotly_chart(fig_pie, use_container_width=True)

else:
    st.info("Поки що записів немає. Додай свій перший запис! 👆")