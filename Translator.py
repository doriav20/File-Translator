from tkinter import Tk, filedialog, messagebox
from googletrans import Translator


def get_path():
    root = Tk()
    root.withdraw()
    path = filedialog.askopenfilename()
    if len(path) == 0:
        show_errors('no_path')
    return path


def get_file_content(path):
    try:
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()
    except:
        show_errors('not_readable')
    file.close()
    if len(content) == 0:
        show_errors('empty')
    return content


def get_translation(text):
    lang = {'src': 'he', 'dest': 'en'}
    for ch in text:
        if 'a' <= ch.lower() <= 'z':
            lang['src'] = 'en'
            lang['dest'] = 'he'
        break
    t = Translator()
    new = t.translate(text, src=lang['src'], dest=lang['dest'])
    if text == new.text:
        show_errors('same_chars')
    return new.text.capitalize()


def save_path(old_path):
    name = old_path.split('/')[-1]
    extension = ''
    if '.' in name:
        extension = name.split('.')[-1]
    file_types = [('Text Documents', '*.txt'), ('All Files', '*')]
    if extension:
        file_types.insert(0, ('{0} File'.format(extension.capitalize()), '*.{0}'.format(extension)))
    path = filedialog.asksaveasfilename(filetypes=file_types, defaultextension='.' + extension)
    if len(path) == 0:
        show_errors('save_failed')
    return path


def write_file(path, text):
    translated = get_translation(text)
    path = save_path(path)
    file = open(path, 'w', encoding='utf-8')
    file.write(translated)
    file.close()


def show_errors(option):
    title = ''
    msg = ''

    if option == 'no_path':
        title = 'No Path'
        msg = 'You have not Entered a Path'

    elif option == 'empty':
        title = 'File Content'
        msg = 'Your File is Empty'

    elif option == 'same_chars':
        title = 'Nothing Happened'
        msg = 'Your File does not Include Hebrew or English Letters\nWe will not Create a Translated File'

    elif option == 'save_failed':
        title = 'No Save'
        msg = 'You did not Save The Translated File'

    elif option == 'not_readable':
        title = 'Problem in File'
        msg = 'Your File is not Readable'

    else:
        return

    messagebox.showinfo(title, msg)
    exit(1)


def main():
    path = get_path()
    content = get_file_content(path)
    write_file(path, content)


if __name__ == '__main__':
    main()
