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


async def save_pdf(args, page, input):
    dest = format(Path(input).stem) + '.pdf'
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
    canvas = page.locator('canvas#interactionCanvas').first
    w = await canvas.get_attribute('width')
    h = await canvas.get_attribute('height')
    await page.pdf(path=dest, width=w, height=h)
    await asyncio.sleep(0.5 * args.delay_multiplier)
    await canvas.focus()


async def get_pdf(args, page, input):
    await page.keyboard.press('Control+M')
    await asyncio.sleep(0.5 * args.delay_multiplier)
    await save_pdf(args, page, input)
    await page.keyboard.press('Control+M')


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
    if not args.edit:
        if args.type == 'svg':
            await get_svg(args, page, input)
        elif args.type == 'pdf':
            await get_pdf(args, page, input)
        pass
    if args.pause or args.edit:
        await page.pause()
    return


async def get_browser_context(args, pw):
    if args.chrome_remote_debugging:
        browser = await pw.chromium.connect_over_cdp(args.chrome_remote_debugging)
        context = browser.contexts[0]
    else:
        if args.browser_type == 'chromium':
            browser_type = pw.chromium
        elif args.browser_type == 'firefox':
            browser_type = pw.firefox
        elif args.browser_type == 'webkit':
            browser_type = pw.webkit
        else:
            browser_type = pw.chromium if not args.edit else pw.webkit
        browser = await browser_type.launch(headless=args.headless and not args.edit)
        context = await browser.new_context(accept_downloads=True)
    return (browser, context)


async def exec(args):
    async with async_playwright() as pw:
        (browser, context) = await get_browser_context(args, pw)
        # print('next: context.new_page()')
        page = await context.new_page()
        await page.goto('https://sequencediagram.org/')
        await asyncio.sleep(0.5 * args.delay_multiplier)
        for file in args.filename:
            await exec_one(args, page, file)
            if args.edit:
                continue
            await asyncio.sleep(0.5 * args.delay_multiplier)
        if args.edit:
            return
        await context.close()
        await browser.close()
    return
