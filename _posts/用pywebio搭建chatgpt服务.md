---
title: 用pywebio搭建chatgpt服务
date: 2023-05-17 10:39:11
tags:
	- AI
---

--

```
"""
免翻墙ChatGPT客户端

pip install openai pywebio requests
"""
import time

import openai

from pywebio.input import input, input_group, textarea, actions
from pywebio.output import put_error, put_text, put_markdown, put_info, use_scope, clear
from pywebio.session import set_env, download

# Get your API key from https://platform.openai.com/account/api-keys
OPENAI_API_KEY = "sk-xxxx"

# openai proxy, allow access from China
# to deploy your proxy, see https://github.com/x-dr/chatgptProxyAPI
API = "https://openai.wangweimin.site/v1"


# Or, use https://api2d.com/
# OPENAI_API_KEY = "fkxxx-xxx"
# API = "https://openai.api2d.net/v1"

class ExceedMaxTokenError(Exception):
    pass


class OmittedContentError(Exception):
    pass


class ChatGPTStreamMessage:
    def __init__(self, response):
        self.response = response
        self.yielded = []

    def __next__(self):
        # https://github.com/openai/openai-cookbook/blob/main/examples/How_to_stream_completions.ipynb
        chunk = next(self.response)

        # https://platform.openai.com/docs/guides/chat/response-format
        # The possible values for finish_reason are:
        #   stop: API returned complete model output
        #   length: Incomplete model output due to max_tokens parameter or token limit
        #   content_filter: Omitted content due to a flag from our content filters
        #   null: API response still in progress or incomplete
        finish_reason = chunk['choices'][0]['finish_reason']
        if finish_reason == 'length':
            raise ExceedMaxTokenError
        elif finish_reason == 'content_filter':
            raise OmittedContentError

        # delta: { "role": "assistant" } or { "content": "..."} or {}
        delta = chunk['choices'][0]['delta']

        content = delta.get('content', '')
        if content:
            self.yielded.append(content)
        return content

    def __iter__(self):
        return self

    def result(self):
        return ''.join(self.yielded)


def chatgpt(model="gpt-3.5-turbo",
            system_message="",
            api_key=OPENAI_API_KEY,
            api_base=API,
            **model_kwargs):
    """
    :param model: gpt-3.5-turbo, gpt-3.5-turbo-0301
    :param system_message: The system message helps set the behavior of the assistant.
    :param model_kwargs: model parameters, see https://platform.openai.com/docs/api-reference/chat/create

    Usage:
        bot = chatgpt()
        bot.send(None)  # initialize
        while True:
            reply = bot.send(input("User: "))
            for msg in reply:
                print(msg, end='', flush=True)
    """
    messages = []
    if system_message:
        messages.append({"role": "system", "content": system_message})
    user_msg = yield

    while True:
        messages.append({"role": "user", "content": user_msg})
        resp = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            stream=True,
            **model_kwargs,
            api_key=api_key,
            api_base=api_base,
            user=str(int(time.time())),
        )
        reply = ChatGPTStreamMessage(resp)
        user_msg = yield reply
        messages.append({"role": "assistant", "content": reply.result()})


def ask_bot(bot, user_msg) -> str:
    try:
        reply_chunks = bot.send(user_msg)
    except ExceedMaxTokenError:
        put_error('Exceed max token. Please open chat in a new session.')
    except OmittedContentError:
        put_error("Omitted content due to a flag from OpanAI's content filters.")
    except Exception as e:
        put_error(f'Error: {e}')
    else:
        with use_scope(f'reply-{int(time.time())}'):
            for chunk in reply_chunks:
                put_text(chunk, inline=True)
            clear()  # clear above text
            put_markdown(reply_chunks.result())
            return reply_chunks.result()


def main():
    """ChatGPT"""
    set_env(input_panel_fixed=False, output_animation=False)
    put_markdown("""
    # ChatGPT
    TIPS: 刷新页面来开启新会话
    """)

    bot = chatgpt()
    bot.send(None)  # initialize
    messages = []
    while True:
        form = input_group('', [
            input(name='msg', placeholder='Ask ChatGPT'),
            actions(name='cmd', buttons=['发送', '多行输入', '保存对话'])
        ])
        if form['cmd'] == '多行输入':
            form['msg'] = textarea(value=form['msg'])
        elif form['cmd'] == '保存对话':
            download(f"chatgpt_{time.strftime('%Y%m%d%H%M%S')}.md",
                     '\n\n'.join(messages).encode('utf8'))
            continue
        user_msg = form['msg']
        if not user_msg:
            continue
        put_info(put_text(user_msg, inline=True))
        reply = ask_bot(bot, user_msg)
        messages.append(f"> {user_msg}")
        messages.append(reply)


if __name__ == '__main__':
    from pywebio import start_server

    start_server(main, port=8085, auto_open_webbrowser=False, debug=True, cdn=False)

```



https://github.com/x-dr/chatgptProxyAPI



参考资料

1、

https://api2d.com/doc/doc