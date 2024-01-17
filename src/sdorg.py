import asyncio
import os
from pathlib import Path
import sys

from playwright.async_api import async_playwright

async def get_svg(args, page, input):
    await page.locator('img#exportButton').click()
    async with page.expect_download() as download_info:
        await page.locator('button#downloadButtonSvg').click()
    download = await download_info.value
    dest = format(Path(input).stem) + '.svg'
    if os.path.isfile(dest):
        if not args.allow_overwrite:
            args.logger.debug('DEBUG: 既存のファイル "{}" を上書きしません'.format(dest))
            return
        else:
            args.logger.debug('DEBUG: 既存のファイル "{}" が上書きされます'.format(dest))
            pass
        pass
    if args.dry_run:
        return
    await download.save_as(dest)


async def exec_one(args, page, input):
    if input is None:
        src = sys.stdin.read()
    else:
        with open(input, 'r') as f:
            src = f.read()
        pass
    source = page.locator('div.CodeMirror textarea')
    await source.focus()
    await page.keyboard.press('Control+A')
    await page.keyboard.press('Delete')
    await source.fill(src)
    await page.keyboard.press('Escape')
    await asyncio.sleep(0.5 * args.delay_multiplier)
    if args.type == 'svg':
        await get_svg(args, page, input)
    if args.pause:
        await page.pause()
    return


async def exec(args):
    async with async_playwright() as pw:
        if args.browser_type == 'chromium':
            browser_type = pw.chromium
        elif args.browser_type == 'firefox':
            browser_type = pw.firefox
        elif args.browser_type == 'webkit':
            browser_type = pw.webkit
        else:
            browser_type = pw.chromium
        browser = await browser_type.launch(headless=args.headless)
        context = await browser.new_context(accept_downloads=True)
        page = await context.new_page()
        await page.goto('https://sequencediagram.org/')
        await asyncio.sleep(0.5 * args.delay_multiplier)
        for file in args.filename:
            await exec_one(args, page, file)
            await asyncio.sleep(0.5 * args.delay_multiplier)
        await context.close()
        await browser.close()
    return
