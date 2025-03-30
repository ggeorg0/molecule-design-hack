# Генерация офтальмологических препаратов с заданными свойствами с использованием обучения с подкреплением

Кейс c хакатона ПРОСТО x СБЕР

## Установка для REINVENT 4 (Linux only)

Клонируйте этот репозиторий и спуститесь в его директорию

```
git clone https://github.com/ggeorg0/molecule-design-hack.git
cd molecule-design-hack
```

Клонируйте репозиторий REINVENT 4 и dockstring. Dockstring это библиотека для молекулярного связывания и бенчмаркинга связывания.
```bash
git clone https://github.com/MolecularAI/REINVENT4.git
git clone https://github.com/dockstring/dockstring.git
```


Создайте окружение в conda с Python версии 3.10.

```bash
conda create -n "hack" python=3.10
```
```bash
conda activate hack
```

Установите зависимости REINVENT 4
```bash
pip install -r REINVENT4/requirements-linux-64.lock
```

последняя вресия REINVENT 4 требует установки утилиты iSIM, которая почему-то не включена в требования по-умолчанию. Утилиту необходимо поставить с помощью следующих команд:

```bash
conda config --add channels conda-forge
conda config --set channel_priority strict
conda install isim
```

Добавьте зависимости dockstring в окружение conda.
```bash
conda env update --file dockstring/environment.yml --prune
```


## Установка с venv

Для работы с данным проектом вам понадобится интерпретатор Python 3.10 или больше.

Клонируйте этот репозиторий

```
git clone https://github.com/ggeorg0/molecule-design-hack.git
```

### Виратульное окружение

Мы рекомендуем использвать виртуальные окружения для изоляции  зависимостей проекта.

Перейдите в директорию с клонированным репозиторием и выполните следующую команду, чтобы создать виртуальное окружение с помощью `venv`:

```bash
python -m venv venv
```


Далее нужно активировать виртальное окружение

- **Linux/macOS**:
    ```bash
    source venv/bin/activate
    ```
- **Windows (CMD/PowerShell)**:
    ```cmd
    .\venv\Scripts\activate
    ```

После активации в начале строки терминала появится `(venv)`.

### Установка зависимостей
Установите необходимые библиотеки из файла `requirements.txt`:
```bash
pip install -r requirements.txt
```
