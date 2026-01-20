import time


from database import init_db, save_perks, get_all_perks
from service import process_screenshot

SELECTED_MODEL = 'openbmb/minicpm-v4.5'
DEFAULT_TEMPERATURE = 0
CHOSEN_IMAGE = 'screenshots/amexTravel.png'


def main():

    init_db()
    try:


        start = time.perf_counter()
        perk_list = process_screenshot(CHOSEN_IMAGE, SELECTED_MODEL, DEFAULT_TEMPERATURE)
        elapsed = time.perf_counter() - start

        result = save_perks(perk_list)
        print(f"Saved: {result['inserted']} new, {result['skipped']} duplicates")

        print(f"\nDone in {elapsed:.2f}s")
        print(f"\nOverall confidence: {perk_list.overall_confidence}")

        for p in perk_list.perks:
            print(
                f"- {p.company_name} | {p.offer_text} | expiry={p.expiry_text} | conf={p.confidence}\n"
                f"  -> pct={p.percentage_value}, min_spend={p.minimum_spend}, "
                f"money_back={p.money_back}, cap={p.cap_amount}\n"
            )

        all_perks_in_db = get_all_perks()
        for x in all_perks_in_db:
            print(x)

    except FileNotFoundError as e:
        print(e)
        exit(1)
    except Exception as e:
        print("Unexpected error" + str(e))
        exit(1)

if __name__ == "__main__":
    main()
