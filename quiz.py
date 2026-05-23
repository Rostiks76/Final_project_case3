"""
Модуль с основной логикой викторины.
"""

import random
from typing import List, Tuple

from models import Question


def run_quiz(questions: List[Question]) -> Tuple[int, int]:
    """
    Запускает процесс опроса пользователя.
    Вопросы выводятся в случайном порядке.
    
    Args:
        questions: Список вопросов викторины
        
    Returns:
        Кортеж (количество правильных ответов, общее количество вопросов)
    """
    # Перемешиваем вопросы
    shuffled_questions = random.sample(questions, len(questions))
    
    correct_count = 0
    total = len(shuffled_questions)
    
    print("\n" + "=" * 60)
    print("🎯 НАЧАЛО ВИКТОРИНЫ!")
    print("=" * 60)
    
    for idx, question in enumerate(shuffled_questions, 1):
        print(f"\n📌 Вопрос {idx}/{total}: {question.text}")
        print("-" * 40)
        
        # Выводим варианты ответов
        for opt_idx, option in enumerate(question.options, 1):
            print(f"   {opt_idx}. {option}")
        
        # Получаем ответ пользователя
        while True:
            try:
                answer = int(input("\n👉 Ваш ответ (1-4): "))
                if 1 <= answer <= 4:
                    break
                else:
                    print("❌ Пожалуйста, введите число от 1 до 4!")
            except ValueError:
                print("❌ Пожалуйста, введите число!")
        
        # Проверяем правильность
        if question.is_correct(answer):
            print("✅ Правильно!")
            correct_count += 1
        else:
            correct_text = question.options[question.correct_idx - 1]
            print(f"❌ Неправильно! Правильный ответ: {correct_text}")
    
    return correct_count, total


def calculate_score(correct: int, total: int) -> int:
    """
    Вычисляет процент правильных ответов.
    
    Args:
        correct: Количество правильных ответов
        total: Общее количество вопросов
        
    Returns:
        Процент правильных ответов (округлённый до целого)
    """
    if total == 0:
        return 0
    return round((correct / total) * 100)