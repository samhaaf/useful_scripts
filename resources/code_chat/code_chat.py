from kit.ai.llms import models
import subprocess
import sys

system_prompt = """
The date is May 25, 2024.
You are an AI assistant for coding assistance.
You make architecture decisions that would be made by a world-class engineer.
Your code is modular, and written with clear separation of concerns.
Each session will start with all of the files currently in the project.
Your first response should start with a discussion of the relevant files.
You can start each subsequent response with more discussions to get creative.
If there is a lot of complexity somewhere, break it down into smaller functions.
Do not ever use a comment as a placeholder for actual logic. Always to solve it.
Do not tell the human to repeat any behavior. You will repeat tedious behaviors.

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

def run_ccd(path):
    result = subprocess.run(f'copy-current-directory --print "{path}"', capture_output=True, text=True, shell=True)
    if result.stderr:
        print(f"Error with ccd command for path {path}: {result.stderr}", file=sys.stderr)
    return result.stdout

def new_session():
    print('|  New session..')
    session = models['gpt4-turbo']().get_session()
    session.constrain(system_prompt)
    return session

def get_ccd_prompt():
    if len(sys.argv) > 1:
        print('|  Including files..')
        return "\n\n".join([run_ccd(path) for path in sys.argv[1:]]) + "\n\n"
    return ''


if __name__ == '__main__':
    session = new_session()
    prompt = get_ccd_prompt()

    try:
        while True:
            prompt += input('|> ')

            if prompt.split('\n')[-1].strip() == '/reset':
                session = new_session()
                prompt = "/include"

            if prompt.split('\n')[-1].strip() == '/include':
                prompt = get_ccd_prompt()
                continue

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
