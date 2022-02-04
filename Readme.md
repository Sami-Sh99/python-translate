
----

# Python Corpus Translator

**Description**:  2 Methods were implemented to translate any corpus of any size from one language to another. 

The first method uses a `Chrome WebDriver` to mock the activity of translating text by the original [google translate](https://translate.google.com.lb/?hl=en) site.

The second method uses a `Translator API ` and send batch data samples to be translated.

## Dependencies

All dependencies with the exact downloading version are listed in the [requirements.txt](requirements.txt) file

## Installation

To install all of the dependencies, run the following script from the root of your project's directory:

```
pip install -r requirements.txt -v
```

## Configuration

Some variables that should be configured:
```python
translate_from=r'Path/to/source/Corpus/'
translate_to=r'Path/to/new/translated/Corpus'
lang_code = 'Target Language'
max_character_limit=5000 #Max Char limit (google translate's max limit per translation is 5000)
```

## Usage

After configuration, run one of the following scripts:
```
python translation_api.py
```
```
python translation_task.py
```
## Known issues

The configuration should be fed as an argument instead of static variables... maybe a contributer can fix it if I was lazy to do so :)

----

## Open source licensing info
To be added, _spoiler (it's open source :D)_


----

## Credits and references

1. Project was inspired during building my thesis experiment as I needed to tranlsate an English Corpus consisting of 200K articles into the Arabic language