import random


def get_rounds():
    while True:
        try:
            rounds = int(input("Сколько загадок вы хотите отгадать? (Введите число от 1 до 19): "))
            if 1 <= rounds <= 19:
                return rounds
            else:
                print("Пожалуйста, введите число от 1 до 19.")
        except ValueError:
            print("Ошибка: нужно ввести число!")


def get_hint(answer, hint_counter):
    return answer[hint_counter]


def riddle_game(riddles, rounds):
    right_answer = 0
    wrong_answer = 0

    for riddle, answer in random.sample(list(riddles.items()), rounds):
        print("\nЗагадка:", riddle)
        hint_counter = 0

        while True:
            user_input = input("Ваш ответ (или напишите 'подсказка' для подсказки): ").strip().lower()

            if user_input == 'подсказка':
                if hint_counter < len(answer):
                    hint_letter = get_hint(answer, hint_counter)
                    print(f"Подсказка: буква '{hint_letter}'")
                    hint_counter += 1
                else:
                    print("Вам наподсказывали всё слово...")
                continue

            if user_input == answer.lower():
                print("Правильно! Вы получаете 1 очко.")
                right_answer += 1
                break
            else:
                print(f"Неправильно. Правильный ответ - {answer}.")
                wrong_answer += 1
                break

    print(f"\nИгра окончена! Правильно отгадано: {right_answer}, неправильно: {wrong_answer}. Всего было"
          f" {rounds} загадок.")
    return right_answer, wrong_answer


def load_results(filename):
    results = {}
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line_number, line in enumerate(file, 1):
                try:
                    parts = line.strip().split(", ")
                    if len(parts) < 4:
                        raise ValueError(f"Некорректная строка на {line_number}: {line}")

                    player_name = parts[0].split(": ")[1]
                    correct = int(parts[1].split(": ")[1])
                    incorrect = int(parts[2].split(": ")[1].split('.')[0])
                    total = int(parts[3].split(": ")[1])

                    results[player_name] = (correct, incorrect, total)
                except (ValueError, IndexError) as e:
                    print(f"Ошибка в строке {line_number}: {e}. Строка будет пропущена.")
    except FileNotFoundError:
        print(f"Файл '{filename}' не найден. Результаты будут записаны при первом сохранении.")
    return results


def save_results(filename, results):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            for player_name, (correct, incorrect, total) in results.items():
                file.write(f"Имя игрока: {player_name}, правильно отгадано: {correct}, "
                           f"неправильно: {incorrect}. Всего загадок: {total}.\n")
        print('Результаты сохранены!')
    except Exception as e:
        print(f"Ошибка при записи в файл: {e}")


def saving_res(filename, rounds, name, right_answer, wrong_answer):
    results = load_results(filename)

    if name in results:
        merge_choice = input(f"Имя '{name}' уже существует. Объединить результаты? да/нет: ").strip().lower()
        if merge_choice == 'да':
            existing_correct, existing_incorrect, existing_total = results[name]
            results[name] = (existing_correct + right_answer,
                             existing_incorrect + wrong_answer,
                             existing_total + rounds)
        else:
            name = input("Введите новое имя для сохранения результата: ").strip()

    results[name] = (right_answer, wrong_answer, rounds)
    save_results(filename, results)


def main():
    print('Добро пожаловать в игру "Загадки"!')
    name = input("Введите ваше имя: ").strip()
    filename = 'riddles_result2.txt'
    riddles = {
        "Под гору — коняшка, в гору — деревяшка.": "Санки",
        "На деревья, на кусты с неба падают цветы. Белые, пушистые, только не душистые.": "Снег",
        "Сидит в темнице, красная девица, а коса на улице. (ответ без суффикса -ка)": "Морковь",
        "Зимой — звезда, весной — вода.": "Снежинка",
        "Кто зимой холодной ходит злой, голодный?": "Волк",
        "Не лает, не кусает, а в дом не пускает.": "Замок",
        "Сто одёжек и все без застежек.": "Капуста",
        "Сидит дед, в шубу одет, кто его раздевает, тот слёзы проливает.": "Лук",
        "Белые поросятки прилегли на грядке.": "Кабачки",
        "И сияет, и блестит, никому оно не льстит.": "Зеркало",
        "В доску спрячется бедняжка — чуть видна его фуражка.": "Гвоздь",
        "Зимой и летом одним цветом.": "Ёлка",
        "Сперва блеск, за блеском — треск!": "Гроза",
        "Рыжая плутовка, хитрая да ловкая, в сарай попала, кур пересчитала.": "Лиса",
        "По лужку он важно бродит, из воды сухим выходит, носит красные ботинки, дарит мягкие перинки.": "Гусь",
        "К нам приехали с бахчи полосатые мячи.": "Арбуз",
        "Белые горошки на зелёной ножке.": "Ландыш",
        "Зубы в пасти в три ряда. Это целая беда. Этот хищник знаменит тем, что он — морской бандит.": "Акула",
        "У представителей какой профессии в килограмме ровно 1024 грамма?": "Программист"
    }

    rounds = get_rounds()
    right_answer, wrong_answer = riddle_game(riddles, rounds)

    save_choice = input("Хотите сохранить результат? да/нет: ").strip().lower()
    if save_choice == 'да':
        saving_res(filename, rounds, name, right_answer, wrong_answer)


main()

if __name__ == "__main__":
    main()
