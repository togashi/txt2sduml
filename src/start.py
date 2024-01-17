import asyncio
import argparse
import sys
import pkg_resources

from . import sdorg
from .lib import logger

def handler(args):
    asyncio.run(sdorg.exec(args))

def exec():
    playwright_parser = argparse.ArgumentParser(add_help=False)
    playwright_parser.add_argument('-H', '--headless', action='store_true', default=True, help='ヘッドレス実行 (-S, --show-browser と排他)')
    playwright_parser.add_argument('-S', '--show-browser', action='store_false', dest='headless', help='ブラウザ表示 (-H, --headless と排他)')
    playwright_parser.add_argument('--browser-type', metavar="TYPE", choices=['chromium', 'firefox', 'webkit'], help='ブラウザタイプ {chromium (default),firefox,webkit}')
    playwright_parser.add_argument('-d', '--delay-multiplier', metavar="MUL", type=float, default=1.0, help='実行ディレイ倍率 (default=1.0)')

    parser = argparse.ArgumentParser(description='render sequence diagrams', parents=[playwright_parser])
    parser.add_argument('-v', '--verbose', action='count', default=0, help='実行ログ出力の詳細度を上げる (-vv, -vvv まで)')
    parser.add_argument('-t', '--type', metavar='OUTPUT_TYPE', choices=['svg', 'pdf'], default='svg', help=argparse.SUPPRESS)
    parser.add_argument('-O', '--allow-overwrite', action='store_true', help='出力ファイルの上書きを許容する')
    parser.add_argument('-P', '--pause', action='store_true', default=False, help='ページの処理が終わる度に一時停止する')
    try:
        ver = pkg_resources.get_distribution('txt2sduml').version
    except:
        ver = 'unknown'
    parser.add_argument('-V', '--version', action='version', help="バージョン情報を表示する", version='{} {}'.format(parser.prog, ver))
    parser.add_argument('--dry-run', action='store_true', help="ファイル出力をスキップする")
    parser.add_argument('--logger', action='store', default=None, help=argparse.SUPPRESS)
    parser.add_argument('filename', nargs='+')
    parser.set_defaults(handler=handler)
    parser.set_defaults(prog=parser.prog)

    args = parser.parse_args()
    args.logger = logger.Logger(args.verbose)

    if hasattr(args, 'handler'):
        args.handler(args)
    else:
        parser.print_help()
    return
