class ListUtils:
    @staticmethod
    def concatenate_unique_lists(list1: list, list2: list) -> list:
        set1 = set(list1)
        set2 = set(list2)

        remainder = list(set2 - set1)

        return list1 + remainder
