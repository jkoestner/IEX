"""Email module.

This module contains functions to send emails as well as generate reports
to send in the emails.

"""

import datetime
import logging
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from folioflex.portfolio import heatmap, helper, wrappers
from folioflex.portfolio.portfolio import Manager, Portfolio
from folioflex.utils import config_helper

# logging options https://docs.python.org/3/library/logging.html
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
if logger.hasHandlers():
    logger.handlers.clear()

formatter = logging.Formatter(fmt="%(levelname)s: %(message)s")

# provides the logging to the console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)


def send_email(message, subject, email_list, image_list=None):
    """Send summary of portfolios to email.

    Parameters
    ----------
    message : object
        Message to send in email
    subject : str
        Subject of email
    email_list : list
        Email addresses to send email to
    image_list : list
        Images to attach to email

    Returns
    -------
    bool
        True if email was sent successfully, False otherwise.

    """
    # Check if SMTP values are set
    for key, value in config_helper.__dict__.items():
        if key.startswith("SMTP_") and not value:
            logger.warning(f"{key} is not set, email not sent")
            return False

    # Create the email
    email = MIMEMultipart()
    email["Subject"] = subject
    email["From"] = config_helper.SMTP_USERNAME
    email["To"] = ";".join(email_list)

    message = MIMEText(message, "html")
    email.attach(message)

    if image_list:
        for idx, image in enumerate(image_list, start=1):
            email_image = MIMEImage(image)
            email_image.add_header("Content-ID", f"image{idx}")
            email_image.add_header(
                "Content-Disposition", "attachment", filename=f"image{idx}.png"
            )
            email.attach(email_image)

    # Send the email
    try:
        with smtplib.SMTP(config_helper.SMTP_SERVER, config_helper.SMTP_PORT) as smtp:
            smtp.starttls()
            smtp.login(config_helper.SMTP_USERNAME, config_helper.SMTP_PASSWORD)
            smtp.send_message(email)
        logger.info("Email sent successfully")
        return True
    except smtplib.SMTPException as e:
        logger.warning(f"Error sending email: {e}")
        return False


def generate_report(
    email_list,
    heatmap_market=None,
    heatmap_portfolio=None,
    manager_performance=None,
    portfolio_performance=None,
):
    """Generate report of portfolio performance and send to email.

    Parameters
    ----------
    email_list : list
        Email addresses to send email to
    heatmap_market : dict
        Market Heatmap dictionary to get values for
            see: folioflex.portfolio.heatmap.get_heatmap for more details
            Keys are:
            - lookback (optional)
    heatmap_portfolio : dict
        Portfolio Heatmap dictionary to get values for
            see: folioflex.portfolio.heatmap.get_heatmap for more details
            Keys are:
            - config_path (required)
            - portfolio (required)
            - lookback (optional)
    manager_performance : dict
        Manager dictionary to get values for
            see: folioflex.portfolio.portfolio.Manager.get_summary for more details
            Keys are:
            - config_path
            - portfolios (optional)
            - date (optional)
            - lookbacks (optional)
    portfolio_performance : dict
        Portfolio dictionary to get values for
            see: folioflex.portfolio.portfolio.Portfolio.get_performance for more details
            Keys are:
            - config_path
            - portfolio
            - date (optional)
            - lookback (optional)

    Returns
    -------
    bool
        True if email was sent successfully, False otherwise.
    """
    # building the email message

    today = datetime.date.today()
    spy_pct = wrappers.Yahoo().get_change_percent(ticker="SPY", days=1)
    subject = f"Summary as of {today}"
    message = (
        f"Below is your financial summary as of {today}."
        "<br>"
        f"The SPY return is {spy_pct:.2%}"
        "<br>"
        "<br>"
    )
    image_list = []
    image_idx = 1

    if heatmap_market is not None:
        lookback = heatmap_market.get("lookback", None)

        heatmap_summary = heatmap.get_heatmap(lookback=lookback)
        # using plotly kaleido to convert to image into bytes then attach it to the email.
        image = heatmap_summary.to_image(format="png")
        image_list.append(image)

        message += (
            "<p>Market Heatmap Summary</p>"
            "<ul>"
            f"<li>lookback: {lookback}</li>"
            "</ul>"
            f"<img src='cid:image{image_idx}' alt='heatmap market'/>"
            "<br>"
        )

        image_idx += 1

    if heatmap_portfolio is not None:
        config_path = heatmap_portfolio.get("config_path", None)
        portfolio = heatmap_portfolio.get("portfolio", None)
        lookback = heatmap_portfolio.get("lookback", None)

        heatmap_summary = heatmap.get_heatmap(
            config_path=config_path, portfolio=portfolio, lookback=lookback
        )
        # using plotly kaleido to convert to image into bytes then attach it to the email.
        image = heatmap_summary.to_image(format="png")
        image_list.append(image)

        message += (
            "<p>Portfolio Heatmap Summary</p>"
            "<ul>"
            f"<li>portfolio: {portfolio}</li>"
            f"<li>lookback: {lookback}</li>"
            "</ul>"
            f"<img src='cid:image{image_idx}' alt='heatmap portfolio'/>"
            "<br>"
        )

        image_idx += 1

    if manager_performance is not None:
        config_path = manager_performance.get("config_path")
        portfolios = manager_performance.get("portfolios", None)
        date = manager_performance.get("date", None)
        lookbacks = manager_performance.get("lookbacks", None)

        manager_summary = Manager(
            config_path=config_path, portfolios=portfolios
        ).get_summary(date=date, lookbacks=lookbacks)

        columns_to_keep = manager_summary.filter(like="_dwrr_pct").columns.tolist()
        columns_to_keep = [col for col in columns_to_keep if "div" not in col]
        columns_to_keep = [
            "date",
            "market_value",
            "equity",
            "cash",
            "return",
            *columns_to_keep,
        ]

        manager_condensed_summary = manager_summary[columns_to_keep]

        message += (
            f"<p>Manager Summary</p>"
            f"<ul>"
            f"<li>lookbacks: {lookbacks}</li>"
            f"</ul><br>{manager_condensed_summary.to_html()}<br>"
        )

    if portfolio_performance is not None:
        config_path = portfolio_performance.get("config_path")
        portfolio = portfolio_performance.get("portfolio")
        date = portfolio_performance.get("date", None)
        lookback = portfolio_performance.get("lookback", None)

        portfolio_summary = Portfolio(
            config_path=config_path, portfolio=portfolio
        ).get_performance(date=date, lookback=lookback, prettify=False)

        # remove rows with 0 market value
        portfolio_summary = portfolio_summary[
            portfolio_summary["market_value"] != 0
        ].sort_values("return", ascending=False)
        portfolio_pct = portfolio_summary.loc["portfolio"]["dwrr_pct"]

        # gainers/losers
        nbr_of_tickers = 5
        conditions = ~portfolio_summary.index.str.contains("Cash|benchmark|portfolio")
        gainers = (
            portfolio_summary[conditions & (portfolio_summary["dwrr_pct"] > 0)]
            .sort_values(by="dwrr_pct", ascending=False)
            .head(nbr_of_tickers)[["dwrr_pct", "return"]]
        )
        gainers = helper.prettify_dataframe(gainers)
        losers = (
            portfolio_summary[conditions & (portfolio_summary["dwrr_pct"] < 0)]
            .sort_values(by="dwrr_pct", ascending=True)
            .head(nbr_of_tickers)[["dwrr_pct", "return"]]
        )
        losers = helper.prettify_dataframe(losers)

        message += (
            "<p>Portfolio Summary</p>"
            "<ul>"
            f"<li>portfolio: {portfolio}</li>"
            f"<li>lookback: {lookback}</li>"
            f"<li>return: {portfolio_pct:.2%}</li>"
            "</ul>"
            "<br>"
            "<table style='width:100%;'>"
            "<tr>"
            "<th>Gainers</th>"
            "<th>Losers</th>"
            "</tr>"
            "<tr>"
            f"<td>{gainers.to_html()}</td>"
            f"<td>{losers.to_html()}</td>"
            "</tr>"
            "</table>"
            "<br>"
        )

    return send_email(
        message, subject=subject, email_list=email_list, image_list=image_list
    )
