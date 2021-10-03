import os
import math
import requests
import shutil
import sys
import heroku3
import traceback
import psutil
from functools import wraps
from os import environ, execle
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError
from pyrogram import Client, filters
from pyrogram.types import Message
from config import (
    HEROKU_API_KEY,
    HEROKU_APP_NAME,
    HEROKU_URL,
    U_BRANCH,
    UPSTREAM_REPO,
    BOT_NAME,
)
from handlers.song import get_text, humanbytes
from helpers.filters import command
from helpers.decorators import sudo_users_only


# ====== UPDATER ======

REPO_ = UPSTREAM_REPO
BRANCH_ = U_BRANCH


@Client.on_message(command("update"))
@sudo_users_only
async def updatebot(_, message: Message):
    msg = await message.reply_text("**updating bot, please wait for a while...**")
    try:
        repo = Repo()
    except GitCommandError:
        return await msg.edit("**invalid git command !**")
    except InvalidGitRepositoryError:
        repo = Repo.init()
        if "upstream" in repo.remotes:
            origin = repo.remote("upstream")
        else:
            origin = repo.create_remote("upstream", REPO_)
        origin.fetch()
        repo.create_head(U_BRANCH, origin.refs.main)
        repo.heads.main.set_tracking_branch(origin.refs.main)
        repo.heads.main.checkout(True)
    if repo.active_branch.name != U_BRANCH:
        return await msg.edit(
            f"**sorry, you are using costum branch named:** `{repo.active_branch.name}`!\n\nchange to `{U_BRANCH}` branch to continue update!"
        )
    try:
        repo.create_remote("upstream", REPO_)
    except BaseException:
        pass
    ups_rem = repo.remote("upstream")
    ups_rem.fetch(U_BRANCH)
    if not HEROKU_URL:
        try:
            ups_rem.pull(U_BRANCH)
        except GitCommandError:
            repo.git.reset("--hard", "FETCH_HEAD")
        await run_cmd("pip3 install --no-cache-dir -r requirements.txt")
        await msg.edit("**update finished, restarting now...**")
        args = [sys.executable, "main.py"]
        execle(sys.executable, *args, environ)
        sys.exit()
        return
    else:
        await msg.edit("`heroku detected!`")
        await msg.edit("`updating and restarting is started, please wait for 5-10 minutes!`")
        ups_rem.fetch(U_BRANCH)
        repo.git.reset("--hard", "FETCH_HEAD")
        if "heroku" in repo.remotes:
            remote = repo.remote("heroku")
            remote.set_url(HEROKU_URL)
        else:
            remote = repo.create_remote("heroku", HEROKU_URL)
        try:
            remote.push(refspec="HEAD:refs/heads/main", force=True)
        except BaseException as error:
            await msg.edit(f"🚫 **updater error** \n\nTraceBack : `{error}`")
            return repo.__del__()


# HEROKU LOGS


async def edit_or_send_as_file(
    text: str,
    message: Message,
    client: Client,
    caption: str = "`Result!`",
    file_name: str = "result",
    parse_mode="md",
):
    """Send As File If Len Of Text Exceeds Tg Limit Else Edit Message"""
    if not text:
        await message.edit("`there is something other than text, aborting...`")
        return
    if len(text) <= 1024:
        return await message.edit(text, parse_mode=parse_mode)

    await message.edit("`output is too large, sending as file!`")
    file_names = f"{file_name}.text"
    open(file_names, "w").write(text)
    await client.send_document(message.chat.id, file_names, caption=caption)
    await message.delete()
    if os.path.exists(file_names):
        os.remove(file_names)
    return


heroku_client = heroku3.from_key(HEROKU_API_KEY) if HEROKU_API_KEY else None


def _check_heroku(func):
    @wraps(func)
    async def heroku_cli(client, message):
        heroku_app = None
        if not heroku_client:
            await message.reply_text("`Please Add Heroku API Key To Use This Feature!`")
        elif not HEROKU_APP_NAME:
            await edit_or_reply(message, "`Please Add Heroku APP Name To Use This Feature!`")
        if HEROKU_APP_NAME and heroku_client:
            try:
                heroku_app = heroku_client.app(HEROKU_APP_NAME)
            except:
                await message.reply_text(message, "`Heroku Api Key And App Name Doesn't Match! Check it again`")
            if heroku_app:
                await func(client, message, heroku_app)

    return heroku_cli


@Client.on_message(command("logs"))
@sudo_users_only
@_check_heroku
async def logswen(client: Client, message: Message, happ):
    msg = await message.reply_text("`please wait for a moment!`")
    logs = happ.get_log()
    capt = f"Heroku logs of `{HEROKU_APP_NAME}`"
    await edit_or_send_as_file(logs, msg, client, capt, "logs")


# Restart Bot
@Client.on_message(command("restart"))
@sudo_users_only
@_check_heroku
async def restart(client: Client, message: Message, hap):
    await message.reply_text("`restarting now, please wait...`")
    hap.restart()


# Set Heroku Var
@Client.on_message(command("setvar"))
@sudo_users_only
@_check_heroku
async def setvar(client: Client, message: Message, app_):
    msg = await message.reply_text("`please wait...`")
    heroku_var = app_.config()
    _var = get_text(message)
    if not _var:
        await msg.edit("**usage:** `/setvar (var) (value)`")
        return
    if " " not in _var:
        await msg.edit("**usage:** `/setvar (var) (value)`")
        return
    var_ = _var.split(" ", 1)
    if len(var_) > 2:
        await msg.edit("**usage:** `/setvar (var) (value)`")
        return
    _varname, _varvalue = var_
    await msg.edit(f"**variable:** `{_varname}` \n**new value:** `{_varvalue}`")
    heroku_var[_varname] = _varvalue


# Delete Heroku Var
@Client.on_message(command("delvar"))
@sudo_users_only
@_check_heroku
async def delvar(client: Client, message: Message, app_):
    msg = await message.reply_text("`please wait...!`")
    heroku_var = app_.config()
    _var = get_text(message)
    if not _var:
        await msg.edit("`give a var name to delete!`")
        return
    if _var not in heroku_var:
        await msg.edit("`this var doesn't exists!`")
        return
    await msg.edit(f"sucessfully deleted var `{_var}`")
    del heroku_var[_var]


# Modul From https://github.com/DevsExpo/Xtra-Plugins/blob/main/usage.py
# Port By https://github.com/FeriEXP | https://t.me/xflicks
# Usage Heroku Dyno


heroku_client = None
if HEROKU_API_KEY:
    heroku_client = heroku3.from_key(HEROKU_API_KEY)
    
def _check_heroku(func):
    @wraps(func)
    async def heroku_cli(client, message):
        if not heroku_client:
            await edit_or_reply(message, "`Please Add Heroku API Key For This To Function To Work!`")
        else:
            await func(client, message, heroku_client)
    return heroku_cli


def fetch_heroku_git_url(api_key, app_name):
    if not api_key:
        return None
    if not app_name:
        return None
    heroku = heroku3.from_key(api_key)
    try:
        heroku_applications = heroku.apps()
    except:
        return None
    heroku_app = None
    for app in heroku_applications:
        if app.name == app_name:
            heroku_app = app
            break
    if not heroku_app:
        return None
    return heroku_app.git_url.replace("https://", "https://api:" + api_key + "@")


@Client.on_message(command("usage"))
@sudo_users_only
@_check_heroku
async def gib_usage(client, message, hc):
  msg_ = await message.reply_text("`[HEROKU] - Please Wait.`")
  useragent = (
        "Mozilla/5.0 (Linux; Android 10; SM-G975F) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/80.0.3987.149 Mobile Safari/537.36"
    )
  acc_id = hc.account().id  
  headers = {
        "User-Agent": useragent,
        "Authorization": f"Bearer {HEROKU_API_KEY}",
        "Accept": "application/vnd.heroku+json; version=3.account-quotas",
    }
  heroku_api = "https://api.heroku.com"
  path = "/accounts/" + acc_id + "/actions/get-quota"
  r = requests.get(heroku_api + path, headers=headers)
  if r.status_code != 200:
        return await msg_.edit(f"`[{r.status_code}] - Something Isn't Right. Please Try Again Later.`")
  result = r.json()
  quota = result["account_quota"]
  quota_used = result["quota_used"]
  remaining_quota = quota - quota_used
  percentage = math.floor(remaining_quota / quota * 100)
  minutes_remaining = remaining_quota / 60
  hours = math.floor(minutes_remaining / 60)
  minutes = math.floor(minutes_remaining % 60)
  App = result["apps"]
  try:
      App[0]["quota_used"]
  except IndexError:
      AppQuotaUsed = 0
      AppPercentage = 0
  else:
      AppQuotaUsed = App[0]["quota_used"] / 60
      AppPercentage = math.floor(App[0]["quota_used"] * 100 / quota)
  AppHours = math.floor(AppQuotaUsed / 60)
  AppMinutes = math.floor(AppQuotaUsed % 60)
  app_name = HEROKU_APP_NAME or "Not Specified."
  return await msg_.edit(
        f"📅 <b>Dyno Usage {app_name}</b>\n\n"
        f"<b>✗ Usage in Hours And Minutes :</b>\n"
        f" • <code>{AppHours}h {AppMinutes}m</code>"
        f" | <code>[{AppPercentage} %]</code> \n\n"
        "<b>✗ Dyno Remaining This Months: </b>\n"
        f" • <code>{hours}h {minutes}m</code>"
        f" | <code>[{percentage}%]</code>",
    )
