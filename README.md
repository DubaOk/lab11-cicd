# Лабораторная 11: CI/CD с GitHub Actions

Простая веб-форма обратной связи с автоматическими UI-тестами (Selenium) и деплоем на GitHub Pages.

## Структура проекта

```
Lab_11/
├── index.html              # Веб-форма
├── style.css               # Стили
├── tests/
│   └── test_ui.py          # 4 UI-теста (Selenium)
├── requirements.txt        # Python-зависимости
├── .github/workflows/
│   └── ci.yml              # CI (тесты) + CD (GitHub Pages)
└── README.md
```

## Что нужно установить локально

1. **Git** — https://git-scm.com/
2. **Python 3.11+** — https://www.python.org/
3. **Google Chrome** — для Selenium-тестов

---

## Пошаговая инструкция

### Шаг 1. Создайте репозиторий на GitHub

1. Зайдите на https://github.com и нажмите **New repository**.
2. Название, например: `lab11-cicd`.
3. **Не** ставьте галочки «Add README» / «Add .gitignore» — репозиторий должен быть пустым.
4. Нажмите **Create repository**.
5. Скопируйте URL репозитория (например `https://github.com/ВАШ_ЛОГИН/lab11-cicd.git`).

### Шаг 2. Первый коммит и отправка в main

Откройте терминал в папке проекта `Lab_11` и выполните:

```powershell
cd d:\Labs_6_sem\TPO\Lab_11

git init
git add .
git commit -m "Initial commit: web form, Selenium tests, CI/CD workflow"

git branch -M main
git remote add origin https://github.com/ВАШ_ЛОГИН/lab11-cicd.git
git push -u origin main
```

Замените URL на свой.

### Шаг 3. Создайте ветки dev и fix

```powershell
git checkout -b dev
git push -u origin dev

git checkout -b fix
git push -u origin fix
```

Итоговая схема веток:

- **main** — продакшен, только через PR из dev
- **dev** — основная ветка разработки
- **fix** — ветка для конкретной задачи (фича/баг), создаётся от dev

### Шаг 4. Включите GitHub Pages

1. На GitHub откройте репозиторий → **Settings** → **Pages**.
2. В **Build and deployment** → **Source** выберите **GitHub Actions** (не «Deploy from a branch»).
3. Сохраните. Сайт будет публиковаться автоматически после успешного merge в `main`.

### Шаг 5. Проверка тестов локально (необязательно)

```powershell
pip install -r requirements.txt
python -m pytest tests/test_ui.py -v
```

Должно пройти 4 теста.

---

## Сценарий работы с ветками (п. 6–7 задания)

### 6.1 Переключитесь на fix

```powershell
git checkout fix
```

Убедитесь, что ветка `fix` создана от `dev`:

```powershell
git merge dev
```

### 6.2 Внесите изменения

Например, измените текст кнопки в `index.html`:

```html
<button type="submit" id="submit-btn">Отправить заявку</button>
```

И **обновите тест** в `tests/test_ui.py` (строка с `"Отправить"`), чтобы он ожидал новый текст:

```python
self.assertEqual(button.text, "Отправить заявку")
```

Если изменить только HTML, а тест не трогать — CI упадёт (это демонстрация п. 5).

### 6.3 Коммит и push

```powershell
git add .
git commit -m "Изменён текст кнопки отправки"
git push origin fix
```

### 6.4 Pull Request: fix → dev

1. На GitHub: **Pull requests** → **New pull request**.
2. **base:** `dev`, **compare:** `fix`.
3. Создайте PR. GitHub Actions запустит job **Run UI Tests**.
4. Если тесты красные — исправьте код в ветке `fix`, сделайте commit и push; PR обновится автоматически.
5. Когда тесты зелёные — нажмите **Merge pull request**.

### 6.5 Pull Request: dev → main

1. **New pull request**: **base:** `main`, **compare:** `dev`.
2. Дождитесь успешных тестов.
3. **Merge pull request**.
4. После merge в `main` запустится job **Deploy to GitHub Pages** (только если тесты прошли).
5. Сайт будет доступен по адресу:  
   `https://ВАШ_ЛОГИН.github.io/lab11-cicd/`

---

## Демонстрация падения тестов (п. 5)

Чтобы показать преподавателю, что CI ловит ошибки:

1. На ветке `fix` измените текст кнопки на «Отправить заявку», **не** меняя тест.
2. Сделайте commit и push.
3. В PR или во вкладке **Actions** увидите failed job **Run UI Tests**.
4. Исправьте тест или верните текст кнопки — тесты снова пройдут.

---

## Что делает ci.yml

| Job | Когда запускается | Что делает |
|-----|-------------------|------------|
| **test** | push/PR в main, dev, fix | Python, Chrome, `pytest tests/test_ui.py` |
| **deploy** | push в **main** после успешного test | Публикует `index.html` и `style.css` на GitHub Pages |

Деплой **не** выполняется, если тесты упали (`needs: test`).

---

## 4 автоматизированных теста

1. Заголовок страницы и `<h1>`.
2. Наличие полей формы (имя, email, сообщение, кнопка).
3. Текст кнопки «Отправить».
4. Успешная отправка формы и сообщение об успехе.

---

## Частые проблемы

| Проблема | Решение |
|----------|---------|
| `git push` просит логин | Используйте Personal Access Token вместо пароля или SSH-ключ |
| Pages не деплоится | Settings → Pages → Source = **GitHub Actions** |
| Тест падает на кнопке | Текст в `index.html` и в `test_submit_button_text` должны совпадать |
| Chrome не найден локально | Установите Google Chrome |

---

## Для отчёта

Сделайте скриншоты:

1. Успешный workflow в **Actions** (ветка fix / dev / main).
2. Упавший workflow при намеренной ошибке.
3. Merged PR fix → dev и dev → main.
4. Работающий сайт на GitHub Pages.
