# 🔥 email-verify-bot 🔥  

[![Abhishek LinkedIn](https://img.shields.io/badge/Abhishek-LinkedIn-blue.svg?style=for-the-badge)](https://www.linkedin.com/in/abhi5h3k/)
[![Abhishek StackOverflow](https://img.shields.io/badge/Abhishek-StackOverflow-orange.svg?style=for-the-badge)](https://stackoverflow.com/users/6870223/abhi?tab=profile)

Check email validity across multiple domains like AOL, Yahoo, and Comcast using Selenium-based automation.

---

## 🚀 Use Case

Use this tool to identify **valid registered user emails** from a list across common providers.

---

## ⚙️ Setup

### ✅ Requirements

- Python 3.10.6+
- Chrome installed
- Compatible [ChromeDriver](https://chromedriver.chromium.org/downloads)

---

### 🧪 Installation (using `uv`)

We use [`uv`](https://github.com/astral-sh/uv) for faster dependency and script management.

1. **Install uv:**

   	``` 
  	curl -LsSf https://astral.sh/uv/install.sh | sh
   	```
2.  Clone repo and install dependencies:

	```
	uv pip install -r requirements.txt
	```
3. Download compatible chromedriver
   - Match your Chrome version.
   - Rename to ```chromedriver.exe``` and place inside the ```driver/```folder.	

---

### ▶️ Run the Bot

```
uv run run.py --domain 1 --input email_list.txt --sleep 5 --no-headless --skip-other-domain
```

### CLI Options:

| Flag                  | Description                                    | Example                  |
| --------------------- | ---------------------------------------------- | ------------------------ |
| `--domain`            | Email domain (`1`=AOL, `2`=Yahoo, `3`=Comcast) | `--domain 1`             |
| `--input`             | Path to input file containing emails           | `--input email_list.txt` |
| `--sleep`             | Delay in seconds between actions               | `--sleep 5`              |
| `--no-headless`       | Launch browser in visible mode (not headless)  |                          |
| `--skip-other-domain` | Skip emails not matching selected domain       |                          |

### 🆘 Help

To see CLI usage and all available options:

```
uv run run.py --help
```

### 📦 Build Standalone Executable (Optional)

If you prefer a single .exe for distribution:

```
pyinstaller --onefile run.py
```

# 🔥V2 color console + progress bar
![color console](https://media.giphy.com/media/jCmB7bVM3orrBuzlFi/giphy.gif)

# Yahoo 
![yahoo email bot](https://media.giphy.com/media/D1XnCQHa1DCbmDK4nf/giphy.gif)

# AOL
![AOL email bot](https://media.giphy.com/media/aMbpIJgA41ctZtVMbp/giphy.gif)

# Comcast
![comcast email bot](https://media.giphy.com/media/aTLZBB98V3goEDQV4h/giphy.gif)


## Authors

* **Abhishek Bhardwaj** - *Stackoverflow profile* - [Stackoverflow profile](https://stackoverflow.com/users/6870223/abhi?tab=profile)
			  *Linkedin profile* - [Linkedin profile](https://www.linkedin.com/in/abhishek-bhardwaj-b16764166)
