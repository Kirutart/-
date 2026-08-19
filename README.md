# Последний урок — Telegram Mini App

Готовая статическая Telegram Mini App. Главный файл — `index.html`.

## 1. Хостинг через GitHub Pages

1. На GitHub создайте публичный репозиторий `posledniy-urok`.
2. Загрузите в корень репозитория файлы `index.html` и `.nojekyll`.
3. Откройте `Settings → Pages`.
4. В `Build and deployment` выберите `Deploy from a branch`.
5. Branch: `main`, Folder: `/(root)` → `Save`.
6. GitHub покажет адрес вида `https://YOUR_GITHUB_USERNAME.github.io/posledniy-urok/`.

## 2. Бот Telegram

1. Откройте @BotFather и отправьте `/newbot`.
2. Задайте имя и username, заканчивающийся на `bot`.
3. `/mybots` → ваш бот → `Bot Settings → Configure Mini App → Enable Mini App`.
4. Вставьте HTTPS-адрес GitHub Pages из шага 1.
5. Дополнительно: `Bot Settings → Menu Button` → текст `Играть` → тот же URL.

После настройки Main Mini App можно делиться ссылкой вида:
`https://t.me/YOUR_BOT_USERNAME?startapp`

## Важно

- Bot token в `index.html` вставлять НЕ нужно и нельзя публиковать.
- Игра работает без backend.
- Локальные рекорды внутри Telegram дополнительно синхронизируются в Telegram CloudStorage конкретного пользователя. Это не глобальный лидерборд.
