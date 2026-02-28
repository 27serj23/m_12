# store/tests/test_sorting.py
from django.test import TestCase
from ..sorting import merge_sort  # импорт из нашего модуля


class MergeSortTest(TestCase):
    """
    Проверяет правильность реализации сортировки слиянием.
    Сравнивает результат с встроенной функцией sorted().
    """

    def test_empty_array(self):
        """Пустой список должен оставаться пустым."""
        self.assertEqual(merge_sort([]), [])

    def test_single_element(self):
        """Список из одного элемента не меняется."""
        self.assertEqual(merge_sort([5]), [5])

    def test_sorted_array(self):
        """Уже отсортированный список остаётся без изменений."""
        sorted_arr = list(range(10))
        self.assertEqual(merge_sort(sorted_arr), sorted_arr)

    def test_reverse_sorted_array(self):
        """Список, отсортированный в обратном порядке."""
        reverse_arr = list(reversed(range(10)))
        expected = list(range(10))
        self.assertEqual(merge_sort(reverse_arr), expected)

    def test_random_ordered_array(self):
        """Случайный порядок чисел."""
        random_arr = [9, 3, 7, 1, 5, 8, 2, 6, 4, 0]
        expected = sorted(random_arr)
        self.assertEqual(merge_sort(random_arr), expected)

    def test_duplicate_elements(self):
        """Наличие дубликатов."""
        duplicate_arr = [5, 3, 5, 1, 3, 8, 8]
        expected = sorted(duplicate_arr)
        self.assertEqual(merge_sort(duplicate_arr), expected)

    def test_negative_numbers(self):
        """Отрицательные числа."""
        negative_arr = [-5, -3, -7, -1, -9]
        expected = sorted(negative_arr)
        self.assertEqual(merge_sort(negative_arr), expected)

    def test_mixed_signs(self):
        """Смешанные положительные и отрицательные числа."""
        mixed_arr = [-5, 3, -7, 1, 9, -2]
        expected = sorted(mixed_arr)
        self.assertEqual(merge_sort(mixed_arr), expected)

    def test_large_array(self):
        """Проверка на массиве из 1000 элементов (для уверенности)."""
        large_arr = [i // 2 for i in range(1000, 0, -1)]  # 1000 элементов с повторениями
        expected = sorted(large_arr)
        self.assertEqual(merge_sort(large_arr), expected)