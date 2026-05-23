#!/usr/bin/env python3
"""
Главный модуль приложения "Викторина".
Запускает интерактивный тест с подсчетом баллов и таблицей лидеров.
"""

import random
import sys
from typing import List

from database import init_database, get_all_questions, save_score, get_leaderboard
from models import Question, LeaderboardEntry
from quiz import run_quiz, calculate_score
from leaderboard import display_leaderboard


def get_player_name() -> str:
    """
    Запрашивает имя игрока у пользователя.
    
    Returns:
        Введённое имя (очищенное от лишних пробелов)
    """
    while True:
        name = input("\n👤 Введите ваше имя: ").strip()
        if name:
            return name
        print("❌ Имя не может быть пустым!")


def show_menu() -> str:
    """
    Отображает главное меню и возвращает выбор пользователя.
    
    Returns:
        Выбранный пункт меню ('1', '2', '3')
    """
    print("\n" + "=" * 60)
    print("📚 ГЛАВНОЕ МЕНЮ")
    print("=" * 60)
    print("1. 🎯 Начать викторину")
    print("2. 🏆 Показать таблицу лидеров")
    print("3. 🚪 Выйти")
    print("-" * 60)
    
    while True:
        choice = input("👉 Ваш выбор (1-3): ").strip()
        if choice in ('1', '2', '3'):
            return choice
        print("❌ Неверный выбор! Введите 1, 2 или 3.")


def convert_to_leaderboard_entries(rows: List[dict]) -> List[LeaderboardEntry]:
    """
    Преобразует записи из БД в объекты LeaderboardEntry.
    
    Args:
        rows: Список словарей с ключами player_name, score, date_played
        
    Returns:
        Список объектов LeaderboardEntry
    """
    entries = []
    for row in rows:
        entries.append(LeaderboardEntry(
            player_name=row["player_name"],
            score=row["score"],
            date_played=row["date_played"]
        ))
    return entries


def main() -> None:
    """
    Главная функция приложения.
    Инициализирует БД, запускает основной цикл программы.
    """
    print("\n" + "🎓" * 30)
    print("   ДОБРО ПОЖАЛОВАТЬ В ВИКТОРИНУ!")
    print("🎓" * 30)
    
    # Инициализируем базу данных
    init_database()
    
    # Загружаем вопросы
    questions_data = get_all_questions()
    questions = [
        Question(
            id=q["id"],
            text=q["text"],
            options=q["options"],
            correct_idx=q["correct_idx"]
        )
        for q in questions_data
    ]
    
    if not questions:
        print("\n⚠️ В базе данных нет вопросов! Добавьте вопросы вручную.")
        return
    
    # Основной цикл программы
    while True:
        choice = show_menu()
        
        if choice == '1':
            # Запуск викторины
            name = get_player_name()
            correct, total = run_quiz(questions)
            score = calculate_score(correct, total)
            
            print("\n" + "=" * 60)
            print("📊 РЕЗУЛЬТАТ ВИКТОРИНЫ")
            print("=" * 60)
            print(f"   👤 Игрок: {name}")
            print(f"   ✅ Правильных ответов: {correct} из {total}")
            print(f"   📈 Процент успеха: {score}%")
            print("=" * 60)
            
            # Сохраняем результат
            save_score(name, score)
            
            input("\nНажмите Enter, чтобы продолжить...")
        
        elif choice == '2':
            # Показ таблицы лидеров
            leaderboard_data = get_leaderboard(limit=10)
            entries = convert_to_leaderboard_entries(leaderboard_data)
            display_leaderboard(entries)
            input("\nНажмите Enter, чтобы продолжить...")
        
        elif choice == '3':
            # Выход из программы
            print("\n👋 Спасибо за игру! До новых встреч!")
            sys.exit(0)


if __name__ == "__main__":
    main()