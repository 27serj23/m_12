# store/sorting.py
def merge_sort(arr):
    """
    Сортирует список методом слияния (merge sort).
    Возвращает новый отсортированный список, исходный не изменяется.
    """
    def _merge(left, right):
        """Слияние двух отсортированных списков."""
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        # Добавляем оставшиеся элементы
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    # Базовый случай: список из 0 или 1 элемента уже отсортирован
    if len(arr) <= 1:
        return arr[:]  # возвращаем копию, чтобы не мутировать исходный

    mid = len(arr) // 2
    left_half = merge_sort(arr[:mid])
    right_half = merge_sort(arr[mid:])
    return _merge(left_half, right_half)