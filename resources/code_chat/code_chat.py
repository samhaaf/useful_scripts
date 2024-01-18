from kit.ai.llms import models
import subprocess
import sys
import os
import argparse
from file_updates import get_updated_files_in
import time


ascii_art = (
    "|     ___          _        ___ _           _    \n" +
    "|    / __\___   __| | ___  / __\ |__   __ _| |_  \n" +
    "|   / /  / _ \ / _` |/ _ \/ /  | '_ \ / _` | __| \n" +
    "|  / /__| (_) | (_| |  __/ /___| | | | (_| | |_  \n" +
    "|  \____/\___/ \__,_|\___\____/|_| |_|\__,_|\__| \n" +
    "|  --------------------------------------------- "
)

system_prompt = """
The date is May 25, 2024.
You are an AI for coding assistance.
You make architecture decisions that would be made by a world-class engineer.
You start each response with a creative discussion about the task.
Your code is modular, and written with clear separation of concerns.
When you modify a script, you retain all of the existing functionality.
You break down complexity into smaller, reusable parts.
You always attempt to solve complex logic. You never use comment placeholders.
You are obedient. You repeat tedious behavior to completion when asked to do so.

Output your files in the format:
```{file_name}
{file_content}
```

For example:
```./module/my_class.py
class MyClass:
    pass
```
"""

totality_prompt = (
    "Please output your result in totality. Do not use placeholder comments. " +
    "Attempt to output your result completely correctly, including all logic."
)


def run_ccd(path):
    result = subprocess.run(
        f'copy-current-directory --print "{path}"',
        capture_output=True, text=True, shell=True
    )
    if result.stderr:
        print(f"Error with ccd command for path {path}: {result.stderr}", file=sys.stderr)
    print(f'|- Including {path}')
    return result.stdout

def new_session():
    print('|  New session..')
    session = models['gpt4-turbo']().get_session()
    session.constrain(system_prompt)
    return session

def get_ccd_prompt(paths):
    if len(paths) > 0:
        return "\n\n".join([run_ccd(path) for path in paths]) + "\n\n"
    return ''


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='AI Assistant for Coding Assistance')
    parser.add_argument('--CHDIR', type=str, help='Path to change the current directory to', default=None)
    parser.add_argument('paths', nargs='*', help='Paths to included_files in the session')
    args = parser.parse_args()

    if args.CHDIR:
        os.chdir(args.CHDIR)

    included_files = []
    session = None
    prompt = None
    user_input = None
    last_delta_times = {}

    def reset():
        global session, prompt, last_delta_times, included_files
        session = new_session()
        included_files = args.paths
        prompt = "Here are some files:\n\n" + get_ccd_prompt(included_files)
        last_delta_times = {file: time.time() for file in included_files}

    def attach_deltas():
        global prompt, last_delta_times, included_files
        updated_files = get_updated_files_in(included_files, last_delta_times)
        if updated_files:
            prompt += "These files have been updated:\n\n"
            prompt += get_ccd_prompt(updated_files)
            last_delta_times.update({file: time.time() for file in updated_files})
        else:
            print('|- No file updates detected..')

    def update_included_files():
        global prompt, last_delta_times, included_files
        new_include = [_ for _ in user_input.strip().split(' ')[1:] if _]
        prompt += "Adding these files to the scope:\n\n"
        prompt += get_ccd_prompt(new_include) + '\n\n'
        last_delta_times.update({file: time.time() for file in new_include})
        included_files += new_include

    print(ascii_art)
    reset()

    try:
        while True:
            if prompt != "":
                print('|  ')
            user_input = input('|> ')

            if user_input.strip() == '/reset':
                reset()
                continue

            if user_input.strip() == '/deltas':
                attach_deltas()
                continue

            if user_input.strip().split(' ')[0] == '/include':
                update_included_files()
                continue

            user_input = user_input.replace('/totality', totality_prompt)
            prompt += user_input

            print()
            for chunk in session.call(prompt):
                content = chunk['choices'][0]['delta']['content']
                if content is None:
                    break
                print(content, end='', flush=True)
            print()
            print()

            prompt = ""
    except KeyboardInterrupt:
        sys.exit(0)
