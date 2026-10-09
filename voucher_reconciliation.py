
import argparse
import pandas as pd


def load_files(crm, groupon):
    crm = pd.read_csv(crm, dtype=str).fillna("")
    groupon = pd.read_csv(groupon, dtype=str, encoding="utf-8-sig").fillna("")
    groupon["clean_code"] = groupon["Groupon Code"].str.strip().str.upper()
    crm["clean_code"] = crm["voucher_code"].str.strip().str.upper()
    return crm, groupon


def add_issues(issues, df, issue_type, note):
    for code in df["clean_code"]:
        issues.append({
            "issue_type": issue_type,
            "voucher_code": code if code else "(blank)",
            "notes": note,
        })


def find_issues(crm, groupon):
    issues = []

    # Groupon-side checks
    add_issues(issues, groupon[groupon["clean_code"] == ""],
               "Blank code in Groupon file", "Code is empty")

    not_blank = groupon[groupon["clean_code"] != ""]

    add_issues(issues, not_blank[not_blank.duplicated("clean_code", keep="first")],
               "Duplicate in Groupon file", "Same code appears more than once")

    groupon["date"] = pd.to_datetime(groupon["Redeemed On"], format="%d/%m/%Y", errors="coerce")
    add_issues(issues, groupon[groupon["date"].isna()],
               "Invalid date", "Date does not exist")

    groupon_unique = not_blank.drop_duplicates("clean_code")
    crm_unique = crm.drop_duplicates("clean_code")

    add_issues(issues, groupon_unique[~groupon_unique["clean_code"].isin(crm["clean_code"])],
               "In Groupon, not in CRM", "Code not found in CRM")

    merged = groupon_unique.merge(crm_unique, on="clean_code", how="inner")
    merged["groupon_price"] = merged["Price Paid"].str.replace("£", "", regex=False).astype(float)
    merged["crm_price"] = merged["amount_gbp"].astype(float)

    add_issues(issues, merged[merged["groupon_price"] != merged["crm_price"]],
               "Price mismatch", "Groupon price differs from CRM")

    add_issues(issues, merged[merged["status"] == "ISSUED"],
               "Status mismatch (CRM ISSUED, Groupon Redeemed)", "CRM needs updating to redeemed")

    # CRM-side checks
    redeemed = crm[crm["status"] == "REDEEMED"]
    add_issues(issues, redeemed[~redeemed["clean_code"].isin(groupon["clean_code"])],
               "In CRM redeemed, missing from Groupon", "Redeemed per CRM but not in Groupon report")

    add_issues(issues, crm[crm.duplicated("clean_code", keep="first")],
               "Duplicate voucher in CRM", "Same voucher appears twice in CRM")

    add_issues(issues, crm[crm["email"] == ""],
               "Missing email in CRM", "Customer email blank")

    return pd.DataFrame(issues, columns=["issue_type", "voucher_code", "notes"])



def main():
    parser = argparse.ArgumentParser(description="Reconcile CRM vouchers with a Groupon report")
    parser.add_argument("--crm", required=True, help="path to CRM export CSV")
    parser.add_argument("--groupon", required=True, help="path to Groupon report CSV")
    parser.add_argument("--out", default="exceptions_report.csv", help="output file name")
    args = parser.parse_args()

    crm, groupon = load_files(args.crm, args.groupon)
    report = find_issues(crm, groupon)
    report.to_csv(args.out, index=False)

    print(report["issue_type"].value_counts())
    print("\nTotal issues:", len(report))
    print("Report saved to:", args.out)


if __name__ == "__main__":
    main()
