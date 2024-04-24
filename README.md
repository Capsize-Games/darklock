# Darklock

Completely disable the internet and other services, only allowing whitelists
through.

---

![img.png](img.png)

---

## Installation

```bash
pip install lockdown
```

---

## Usage

Import into your application at the top of the main entry file (e.g. `main.py`).

Install the lockdown for the service you want to restrict.

```python
import lockdown

lockdown.network.install()
lockdown.os.install()
```

Uninstall the lockdown for the service you no longer want to restrict.

```python
import lockdown

lockdown.network.uninstall()
lockdown.os.uninstall()
```

---

## Testing

```bash
python -m unittest discover -s tests
```
