# Molecule Design Hack
Инструмент, генерирующий офтальмологические препараты с использованием обучения с подкреплением (Reinforcement Learning).

1. Реализованы модели для предсказания проницаемости через роговицу, связывания с меланином и раздражения
2. RL-модель генерации молекул учитывает свойства капель и связывание с белком COX-2
3. Лучшие молекулы отбираются по критериям SAscore, QED


_Проект разработан в рамках хакатона ПРОСТО x СБЕР._ 

## Требования
- Python 3.10+
- ОС: Linux, macOS, Windows
- Conda


## Установка

Клонируйте этот репозиторий и спуститесь в его директорию
```bash
git clone https://github.com/ggeorg0/molecule-design-hack.git
cd molecule-design-hack
```

Клонируйте репозиторий [REINVENT 4](https://github.com/MolecularAI/REINVENT4.git)
```bash
git clone https://github.com/MolecularAI/REINVENT4.git
git clone https://github.com/dockstring/dockstring.git
```


Создайте окружение в [Conda](https://docs.conda.io/projects/conda/en/latest/index.html)
```bash
conda create -n "hack" python=3.10
```
```bash
conda activate hack
```

Установите зависимости
```bash
pip install -r requirements.txt
```
```bash
pip install -r REINVENT4/requirements-linux-64.lock
```
_Опционально: используйте _requirements-macOS.lock_ для ОС MacOSX._

Последняя версия REINVENT 4 требует установки утилиты iSIM, которая не включена по-умолчанию в требованиях для установки REINVENT 4. Утилиту необходимо поставить с помощью следующих команд:

```bash
conda config --add channels conda-forge
conda config --set channel_priority strict
conda install isim
```

## Использование
Чтобы запустить процесс обучения с подкреплением для генерации молекул, необходимо активировать окружение conda, а также экспортировать путь для интерпретатора Python, чтобы REINVENT 4 мог корректно найти метрики, реализованные в этом репозитории

```bash
conda activate hack
export PYTHONPATH=$(env)
reinvent reinvent_config/rl_stage_1.toml
```

## Данные
Данные белка COX-2 и данные для вычисления проницаемости через роговицу, связывания с меланином и раздражения, были предоставлены сотрудниками Центра ИИ в химии.

Пример данных проницаемости через роговицу

| SMILES  | logPerm |
| ------------- | ------------- |
| CC1CC2C3CCC(C3(CC(C2(C4(C1=CC(=O)C=C4)C)F)O)C)(C(=O)C)O  | 5.135798437050  |
| CC(C1=CC(=C(C=C1)C2=CC=CC=C2)F)C(=O)O  | 5.347107530717  |