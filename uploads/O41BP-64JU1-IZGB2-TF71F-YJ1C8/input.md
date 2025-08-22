# Translation

- [Translation](#translation)
  - [Get Started](#get-started)
    - [Extract the text](#extract-the-text)
    - [Create the database for your language](#create-the-database-for-your-language)
    - [Start Translating](#start-translating)
    - [Include it in the app](#include-it-in-the-app)


If you want to add a translation for the website, you can do this easily by following this step by step guide

## Get Started

First, we highly recommend you to **fork** the project, download [poedit](https://poedit.net/) (for easy translation). Once you got all of this we can god further.

From the root directory in your shell go to `translations`

```
cd translations
```

### Extract the text

We have marked all the text that needs to be translate so you just need to extract it. To do so type:

```
pybabel extract -F babel.cfg -k _ -o to_translate.pot ..
```

You should have a file called `to_translate.pot`.

### Create the database for your language

If it's your **first time**, you need to create a new folder with this command:

```
pybabel init -i to_translate.pot -d . -l <YOUR LANGUAGE>
```

Replace `<YOUR LANGUAGE>` with **the standard 2 letters denomination of your language** (*eg*: `en` for english, `fr` for french, ... )

If you just want to **update** it run:

```
pybabel update -i to_translate.pot -d . -l <YOUR LANGUAGE>
```

### Start Translating

Now you should have created a new folder in translations looking like `<YOUR LANGUAGE>/LC_MESSAGES`. Open the `messages.po` with *poedit* and start doing the translation.

### Include it in the app

You need to first compile this `.po` file into `.mo` with this command:

```
pybabel compile -d .
```

Then to use the language in the app, you should look for the constant `LANGUAGES` in [`app.py`](../app.py) and add to the list the 2 letters of your language. You also need to add those two letters in the [`base.html`](../templates/base.html) (search in the file there should be already a list).

Run the app and your language and translation should appear automatically.