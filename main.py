import requests

from rich.console import Console
from rich.prompt import Prompt, IntPrompt

console = Console(
    width=100,
    log_path=False
)
LUTION_API_KEY = ""
BEEMAIL_API_KEY = ""

class MailPurchaser:

    def __init__(self, purchase_amount: int) -> None:
        self.purchase_amount = purchase_amount
        self.total_purchased = 0

    def purchase_lution_mail(self, mail_code: str) -> str:
        headers = {
            "Authorization": f"Bearer {LUTION_API_KEY}"
        }
        response = requests.get(f"https://api.lution.ee/mail/buy?mailcode={mail_code}&quantity=1", headers=headers)
        if response.status_code == 200:
            email = response.json()["Data"]["Emails"][0]["Email"]
            password = response.json()["Data"]["Emails"][0]["Password"]
            self.total_purchased += 1
            return f"{email}:{password}"
        else:
            return ""

    def lution_process(self) -> None:
        while self.total_purchased != self.purchase_amount:
            for mail_code in ["OUTLOOK", "HOTMAIL"]:
                mail = self.purchase_lution_mail(mail_code)
                if mail:
                    console.log(
                        f"[{self.total_purchased}] Purchased Mail | {mail}"
                    )
                    with open("mails.txt", "a") as f:
                        f.write(mail + "\n")
        else:
            print()
            console.log(
                f"[END] Finished purchasing e-mails."
            )

    def purchase_beemail(self) -> str:
        response = requests.get(f"http://bee-mails.com/getEmail?num=1&key={BEEMAIL_API_KEY}&emailType&format=txt")
        if '"success":false' not in response.text:
            mail = response.text.strip()
            self.total_purchased += 1
            return mail
        else:
            return ""

    def beemail_process(self) -> None:
        while self.total_purchased != self.purchase_amount:
            mail = self.purchase_beemail()
            if mail:
                console.log(
                    f"[{self.total_purchased}] Purchased Mail | {mail}"
                )
                with open("mails.txt", "a") as f:
                    f.write(mail + "\n")
        else:
            print()
            console.log(
                f"[END] Finished purchasing e-mails."
            )


if __name__ == "__main__":
    console.rule("Pixens' Mail Purchaser (github.com/Pixens)")
    print()
    purchaser_type = Prompt.ask("Service you want to purchase from", choices=["LUTION", "BEEMAIL"], default="LUTION")
    amount = IntPrompt.ask("Number of e-mails you want to purchase")
    print()
    console.log(f"Purchasing {amount} e-mails from {purchaser_type}.")
    print()
    match purchaser_type:
        case "LUTION":
            if not LUTION_API_KEY:
                console.log(
                    "[red] Lution.ee API key not set."
                )
                print()
                quit()

            MailPurchaser(amount).lution_process()
        case "BEEMAIL":
            if not LUTION_API_KEY:
                console.log(
                    "[red] BeeMail bot API key not set."
                )
                quit()

            MailPurchaser(amount).beemail_process()
