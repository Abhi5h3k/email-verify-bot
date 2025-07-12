import typer
from verify_email import VerifyEmail

app = typer.Typer(
    help="""
🔍 Verify email availability on popular domains.

📌 Supported Domains:
   1 -> AOL (aol.com)
   2 -> Yahoo (yahoo.com)
   3 -> Comcast/Xfinity (comcast.net)

💡 Example:
   uv run run.py run --domain 1 --input email_list.txt --sleep 5 --no-headless --skip-other-domain
"""
)


@app.command()
def run(
    domain: str = typer.Option(
        ..., 
        help="🌐 Domain to check. Use 1 for AOL, 2 for Yahoo, 3 for Comcast."
    ),
    input: str = typer.Option(
        ..., 
        help="📄 Input filename (with .txt extension) containing list of emails, one per line."
    ),
    sleep: int = typer.Option(
        5, 
        help="⏱️ Delay in seconds between checks. Default is 5."
    ),
    headless: bool = typer.Option(
        True, "--headless/--no-headless", 
        help="🧠 Run browser in headless mode. Use --no-headless to show browser window."
    ),
    skip_other_domain: bool = typer.Option(
        False, "--skip-other-domain/--no-skip-other-domain",
        help="🚫 Skip emails that don't match the selected domain (recommended for mixed lists)."
    ),
):
    VerifyEmail(
        domain_key=domain,
        input_file_name=input,
        headless=headless,
        sleep=sleep,
        skip_other_domain=skip_other_domain,
    )

if __name__ == "__main__":
    app()
